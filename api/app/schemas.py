"""Pydantic request/response models for the API."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


# --- Concepts / map -----------------------------------------------------------

ConceptState = Literal["locked", "available", "mastered"]


class ConceptStateOut(BaseModel):
    id: int
    slug: str
    name: str
    order_hint: int
    state: ConceptState
    p_mastered: float
    attempts: int
    prerequisite_ids: list[int]


# --- Chapters -----------------------------------------------------------------

class ChapterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    concept_id: int
    title: str
    body_md: str
    video_url: str | None = None


class ConceptDetailOut(BaseModel):
    id: int
    slug: str
    name: str
    summary: str = ""
    explanation_md: str
    worked_example_md: str
    state: ConceptState
    chapters: list[ChapterOut]


# --- Students -----------------------------------------------------------------

class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str


# --- Auth ---------------------------------------------------------------------

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str


class RegisterIn(BaseModel):
    name: str
    email: str
    password: str


class LoginIn(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# --- Quiz ---------------------------------------------------------------------

class QuizQuestionOut(BaseModel):
    # `id` is the persisted exercise id when seeded; ephemeral negative ids for
    # freshly-generated questions so the client can submit them back.
    id: int
    type: Literal["mcq", "predict_output", "pseudocode_order"]
    difficulty: Literal["easy", "medium", "hard"]
    prompt: str
    # plain strings, or {shape, text} boxes when answer_format == "flowchart"
    options: list[Any] | None = None
    prompt_diagram: dict | None = None       # flowchart shown above the prompt
    answer_format: str = "text"              # "text" | "flowchart" (ordering questions)
    # correct_answer is intentionally omitted from the student-facing payload.


class QuizOut(BaseModel):
    concept_id: int
    source: Literal["bank"]  # questions come from the seeded item bank (no external model)
    questions: list[QuizQuestionOut]


class AnswerIn(BaseModel):
    question_id: int
    type: Literal["mcq", "predict_output", "pseudocode_order"]
    prompt: str
    response: Any


class QuizSubmitIn(BaseModel):
    # student comes from the auth token, not the payload.
    concept_id: int
    answers: list[AnswerIn]


class GradedAnswerOut(BaseModel):
    question_id: int
    is_correct: bool
    score: float
    misconception_label: str
    explanation: str


class QuizResultOut(BaseModel):
    concept_id: int
    graded: list[GradedAnswerOut]
    p_mastered: float
    attempts: int
    mastered: bool
    newly_unlocked: list[str]
    next_concept_slug: str | None
    encouragement: str


# --- Progress -----------------------------------------------------------------

class MasteryOut(BaseModel):
    concept_id: int
    concept_slug: str
    concept_name: str
    p_mastered: float
    attempts: int
    state: ConceptState
    updated_at: datetime | None = None


class DifficultyOut(BaseModel):
    label: str          # taxonomy id, e.g. loop_boundary_offbyone
    human: str          # plain-language phrasing
    count: int          # how many wrong attempts the system attributed to it


class ProgressOut(BaseModel):
    student_id: int
    mastery: list[MasteryOut]
    next_concept_slug: str | None
    total_attempts: int = 0
    # What the learner model (BKT + graded attempts) has noticed — the AI made visible.
    recurring_difficulties: list[DifficultyOut] = []
