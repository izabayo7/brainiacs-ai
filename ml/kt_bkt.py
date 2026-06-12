"""Bayesian Knowledge Tracing — a small, self-contained NumPy implementation.

Standard 2-state HMM BKT (Corbett & Anderson 1995) with four parameters per skill:

    p_L0 : P(skill already known before the first opportunity)   -- prior
    p_T  : P(not-known -> known) after an opportunity            -- learn / transit
    p_S  : P(answer wrong | known)                               -- slip
    p_G  : P(answer right | not known)                           -- guess

Slip and guess are bounded <= 0.30 (Baker et al.'s "no conceptual swap" constraint)
to avoid the well-known BKT identifiability degeneracy. Parameters are fit per skill
by maximum likelihood (L-BFGS-B) on the training students' answer sequences; the same
forward recursion produces the next-step P(correct) used for AUC on held-out students.

This is deliberately our own implementation (pyBKT's C++ wheel doesn't build on
current Python), which also means we can explain every line at the defense.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

EPS = 1e-6


def _clip(p: float) -> float:
    return min(max(p, EPS), 1.0 - EPS)


def seq_forward(params, seq):
    """One forward pass over a 0/1 answer sequence.

    Returns (log_likelihood, predicted_p_correct_per_step). The prediction at step n
    uses only information BEFORE observing step n's answer — the honest KT target.
    """
    p_L0, p_T, p_S, p_G = params
    p_known = p_L0
    log_lik = 0.0
    preds = []
    for c in seq:
        p_correct = _clip(p_known * (1.0 - p_S) + (1.0 - p_known) * p_G)
        preds.append(p_correct)
        log_lik += np.log(p_correct) if c == 1 else np.log(1.0 - p_correct)

        # Posterior P(known | this answer).
        if c == 1:
            num = p_known * (1.0 - p_S)
            den = p_known * (1.0 - p_S) + (1.0 - p_known) * p_G
        else:
            num = p_known * p_S
            den = p_known * p_S + (1.0 - p_known) * (1.0 - p_G)
        p_known_post = num / den if den > 0 else p_known

        # Learning transition for the next opportunity.
        p_known = p_known_post + (1.0 - p_known_post) * p_T
    return log_lik, preds


def _neg_log_lik(params, seqs):
    return -sum(seq_forward(params, s)[0] for s in seqs)


def fit_skill(seqs, x0=(0.20, 0.15, 0.10, 0.20)):
    """Fit (p_L0, p_T, p_S, p_G) for one skill by MLE."""
    bounds = [(0.01, 0.99), (0.01, 0.99), (0.01, 0.30), (0.01, 0.30)]
    res = minimize(
        _neg_log_lik, x0, args=(seqs,), method="L-BFGS-B",
        bounds=bounds, options={"maxiter": 100},
    )
    return tuple(res.x)


def predict_sequences(params, seqs):
    """Flatten per-step predictions + actuals across sequences (for AUC)."""
    preds, actuals = [], []
    for s in seqs:
        _, p = seq_forward(params, s)
        preds.extend(p)
        actuals.extend(s)
    return np.asarray(preds), np.asarray(actuals)


def mastery_trajectory(params, seq):
    """P(known) AFTER each answer — the mastery curve shown to drive the unlock gate."""
    p_L0, p_T, p_S, p_G = params
    p_known = p_L0
    traj = []
    for c in seq:
        if c == 1:
            num = p_known * (1.0 - p_S)
            den = p_known * (1.0 - p_S) + (1.0 - p_known) * p_G
        else:
            num = p_known * p_S
            den = p_known * p_S + (1.0 - p_known) * (1.0 - p_G)
        p_known_post = num / den if den > 0 else p_known
        traj.append(p_known_post)
        p_known = p_known_post + (1.0 - p_known_post) * p_T
    return traj
