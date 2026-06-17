"""Concept map + per-student lock/available/mastered state, and concept detail."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_student
from app.config import settings
from app.db import get_db
from app.llm import get_llm_client
from app.models import Chapter, Concept, Student
from app.schemas import AskTutorIn, AskTutorOut, ChapterOut, ConceptDetailOut, ConceptStateOut
from app.services import compute_states

router = APIRouter(prefix="/concepts", tags=["concepts"])


@router.get("", response_model=list[ConceptStateOut])
def list_concepts(
    current: Student = Depends(get_current_student), db: Session = Depends(get_db)
) -> list[ConceptStateOut]:
    states = compute_states(db, current.id)
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
    concept_id: int,
    current: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
) -> ConceptDetailOut:
    concept = db.get(Concept, concept_id)
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    states = compute_states(db, current.id)
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
        summary=concept.summary or "",
        explanation_md=concept.explanation_md,
        worked_example_md=concept.worked_example_md,
        state=state,
        chapters=[ChapterOut.model_validate(ch) for ch in chapters],
    )


@router.post("/{concept_id}/ask", response_model=AskTutorOut)
def ask_tutor(
    concept_id: int,
    payload: AskTutorIn,
    current: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
) -> AskTutorOut:
    """Lesson-scoped tutor chat. Uses the configured LLM; honest about which model."""
    concept = db.get(Concept, concept_id)
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Ask a question first")

    chapter = db.scalars(
        select(Chapter).where(Chapter.concept_id == concept_id).order_by(Chapter.id)
    ).first()
    chapter_body = chapter.body_md if chapter else concept.explanation_md

    try:
        client = get_llm_client()
    except Exception:  # noqa: BLE001 - no model configured in this environment
        return AskTutorOut(
            answer=(
                "The AI tutor isn't enabled in this environment yet. In the meantime, "
                "re-read the Key ideas above and try the quiz — it pinpoints exactly "
                "what to review."
            ),
            model="not configured",
        )
    answer = client.ask_tutor(
        concept={"name": concept.name}, chapter_body=chapter_body, question=question
    )
    return AskTutorOut(answer=answer, model=settings.anthropic_model)
