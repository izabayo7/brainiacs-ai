"""Bayesian Knowledge Tracing — a deliberately simple per-concept update.

Single source of truth for the mastery gate. BKT models P(mastered) as a hidden
state updated after each observed answer using four parameters:

    p_init  : prior P(knows the skill) before any evidence
    p_learn : P(transition unmastered -> mastered) after an attempt
    p_slip  : P(answers wrong | actually mastered)
    p_guess : P(answers right | not mastered)

For this demo the standard textbook BKT equations are plenty — no RL, no tuning.
"""
from __future__ import annotations

from dataclasses import dataclass

# --- Mastery gate constants (single source of truth) ---
MASTERY_THRESHOLD = 0.85
MIN_ATTEMPTS = 3

# --- BKT parameters (reasonable defaults; could be fit per concept later) ---
P_INIT = 0.20
P_LEARN = 0.20
P_SLIP = 0.10
P_GUESS = 0.20


@dataclass
class BktResult:
    p_mastered: float
    attempts: int


def update_mastery(prior_p: float, attempts: int, is_correct: bool) -> BktResult:
    """Run one BKT step.

    `prior_p` is the previous P(mastered) (use P_INIT for a fresh concept).
    Returns the posterior after observing this answer plus the learning transition.
    """
    if attempts == 0:
        prior_p = P_INIT

    # Bayes update of the *current* belief given the observed correctness.
    if is_correct:
        numerator = prior_p * (1.0 - P_SLIP)
        denominator = prior_p * (1.0 - P_SLIP) + (1.0 - prior_p) * P_GUESS
    else:
        numerator = prior_p * P_SLIP
        denominator = prior_p * P_SLIP + (1.0 - prior_p) * (1.0 - P_GUESS)

    posterior = numerator / denominator if denominator > 0 else prior_p

    # Account for learning that happens by doing the exercise.
    p_mastered = posterior + (1.0 - posterior) * P_LEARN

    return BktResult(p_mastered=round(p_mastered, 4), attempts=attempts + 1)


def is_mastered(p_mastered: float, attempts: int) -> bool:
    """The §4 gate: mastered iff confident enough AND enough evidence."""
    return p_mastered >= MASTERY_THRESHOLD and attempts >= MIN_ATTEMPTS
