"""Authenticated learner's mastery overview + recommended next concept."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_student
from app.db import get_db
from app.models import Concept, Student
from app.schemas import MasteryOut, ProgressOut
from app.services import compute_states, recommend_next_concept

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

    nxt = recommend_next_concept(db, current.id)
    return ProgressOut(
        student_id=current.id,
        mastery=mastery,
        next_concept_slug=nxt.slug if nxt else None,
    )
