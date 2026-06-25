"""Quiz flow: serve a per-student quiz from the seeded bank, then grade
deterministically, run the BKT update, persist attempts, recompute mastery + unlocks.

No external model is involved: quizzes are drawn from the human-authored item bank
(random subset + shuffled options) and grading is deterministic (see grading.py).
This NEVER executes student input.
"""
from __future__ import annotations

import logging
import random

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_student
from app.bkt import is_mastered, update_mastery
from app.db import get_db
from app.grading import offline_explain, offline_grade_and_classify
from app.models import Attempt, Concept, Exercise, MasteryEstimate, Student
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

NUM_QUESTIONS = 4


def _shuffle_options(options, qtype: str, correct=None):
    """Shuffle displayed options so positions aren't shareable ("pick option 2").
    Grading compares option TEXT, so reordering is safe. For ordering questions,
    avoid presenting the lines already in the right order."""
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
    pool = db.scalars(select(Exercise).where(Exercise.concept_id == concept_id)).all()
    # Random subset + shuffled options, so two students don't get the same questions in
    # the same order (anti-cheating).
    chosen = random.sample(pool, min(NUM_QUESTIONS, len(pool)))
    questions = [
        QuizQuestionOut(
            id=ex.id,
            type=ex.type.value,
            difficulty=ex.difficulty.value,
            prompt=ex.prompt,
            options=_shuffle_options(ex.options_json, ex.type.value, ex.correct_answer_json),
            prompt_diagram=ex.prompt_diagram,
            answer_format=ex.answer_format or "text",
        )
        for ex in chosen
    ]
    return QuizOut(concept_id=concept_id, source="bank", questions=questions)


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
    return _seeded_quiz(db, concept_id)


def _reference_for(db: Session, question_id: int) -> tuple[str, object, str | None, str | None]:
    """Return (prompt, reference_answer, target_misconception, authored_explanation)."""
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
        # Deterministic grading — no external model.
        result = offline_grade_and_classify(reference, ans.response, target_misconception)
        is_correct = bool(result.get("is_correct"))
        misconception = result.get("misconception_label", "none")
        explanation = result.get("explanation", "")

        # Scaffolded explanation for wrong answers: prefer the human-authored one,
        # else a per-misconception hint. Never reveals the full answer.
        if not is_correct:
            explanation = authored_explanation or offline_explain(misconception, concept.name)

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
