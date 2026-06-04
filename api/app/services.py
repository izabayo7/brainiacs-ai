"""Shared domain logic: per-student concept state and next-concept recommendation.

Kept in one place so the concepts, quiz, and progress routers agree on what
LOCKED / AVAILABLE / MASTERED mean.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.bkt import is_mastered
from app.models import Concept, ConceptPrerequisite, MasteryEstimate


def _mastery_map(db: Session, student_id: int) -> dict[int, MasteryEstimate]:
    rows = db.scalars(
        select(MasteryEstimate).where(MasteryEstimate.student_id == student_id)
    ).all()
    return {row.concept_id: row for row in rows}


def _prerequisite_map(db: Session) -> dict[int, list[int]]:
    edges = db.scalars(select(ConceptPrerequisite)).all()
    prereqs: dict[int, list[int]] = {}
    for edge in edges:
        prereqs.setdefault(edge.concept_id, []).append(edge.prerequisite_concept_id)
    return prereqs


def compute_states(db: Session, student_id: int) -> dict[int, dict]:
    """Return {concept_id: {state, p_mastered, attempts, prerequisite_ids}}.

    A concept is MASTERED per the BKT gate; AVAILABLE when every prerequisite is
    mastered; otherwise LOCKED. Concepts with no prerequisites start AVAILABLE.
    """
    concepts = db.scalars(select(Concept)).all()
    mastery = _mastery_map(db, student_id)
    prereqs = _prerequisite_map(db)

    mastered_ids: set[int] = set()
    info: dict[int, dict] = {}
    for concept in concepts:
        est = mastery.get(concept.id)
        p = est.p_mastered if est else 0.0
        attempts = est.attempts if est else 0
        if is_mastered(p, attempts):
            mastered_ids.add(concept.id)
        info[concept.id] = {
            "p_mastered": p,
            "attempts": attempts,
            "prerequisite_ids": prereqs.get(concept.id, []),
        }

    for concept in concepts:
        cid = concept.id
        if cid in mastered_ids:
            state = "mastered"
        elif all(pid in mastered_ids for pid in prereqs.get(cid, [])):
            state = "available"
        else:
            state = "locked"
        info[cid]["state"] = state

    return info


def recommend_next_concept(db: Session, student_id: int) -> Concept | None:
    """Lowest order_hint concept that is AVAILABLE (not yet mastered)."""
    states = compute_states(db, student_id)
    concepts = db.scalars(select(Concept).order_by(Concept.order_hint)).all()
    for concept in concepts:
        if states[concept.id]["state"] == "available":
            return concept
    return None
