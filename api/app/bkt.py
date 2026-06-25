"""Bayesian Knowledge Tracing — a deliberately simple per-concept update.

Single source of truth for the mastery gate. BKT models P(mastered) as a hidden
state updated after each observed answer using four parameters:

    p_init  : prior P(knows the skill) before any evidence
    p_learn : P(transition unmastered -> mastered) after an attempt
    p_slip  : P(answers wrong | actually mastered)
    p_guess : P(answers right | not mastered)

The parameters are data-informed, not pulled from thin air — see the note below and
ml/kt_evaluation.py, where a fitted BKT beats the score-gate baseline (AUC 0.715 vs
0.696) on a leakage-safe split of ASSISTments.
"""
from __future__ import annotations

from dataclasses import dataclass

# --- Mastery gate constants (single source of truth) ---
MASTERY_THRESHOLD = 0.85
MIN_ATTEMPTS = 3

# --- BKT parameters ---
# Slip and guess (the observation-noise terms) are set to the MEDIAN of the per-concept
# maximum-likelihood fits on ASSISTments (ml/kt_evaluation.py); these transfer reasonably
# across domains. The prior and learn rate are NOT taken from ASSISTments: its learners
# are not absolute beginners (fitted prior ~0.70) and its cadence differs, so we keep a
# low beginner prior and a moderate learn rate suited to first-exposure pseudocode. Our
# own in-domain pilot is currently too small and skewed (n=61, ~90% correct from early
# testers) to fit a reliable prior; re-fitting all four from in-domain logs as the pilot
# grows is future work.
P_INIT = 0.20    # beginner prior: a first-time learner starts mostly unmastered
P_LEARN = 0.20   # moderate per-attempt learning, suited to the quiz cadence
P_SLIP = 0.22    # P(wrong | mastered) — ASSISTments per-concept MLE median
P_GUESS = 0.26   # P(right | not mastered) — ASSISTments per-concept MLE median


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
