"""LLMClient seam — the one abstraction we deliberately keep.

Today the demo is backed by the Anthropic API (Claude). The production plan is a
self-hosted fine-tuned Qwen3.5-4B; swapping it in means writing one more subclass
of `LLMClient` and changing the factory below. Nothing else in the app changes.

The three jobs (§5): generate_quiz, grade_and_classify, explain. All pseudocode /
conceptual only — this module NEVER executes student input.
"""
from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from typing import Any

from app.config import settings
from app.taxonomy import MISCONCEPTION_LABELS, is_valid_label

logger = logging.getLogger("brainiacs.llm")


class LLMClient(ABC):
    @abstractmethod
    def generate_quiz(
        self, concept: dict, chapter_body: str, student_mastery: float, num_questions: int = 4
    ) -> list[dict]:
        """Return a list of exercise-like dicts grounded ONLY in chapter_body."""

    @abstractmethod
    def grade_and_classify(
        self, question: str, reference_answer: Any, student_answer: Any
    ) -> dict:
        """Return {is_correct, score, misconception_label, explanation}."""

    @abstractmethod
    def explain(self, misconception_label: str, concept: dict, student_answer: Any) -> str:
        """Return a short scaffolded explanation that does not give away the answer."""

    @abstractmethod
    def ask_tutor(self, concept: dict, chapter_body: str, question: str) -> str:
        """Answer a lesson-scoped concept question with hints, not full solutions."""


# --- Prompt fragments ---------------------------------------------------------

_QUIZ_SYSTEM = (
    "You are a question author for an introductory programming course that uses "
    "PSEUDOCODE ONLY. Never produce runnable code in any real language and never "
    "ask the student to write compilable code. Allowed question types are exactly: "
    "'mcq' (multiple choice), 'predict_output' (read pseudocode, state the result), "
    "and 'pseudocode_order' (arrange shuffled pseudocode lines). Ground every "
    "question strictly in the supplied chapter content."
)

_GRADE_SYSTEM = (
    "You are a patient grader for a pseudocode-only programming course. You never "
    "execute code; you reason about the student's conceptual/pseudocode answer "
    "against the reference answer and rubric. You must classify the underlying "
    "misconception using ONLY the provided fixed taxonomy."
)

_TUTOR_SYSTEM = (
    "You are a warm, patient tutor for absolute beginners in an introductory "
    "PSEUDOCODE-ONLY programming course. Answer the student's question about the "
    "current lesson concisely (2–5 sentences), in plain language. Use hints and "
    "intuition; do NOT solve their exercises or hand over full answers. If the "
    "question is off-topic for this lesson, gently steer back. Use only simple "
    "pseudocode if you must show any."
)


def _extract_json(text: str) -> Any:
    """Best-effort: parse a JSON object/array, tolerating ```json fences."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()
    return json.loads(cleaned)


class AnthropicClient(LLMClient):
    """Claude-backed implementation. Imports the SDK lazily so the app boots
    (and the seeded-fallback path works) even if anthropic isn't installed yet."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.anthropic_api_key
        self.model = model or settings.anthropic_model
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        from anthropic import Anthropic  # lazy import

        self._client = Anthropic(api_key=self.api_key)

    def _complete(self, system: str, user: str, max_tokens: int = 1500) -> str:
        message = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        # Concatenate text blocks.
        return "".join(block.text for block in message.content if block.type == "text")

    def generate_quiz(
        self, concept: dict, chapter_body: str, student_mastery: float, num_questions: int = 4
    ) -> list[dict]:
        user = f"""Concept: {concept.get('name')}
Student current mastery (0-1): {student_mastery:.2f}

CHAPTER CONTENT (the only source of truth):
\"\"\"
{chapter_body}
\"\"\"

Write {num_questions} questions calibrated to the student's mastery (lower mastery
=> easier, more scaffolded). Mix the three allowed types.

Return JSON ONLY: a list of objects with this shape:
[
  {{
    "type": "mcq" | "predict_output" | "pseudocode_order",
    "difficulty": "easy" | "medium" | "hard",
    "prompt": "string",
    "options": ["..."] | null,          // choices for mcq; shuffled lines for pseudocode_order; null for predict_output
    "correct_answer": <string or list>, // mcq: the correct option; predict_output: expected output; pseudocode_order: lines in correct order
    "target_misconception": one of {MISCONCEPTION_LABELS} or null
  }}
]
No prose, no markdown — JSON only."""
        # Retry once on parse failure; caller handles the seeded fallback.
        last_error: Exception | None = None
        for _ in range(2):
            raw = self._complete(_QUIZ_SYSTEM, user, max_tokens=2500)
            try:
                data = _extract_json(raw)
                if isinstance(data, list) and data:
                    return data
            except Exception as exc:  # noqa: BLE001 - we want to retry on any parse issue
                last_error = exc
                logger.warning("Quiz JSON parse failed, retrying: %s", exc)
        raise ValueError(f"LLM quiz generation did not return valid JSON: {last_error}")

    def grade_and_classify(
        self, question: str, reference_answer: Any, student_answer: Any
    ) -> dict:
        user = f"""Allowed misconception labels (pick exactly one, or "none" if correct):
{json.dumps(MISCONCEPTION_LABELS)}

QUESTION:
{question}

REFERENCE ANSWER (rubric / ground truth):
{json.dumps(reference_answer)}

STUDENT ANSWER (pseudocode/conceptual — do NOT execute it):
{json.dumps(student_answer)}

Grade conceptually. Return JSON ONLY:
{{
  "is_correct": true | false,
  "score": 0.0-1.0,
  "misconception_label": one of the allowed labels,
  "explanation": "one or two sentences naming what went wrong, WITHOUT giving the full answer"
}}"""
        raw = self._complete(_GRADE_SYSTEM, user, max_tokens=600)
        data = _extract_json(raw)
        if not is_valid_label(data.get("misconception_label")):
            # Defensive: coerce an unknown label rather than trusting the model blindly.
            data["misconception_label"] = "none" if data.get("is_correct") else "algorithm_sequencing_error"
        return data

    def explain(self, misconception_label: str, concept: dict, student_answer: Any) -> str:
        user = f"""Concept: {concept.get('name')}
Student's misconception: {misconception_label}
Student's answer: {json.dumps(student_answer)}

Write a SHORT (2-4 sentence), encouraging, scaffolded explanation that helps the
student see their misconception and nudges them toward the right idea. Do NOT hand
over the full correct answer. Plain prose only."""
        return self._complete(_GRADE_SYSTEM, user, max_tokens=300).strip()

    def ask_tutor(self, concept: dict, chapter_body: str, question: str) -> str:
        user = f"""Lesson: {concept.get('name')}

LESSON CONTENT (your only source of truth):
\"\"\"
{chapter_body}
\"\"\"

Student's question: {question}

Answer it briefly, with hints — do not solve their exercises."""
        return self._complete(_TUTOR_SYSTEM, user, max_tokens=400).strip()


def get_llm_client() -> LLMClient:
    """Factory — the single place that decides which model backs the demo.

    TODO: when the self-hosted Qwen3.5-4B is ready, branch here on a config flag
    and return a QwenClient() instead. The rest of the app is unaffected.
    """
    return AnthropicClient()
