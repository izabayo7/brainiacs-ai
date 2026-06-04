"""Student mastery overview + recommended next concept. Also a student picker."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Concept, Student
from app.schemas import MasteryOut, ProgressOut, StudentOut
from app.services import compute_states, recommend_next_concept

router = APIRouter(tags=["progress"])


@router.get("/students", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)) -> list[StudentOut]:
    students = db.scalars(select(Student).order_by(Student.id)).all()
    return [StudentOut.model_validate(s) for s in students]


@router.get("/progress/{student_id}", response_model=ProgressOut)
def get_progress(student_id: int, db: Session = Depends(get_db)) -> ProgressOut:
    if db.get(Student, student_id) is None:
        raise HTTPException(status_code=404, detail="Student not found")

    states = compute_states(db, student_id)
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

    nxt = recommend_next_concept(db, student_id)
    return ProgressOut(
        student_id=student_id,
        mastery=mastery,
        next_concept_slug=nxt.slug if nxt else None,
    )
