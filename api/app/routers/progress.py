"""Authenticated learner's mastery overview + recommended next concept."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth import get_current_student
from app.db import get_db
from app.models import Attempt, Concept, Student
from app.schemas import DifficultyOut, MasteryOut, ProgressOut
from app.services import compute_states, recommend_next_concept
from app.taxonomy import humanize

router = APIRouter(tags=["progress"])


@router.get("/progress", response_model=ProgressOut)
def get_progress(
    current: Student = Depends(get_current_student), db: Session = Depends(get_db)
) -> ProgressOut:
    states = compute_states(db, current.id)
    concepts = {c.id: c for c in db.scalars(select(Concept).order_by(Concept.order_hint)).all()}

    mastery = [
        MasteryOut(
            concept_id=cid,
            concept_slug=concepts[cid].slug,
            concept_name=concepts[cid].name,
            p_mastered=info["p_mastered"],
            attempts=info["attempts"],
            state=info["state"],
        )
        for cid, info in sorted(states.items(), key=lambda kv: concepts[kv[0]].order_hint)
    ]

    total_attempts = db.scalar(
        select(func.count()).select_from(Attempt).where(Attempt.student_id == current.id)
    ) or 0

    # The learner model made visible: which misconceptions the grader has attributed to
    # this student's wrong answers, most frequent first.
    rows = db.execute(
        select(Attempt.misconception_label, func.count().label("n"))
        .where(
            Attempt.student_id == current.id,
            Attempt.is_correct.is_(False),
            Attempt.misconception_label.is_not(None),
            Attempt.misconception_label != "none",
        )
        .group_by(Attempt.misconception_label)
        .order_by(func.count().desc())
        .limit(3)
    ).all()
    recurring = [DifficultyOut(label=lbl, human=humanize(lbl), count=n) for lbl, n in rows]

    nxt = recommend_next_concept(db, current.id)
    return ProgressOut(
        student_id=current.id,
        mastery=mastery,
        next_concept_slug=nxt.slug if nxt else None,
        total_attempts=int(total_attempts),
        recurring_difficulties=recurring,
    )
