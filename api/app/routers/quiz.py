"""The AI loop: generate a per-student quiz, then grade + classify + explain.

Flow:
  POST /quiz/{concept_id}/generate?student_id=...
      -> LLM generates questions grounded in the chapter; on any failure we fall
         back to the pre-seeded exercises so the demo is never empty.
  POST /quiz/{concept_id}/submit
      -> grade each answer, classify the misconception, write an explanation,
         run the BKT update, persist attempts, recompute mastery + unlocks.
"""
from __future__ import annotations

import itertools
import logging
import random

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_student
from app.bkt import is_mastered, update_mastery
from app.db import get_db
from app.grading import offline_explain, offline_grade_and_classify
from app.llm import get_llm_client
from app.models import (
    Attempt,
    Chapter,
    Concept,
    Difficulty,
    Exercise,
    ExerciseType,
    MasteryEstimate,
    Student,
)
from app.schemas import (
    GradedAnswerOut,
    QuizOut,
    QuizQuestionOut,
    QuizResultOut,
    QuizSubmitIn,
)
from app.services import compute_states, recommend_next_concept

logger = logging.getLogger("brainiacs.quiz")
router = APIRouter(prefix="/quiz", tags=["quiz"])

# Ephemeral ids for freshly-generated (non-persisted) questions count down from -1.
_ephemeral_ids = itertools.count(start=-1, step=-1)

# In-memory map question_id -> reference_answer for generated questions, so the
# correct answer is NOT shipped to the browser.
# TODO: replace with a short-lived store (Redis / DB quiz row) before multi-worker
# deployment — a module dict is per-process and lost on restart.
_reference_cache: dict[int, dict] = {}

NUM_QUESTIONS = 4


def _shuffle_options(options, qtype: str, correct=None):
    """Shuffle the displayed options so answer positions aren't shareable between
    students ("pick option 2"). Grading compares the option TEXT, so reordering is
    safe. For ordering questions, avoid presenting the lines already in the right order."""
    if not isinstance(options, list) or len(options) < 2:
        return options
    shuffled = list(options)
    random.shuffle(shuffled)
    if qtype == "pseudocode_order" and isinstance(correct, list):
        tries = 0
        while shuffled == list(correct) and tries < 10:
            random.shuffle(shuffled)
            tries += 1
    return shuffled


def _seeded_quiz(db: Session, concept_id: int) -> QuizOut:
    pool = db.scalars(
        select(Exercise).where(Exercise.concept_id == concept_id)
    ).all()
    # Pick a random subset and shuffle each question's options, so two students don't
    # get the same questions in the same order.
    chosen = random.sample(pool, min(NUM_QUESTIONS, len(pool)))
    questions = [
        QuizQuestionOut(
            id=ex.id,
            type=ex.type.value,
            difficulty=ex.difficulty.value,
            prompt=ex.prompt,
            options=_shuffle_options(ex.options_json, ex.type.value, ex.correct_answer_json),
        )
        for ex in chosen
    ]
    return QuizOut(concept_id=concept_id, source="seeded_fallback", questions=questions)


@router.post("/{concept_id}/generate", response_model=QuizOut)
def generate_quiz(
    concept_id: int,
    current: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
) -> QuizOut:
    concept = db.get(Concept, concept_id)
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    states = compute_states(db, current.id)
    if states[concept_id]["state"] == "locked":
        raise HTTPException(status_code=403, detail="Concept is locked")
    student_mastery = states[concept_id]["p_mastered"]

    chapter = db.scalars(
        select(Chapter).where(Chapter.concept_id == concept_id).order_by(Chapter.id)
    ).first()
    chapter_body = chapter.body_md if chapter else concept.explanation_md

    # Try the LLM; on ANY failure fall back to seeded exercises (demo must work).
    try:
        client = get_llm_client()
        raw_questions = client.generate_quiz(
            concept={"name": concept.name, "slug": concept.slug},
            chapter_body=chapter_body,
            student_mastery=student_mastery,
            num_questions=NUM_QUESTIONS,
        )
    except Exception as exc:  # noqa: BLE001 - any failure -> graceful fallback
        logger.warning("LLM quiz-gen failed (%s); using seeded fallback", exc)
        return _seeded_quiz(db, concept_id)

    questions: list[QuizQuestionOut] = []
    for q in raw_questions:
        qid = next(_ephemeral_ids)
        _reference_cache[qid] = {
            "prompt": q.get("prompt", ""),
            "type": q.get("type", "mcq"),
            "reference_answer": q.get("correct_answer"),
        }
        questions.append(
            QuizQuestionOut(
                id=qid,
                type=q.get("type", "mcq"),
                difficulty=q.get("difficulty", "medium"),
                prompt=q.get("prompt", ""),
                options=_shuffle_options(
                    q.get("options"), q.get("type", "mcq"), q.get("correct_answer")
                ),
            )
        )
    if not questions:
        return _seeded_quiz(db, concept_id)
    return QuizOut(concept_id=concept_id, source="llm", questions=questions)


def _reference_for(db: Session, question_id: int) -> tuple[str, object, str | None, str | None]:
    """Return (prompt, reference_answer, target_misconception, authored_explanation)."""
    if question_id < 0:
        cached = _reference_cache.get(question_id)
        if cached is None:
            raise HTTPException(
                status_code=400,
                detail="Generated question expired; regenerate the quiz",
            )
        # Generated questions carry no pre-authored misconception/explanation.
        return cached["prompt"], cached["reference_answer"], None, None
    exercise = db.get(Exercise, question_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail=f"Exercise {question_id} not found")
    return (exercise.prompt, exercise.correct_answer_json,
            exercise.target_misconception, exercise.explanation)


@router.post("/{concept_id}/submit", response_model=QuizResultOut)
def submit_quiz(
    concept_id: int,
    payload: QuizSubmitIn,
    current: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
) -> QuizResultOut:
    concept = db.get(Concept, concept_id)
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    # Which concepts were already mastered, to compute what gets newly unlocked.
    before = compute_states(db, current.id)

    # Use the LLM when configured; otherwise grade seeded answers deterministically
    # so the demo runs with no API key (and stays deterministic for the video).
    try:
        client = get_llm_client()
    except Exception as exc:  # noqa: BLE001 - no key / SDK -> offline grading
        logger.info("No LLM client (%s); using offline grader", exc)
        client = None

    # Load / create this student's mastery row for the concept.
    estimate = db.scalars(
        select(MasteryEstimate).where(
            MasteryEstimate.student_id == current.id,
            MasteryEstimate.concept_id == concept_id,
        )
    ).first()
    if estimate is None:
        estimate = MasteryEstimate(
            student_id=current.id, concept_id=concept_id, p_mastered=0.0, attempts=0
        )
        db.add(estimate)

    graded: list[GradedAnswerOut] = []
    for ans in payload.answers:
        prompt, reference, target_misconception, authored_explanation = _reference_for(
            db, ans.question_id
        )
        if ans.reference_answer is not None:
            reference = ans.reference_answer  # client-supplied override (generated qs)

        if client is not None:
            result = client.grade_and_classify(
                question=prompt, reference_answer=reference, student_answer=ans.response
            )
        else:
            result = offline_grade_and_classify(reference, ans.response, target_misconception)

        is_correct = bool(result.get("is_correct"))
        misconception = result.get("misconception_label", "none")
        explanation = result.get("explanation", "")

        # Scaffolded explanation for wrong answers (don't reveal the full answer).
        if not is_correct:
            if authored_explanation and client is None:
                # Prefer the human-authored explanation for seeded exercises offline.
                explanation = authored_explanation
            elif client is not None:
                try:
                    explanation = client.explain(
                        misconception_label=misconception,
                        concept={"name": concept.name},
                        student_answer=ans.response,
                    )
                except Exception as exc:  # noqa: BLE001 - keep the grade even if explain fails
                    logger.warning("explain() failed: %s", exc)
            else:
                explanation = offline_explain(misconception, concept.name)

        # Persist the attempt. Only seeded exercises (positive id) FK-link cleanly.
        if ans.question_id > 0:
            db.add(
                Attempt(
                    student_id=current.id,
                    exercise_id=ans.question_id,
                    response_json=ans.response,
                    is_correct=is_correct,
                    misconception_label=misconception,
                    explanation_text=explanation,
                )
            )

        # BKT update per answer.
        step = update_mastery(estimate.p_mastered, estimate.attempts, is_correct)
        estimate.p_mastered = step.p_mastered
        estimate.attempts = step.attempts

        graded.append(
            GradedAnswerOut(
                question_id=ans.question_id,
                is_correct=is_correct,
                score=float(result.get("score", 1.0 if is_correct else 0.0)),
                misconception_label=misconception,
                explanation=explanation,
            )
        )

    db.commit()

    # Recompute states to find newly-unlocked concepts.
    after = compute_states(db, current.id)
    mastered_after = {cid for cid, info in after.items() if info["state"] == "mastered"}
    available_after = {cid for cid, info in after.items() if info["state"] == "available"}
    newly_unlocked_ids = available_after - {
        cid for cid, info in before.items() if info["state"] in ("available", "mastered")
    }
    id_to_slug = {c.id: c.slug for c in db.scalars(select(Concept)).all()}
    newly_unlocked = [id_to_slug[cid] for cid in newly_unlocked_ids]

    mastered_now = is_mastered(estimate.p_mastered, estimate.attempts)
    nxt = recommend_next_concept(db, current.id)

    if mastered_now:
        encouragement = "Great work — you've mastered this concept!"
    elif estimate.attempts < 3:
        encouragement = "Nice start. A little more practice and you'll have this."
    else:
        encouragement = "You're getting there. Let's practise the tricky parts once more."

    return QuizResultOut(
        concept_id=concept_id,
        graded=graded,
        p_mastered=estimate.p_mastered,
        attempts=estimate.attempts,
        mastered=mastered_now,
        newly_unlocked=newly_unlocked,
        next_concept_slug=nxt.slug if nxt else None,
        encouragement=encouragement,
    )
