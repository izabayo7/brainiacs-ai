"""ORM models — the §4 schema.

A strict prerequisite DAG of concepts, human-authored chapters/exercises, and
per-student attempts + mastery estimates. Names are full and meaningful.
"""
from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class ExerciseType(str, enum.Enum):
    mcq = "mcq"
    predict_output = "predict_output"
    pseudocode_order = "pseudocode_order"


class Difficulty(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Concept(Base):
    __tablename__ = "concept"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    order_hint: Mapped[int] = mapped_column(Integer, default=0)
    summary: Mapped[str] = mapped_column(Text, default="", server_default="")  # one-line lead
    explanation_md: Mapped[str] = mapped_column(Text, default="")
    worked_example_md: Mapped[str] = mapped_column(Text, default="")

    chapters: Mapped[list["Chapter"]] = relationship(back_populates="concept")
    exercises: Mapped[list["Exercise"]] = relationship(back_populates="concept")
    # Edges where THIS concept is the dependent (i.e. its prerequisites).
    prerequisite_edges: Mapped[list["ConceptPrerequisite"]] = relationship(
        back_populates="concept",
        foreign_keys="ConceptPrerequisite.concept_id",
    )


class ConceptPrerequisite(Base):
    """A directed edge of the prerequisite DAG: concept_id requires prerequisite_concept_id."""

    __tablename__ = "concept_prerequisite"
    __table_args__ = (
        UniqueConstraint("concept_id", "prerequisite_concept_id", name="uq_concept_prereq"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    concept_id: Mapped[int] = mapped_column(ForeignKey("concept.id"), index=True)
    prerequisite_concept_id: Mapped[int] = mapped_column(ForeignKey("concept.id"), index=True)

    concept: Mapped["Concept"] = relationship(
        back_populates="prerequisite_edges", foreign_keys=[concept_id]
    )


class Chapter(Base):
    __tablename__ = "chapter"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    concept_id: Mapped[int] = mapped_column(ForeignKey("concept.id"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    body_md: Mapped[str] = mapped_column(Text)
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    concept: Mapped["Concept"] = relationship(back_populates="chapters")


class Exercise(Base):
    __tablename__ = "exercise"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    concept_id: Mapped[int] = mapped_column(ForeignKey("concept.id"), index=True)
    type: Mapped[ExerciseType] = mapped_column(Enum(ExerciseType, name="exercise_type"))
    difficulty: Mapped[Difficulty] = mapped_column(Enum(Difficulty, name="difficulty"))
    prompt: Mapped[str] = mapped_column(Text)
    # MCQ choices / ordering lines. Shape depends on `type`.
    options_json: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)
    correct_answer_json: Mapped[dict | list | str] = mapped_column(JSONB)
    target_misconception: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Human-authored scaffolded explanation (names the misconception, not the full answer).
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

    concept: Mapped["Concept"] = relationship(back_populates="exercises")


class Student(Base):
    """A learner / authenticated user. (Kept named `student` since all progress FKs
    reference student_id; functionally this is the app's user account.)"""

    __tablename__ = "student"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    # Auth fields. password_hash is null for OAuth (Google) accounts.
    password_hash: Mapped[str | None] = mapped_column(String(200), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    provider: Mapped[str] = mapped_column(
        String(20), default="password", server_default="password"
    )  # password | google


class Attempt(Base):
    __tablename__ = "attempt"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), index=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise.id"), index=True)
    response_json: Mapped[dict | list | str] = mapped_column(JSONB)
    is_correct: Mapped[bool] = mapped_column(Boolean)
    misconception_label: Mapped[str | None] = mapped_column(String(64), nullable=True)
    explanation_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MasteryEstimate(Base):
    __tablename__ = "mastery_estimate"
    __table_args__ = (
        UniqueConstraint("student_id", "concept_id", name="uq_mastery_student_concept"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), index=True)
    concept_id: Mapped[int] = mapped_column(ForeignKey("concept.id"), index=True)
    p_mastered: Mapped[float] = mapped_column(Float, default=0.0)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
