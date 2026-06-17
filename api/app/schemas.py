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


class AskTutorIn(BaseModel):
    question: str


class AskTutorOut(BaseModel):
    answer: str
    model: str  # which model actually answered (honest), e.g. the Claude model id


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
    avatar_url: str | None = None
    provider: str


class RegisterIn(BaseModel):
    name: str
    email: str
    password: str


class LoginIn(BaseModel):
    email: str
    password: str


class GoogleSyncIn(BaseModel):
    email: str
    name: str
    avatar_url: str | None = None


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
    source: Literal["llm", "seeded_fallback"]
    questions: list[QuizQuestionOut]


class AnswerIn(BaseModel):
    question_id: int
    type: Literal["mcq", "predict_output", "pseudocode_order"]
    prompt: str
    # Reference answer travels with LLM-generated questions (negative ids) since
    # they aren't in the DB; for seeded questions it's looked up server-side.
    reference_answer: Any | None = None
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


class ProgressOut(BaseModel):
    student_id: int
    mastery: list[MasteryOut]
    next_concept_slug: str | None
