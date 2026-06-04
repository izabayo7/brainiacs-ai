"""Concept map + per-student lock/available/mastered state, and concept detail."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Chapter, Concept
from app.schemas import ChapterOut, ConceptDetailOut, ConceptStateOut
from app.services import compute_states

router = APIRouter(prefix="/concepts", tags=["concepts"])


@router.get("", response_model=list[ConceptStateOut])
def list_concepts(student_id: int, db: Session = Depends(get_db)) -> list[ConceptStateOut]:
    states = compute_states(db, student_id)
    concepts = db.scalars(select(Concept).order_by(Concept.order_hint)).all()
    return [
        ConceptStateOut(
            id=c.id,
            slug=c.slug,
            name=c.name,
            order_hint=c.order_hint,
            state=states[c.id]["state"],
            p_mastered=states[c.id]["p_mastered"],
            attempts=states[c.id]["attempts"],
            prerequisite_ids=states[c.id]["prerequisite_ids"],
        )
        for c in concepts
    ]


@router.get("/{concept_id}", response_model=ConceptDetailOut)
def get_concept(
    concept_id: int, student_id: int, db: Session = Depends(get_db)
) -> ConceptDetailOut:
    concept = db.get(Concept, concept_id)
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    states = compute_states(db, student_id)
    state = states[concept.id]["state"]
    if state == "locked":
        # Locked concepts are not reachable — prerequisites unmet.
        raise HTTPException(status_code=403, detail="Concept is locked; finish prerequisites first")

    chapters = db.scalars(
        select(Chapter).where(Chapter.concept_id == concept_id).order_by(Chapter.id)
    ).all()
    return ConceptDetailOut(
        id=concept.id,
        slug=concept.slug,
        name=concept.name,
        explanation_md=concept.explanation_md,
        worked_example_md=concept.worked_example_md,
        state=state,
        chapters=[ChapterOut.model_validate(ch) for ch in chapters],
    )
