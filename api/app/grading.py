"""Deterministic offline grader for SEEDED exercises.

The production grading path is the LLM (see llm.py). But the demo must run with no
ANTHROPIC_API_KEY: a reviewer clones, seeds, and clicks through without a key. For
seeded exercises we already hold the reference answer, so we can grade by direct
comparison and attribute the exercise's pre-authored target misconception when the
answer is wrong. This keeps the video deterministic too.

This still NEVER executes student code — it only compares answers.
"""
from __future__ import annotations

import re


def _norm(value: object) -> str:
    return re.sub(r"\s+", " ", str(value).strip().lower())


def _matches(reference: object, student: object) -> bool:
    # Ordering questions: compare the sequence element-by-element.
    if isinstance(reference, list):
        if not isinstance(student, list) or len(reference) != len(student):
            return False
        return all(_norm(a) == _norm(b) for a, b in zip(reference, student))
    return _norm(reference) == _norm(student)


def offline_grade_and_classify(
    reference: object, student_answer: object, target_misconception: str | None
) -> dict:
    is_correct = _matches(reference, student_answer)
    if is_correct:
        return {
            "is_correct": True,
            "score": 1.0,
            "misconception_label": "none",
            "explanation": "Correct — well reasoned.",
        }
    return {
        "is_correct": False,
        "score": 0.0,
        # Fall back to a sequencing error if the exercise didn't name a misconception.
        "misconception_label": target_misconception or "algorithm_sequencing_error",
        "explanation": "",  # filled by offline_explain()
    }


_SCAFFOLDS = {
    "variable_name_semantics": "Remember: the computer doesn't read meaning from a variable's name — only its stored value matters.",
    "assignment_as_equality": "Re-read assignment as 'store into', not 'is equal to'. The left side gets a new value.",
    "loop_boundary_offbyone": "Count the iterations carefully, including the very first and the very last one.",
    "loop_execution_model": "The loop body runs once per iteration, in sequence — not all at once.",
    "scope_confusion": "Think about where the variable lives: a variable made inside a function is local to it.",
    "recursion_no_base_case": "Every recursion needs a base case — a condition that stops it from calling itself.",
    "recursion_state_confusion": "Trace each recursive call and how its result feeds back into the caller.",
    "array_index_value_confusion": "Separate the index (the position) from the value stored at that position.",
    "boolean_logic_error": "Check each part of the condition and how AND / OR combine them.",
    "algorithm_sequencing_error": "Look again at the order of the steps — does each step have what it needs by the time it runs?",
    "none": "Almost — compare your answer carefully against the reference.",
}


def offline_explain(misconception_label: str, concept_name: str) -> str:
    tip = _SCAFFOLDS.get(misconception_label, _SCAFFOLDS["none"])
    return f"For {concept_name}: {tip} Try once more."
