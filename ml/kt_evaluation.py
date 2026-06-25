"""Knowledge-tracing evaluation — baselines vs BKT, on a leakage-safe split.

This is the capstone's core ML evidence (CHANGES A1/A2/A3/A5). It answers the only
question that makes the model worth shipping: **does BKT beat a simple baseline at
predicting whether a learner gets their next attempt right?**

Pipeline (the methodology chain, stated plainly):
  acquire -> clean -> split BY STUDENT and time (no leakage) -> baselines -> fit BKT
  -> evaluate (AUC, recall on the costly class, calibration) -> learning curves.

Leakage control (Slide 10 / supervisor S6): students are split into disjoint train/test
groups, so a learner's future answers never inform the model that predicts them. Within a
test sequence, every prediction uses ONLY prior answers (seq_forward is a causal filter).

The baseline a model must beat (Slide 11): the strongest naive predictor here is the
learner's own running success rate — which is exactly the "advance at 80%" score gate.
If BKT can't beat that, we don't need BKT, and we'd say so.

Run:  ml/.venv/bin/python kt_evaluation.py
Out:  ml/figures/kt_results.json + kt_baseline_comparison.png + kt_learning_curve.png
      + kt_calibration.png ; and updated Bayesian params for api/app/bkt.py (printed).
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless: save figures, never open a window
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix, f1_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import GroupShuffleSplit

import kt_bkt

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "assistments_2009_corrected.csv"
FIG = HERE / "figures"
FIG.mkdir(exist_ok=True)

RNG_SEED = 42          # fixed so the split (and every number) is reproducible
TOP_SKILLS = 30        # most-practised skills, matching the original notebook scope
TEST_FRACTION = 0.25   # fraction of STUDENTS held out


# --- 1. Acquire + clean ------------------------------------------------------

def load_clean() -> pd.DataFrame:
    df = pd.read_csv(DATA, low_memory=False, encoding="latin-1")
    df = df[["user_id", "skill_id", "skill_name", "correct", "order_id", "opportunity"]].copy()
    df = df.dropna(subset=["skill_id", "correct", "order_id"])
    df = df[df["correct"].isin([0, 1])]
    df["skill_id"] = df["skill_id"].astype(int)
    df["user_id"] = df["user_id"].astype(int)
    df["correct"] = df["correct"].astype(int)
    # Keep the most-practised skills so per-skill BKT fits are well-conditioned.
    top = df["skill_id"].value_counts().nlargest(TOP_SKILLS).index
    df = df[df["skill_id"].isin(top)]
    # Time order within each student so "prior" really means earlier in time.
    df = df.sort_values(["user_id", "order_id"]).reset_index(drop=True)
    return df


# --- 2. Leakage-safe split (by student) --------------------------------------

def split_by_student(df: pd.DataFrame):
    gss = GroupShuffleSplit(n_splits=1, test_size=TEST_FRACTION, random_state=RNG_SEED)
    train_idx, test_idx = next(gss.split(df, groups=df["user_id"]))
    return df.iloc[train_idx].copy(), df.iloc[test_idx].copy()


def sequences(df: pd.DataFrame) -> dict[int, dict[int, list[int]]]:
    """{skill_id: {user_id: [0/1, ...] in time order}}."""
    out: dict[int, dict[int, list[int]]] = {}
    for (skill, user), g in df.groupby(["skill_id", "user_id"], sort=False):
        out.setdefault(skill, {})[user] = g["correct"].tolist()
    return out


# --- 3. Per-step predictions for every method (same test steps) ---------------

def _seq_features(seqs: dict) -> tuple[np.ndarray, np.ndarray]:
    """Per-step features [n_prior_in_skill, prior_success_rate] + targets, built by the
    SAME skill->user->step iteration used everywhere else (so rows stay aligned)."""
    X, y = [], []
    for users in seqs.values():
        for seq in users.values():
            rc, rn = 0, 0
            for c in seq:
                X.append([rn, rc / rn if rn else 0.5])
                y.append(c)
                rc += c
                rn += 1
    return np.asarray(X, dtype=float), np.asarray(y, dtype=int)


def collect_predictions(train: pd.DataFrame, test: pd.DataFrame):
    """Return (actuals, dict[name]->preds, bkt_params), all aligned across the SAME
    test steps. Every method is built in one iteration order to rule out misalignment."""
    train_seqs = sequences(train)
    test_seqs = sequences(test)

    base_rate = float(train["correct"].mean())
    skill_mean = train.groupby("skill_id")["correct"].mean().to_dict()

    # Fit BKT per skill on the TRAIN students only.
    bkt_params = {
        skill: kt_bkt.fit_skill(list(users.values()))
        for skill, users in train_seqs.items()
    }

    # Logistic-regression baseline: fit on train features (prior signal only).
    Xtr, ytr = _seq_features(train_seqs)
    logreg = LogisticRegression(max_iter=1000).fit(Xtr, ytr)

    actuals: list[int] = []
    preds = {"base_rate": [], "skill_mean": [], "student_running": [], "bkt": []}
    Xte: list[list[float]] = []

    for skill, users in test_seqs.items():
        params = bkt_params.get(skill)
        s_mean = skill_mean.get(skill, base_rate)
        for seq in users.values():
            # BKT causal per-step predictions (uses only prior answers).
            _, bkt_p = kt_bkt.seq_forward(params, seq) if params else (0, [s_mean] * len(seq))
            running_correct, running_n = 0, 0
            for i, c in enumerate(seq):
                actuals.append(c)
                preds["base_rate"].append(base_rate)
                preds["skill_mean"].append(s_mean)
                # student's running success rate over PRIOR steps (the score-gate proxy)
                preds["student_running"].append(running_correct / running_n if running_n else s_mean)
                preds["bkt"].append(bkt_p[i])
                Xte.append([running_n, running_correct / running_n if running_n else 0.5])
                running_correct += c
                running_n += 1

    actuals = np.asarray(actuals)
    preds = {k: np.asarray(v) for k, v in preds.items()}
    preds["logreg"] = logreg.predict_proba(np.asarray(Xte, dtype=float))[:, 1]
    return actuals, preds, bkt_params


# --- 4. Metrics --------------------------------------------------------------

def metrics(actuals, p) -> dict:
    auc = roc_auc_score(actuals, p)
    hard = (p >= 0.5).astype(int)
    return {
        "auc": round(float(auc), 4),
        "accuracy": round(float((hard == actuals).mean()), 4),
        "f1": round(float(f1_score(actuals, hard)), 4),
        # The costly error is a false "mastered" -> the student advances unprepared.
        # That is a wrong answer we predicted as correct -> recall on the INCORRECT class.
        "recall_incorrect": round(float(recall_score(actuals, hard, pos_label=0)), 4),
    }


# --- 5. Figures --------------------------------------------------------------

def fig_baseline_bar(results: dict):
    order = ["base_rate", "skill_mean", "student_running", "logreg", "bkt"]
    labels = ["base rate", "skill mean", "running avg\n(score gate)", "logistic reg", "BKT"]
    aucs = [results[k]["auc"] for k in order]
    colors = ["#cbd5e1"] * 4 + ["#4f46e5"]
    plt.figure(figsize=(7, 4))
    bars = plt.bar(labels, aucs, color=colors)
    plt.axhline(0.5, ls="--", c="#94a3b8", lw=1, label="chance (0.5)")
    plt.ylim(0.45, max(aucs) + 0.05)
    plt.ylabel("AUC (next-attempt correctness)")
    plt.title("Knowledge tracing vs. baselines — ASSISTments (leakage-safe split)")
    for b, a in zip(bars, aucs):
        plt.text(b.get_x() + b.get_width() / 2, a + 0.004, f"{a:.3f}", ha="center", fontsize=9)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "kt_baseline_comparison.png", dpi=140)
    plt.close()


def fig_learning_curve(df: pd.DataFrame, bkt_params: dict):
    """Empirical success rate vs practice opportunity — does success rise with practice?"""
    d = df[df["opportunity"].notna()].copy()
    d["opportunity"] = d["opportunity"].astype(int)
    d = d[d["opportunity"].between(1, 12)]
    emp = d.groupby("opportunity")["correct"].mean()
    plt.figure(figsize=(7, 4))
    plt.plot(emp.index, emp.values, "o-", color="#4f46e5", label="observed success rate")
    plt.xlabel("practice opportunity (n-th attempt on a skill)")
    plt.ylabel("P(correct)")
    plt.title("Learning curve — success rises with practice (ASSISTments)")
    plt.ylim(0, 1)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "kt_learning_curve.png", dpi=140)
    plt.close()
    return {int(k): round(float(v), 4) for k, v in emp.items()}


def fig_calibration(actuals, p):
    bins = np.linspace(0, 1, 11)
    idx = np.digitize(p, bins) - 1
    xs, ys = [], []
    for b in range(10):
        m = idx == b
        if m.sum() > 30:
            xs.append(p[m].mean())
            ys.append(actuals[m].mean())
    plt.figure(figsize=(5, 5))
    plt.plot([0, 1], [0, 1], "--", c="#94a3b8", label="perfect")
    plt.plot(xs, ys, "o-", c="#4f46e5", label="BKT")
    plt.xlabel("predicted P(correct)")
    plt.ylabel("observed frequency")
    plt.title("BKT calibration")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "kt_calibration.png", dpi=140)
    plt.close()


# --- main --------------------------------------------------------------------

def main():
    print("Loading + cleaning ASSISTments…")
    df = load_clean()
    train, test = split_by_student(df)
    n_tr_u, n_te_u = train["user_id"].nunique(), test["user_id"].nunique()
    assert set(train["user_id"]) & set(test["user_id"]) == set(), "LEAKAGE: student in both splits"
    print(f"  rows={len(df)}  skills={df['skill_id'].nunique()}  "
          f"train_students={n_tr_u}  test_students={n_te_u}  (disjoint ✓)")

    print("Fitting BKT per skill + collecting predictions…")
    actuals, preds, bkt_params = collect_predictions(train, test)
    results = {name: metrics(actuals, p) for name, p in preds.items()}

    # The honest verdict.
    best_baseline = max(["base_rate", "skill_mean", "student_running", "logreg"],
                        key=lambda k: results[k]["auc"])
    delta = results["bkt"]["auc"] - results[best_baseline]["auc"]

    print("Rendering figures…")
    fig_baseline_bar(results)
    curve = fig_learning_curve(df, bkt_params)
    fig_calibration(actuals, preds["bkt"])

    # Seed the LIVE gate (A4) with the MEDIAN of the per-skill MLE fits — robust to the
    # pooling degeneracy a single global fit suffers, and easy to defend ("median of the
    # per-skill maximum-likelihood fits on ASSISTments").
    per_skill = np.array(list(bkt_params.values()))  # (n_skills, 4)
    med = np.median(per_skill, axis=0)
    live = {"P_INIT": round(float(med[0]), 3), "P_LEARN": round(float(med[1]), 3),
            "P_SLIP": round(float(med[2]), 3), "P_GUESS": round(float(med[3]), 3)}

    out = {
        "dataset": "ASSISTments 2009 (corrected)",
        "split": "by student, time-ordered, disjoint (leakage-safe)",
        "n_test_predictions": int(len(actuals)),
        "results": results,
        "best_baseline": best_baseline,
        "bkt_minus_best_baseline_auc": round(float(delta), 4),
        "learning_curve_observed": curve,
        "fitted_live_bkt_params": live,
    }
    (FIG / "kt_results.json").write_text(json.dumps(out, indent=2))

    print("\n=== RESULTS (AUC) ===")
    for k in ["base_rate", "skill_mean", "student_running", "logreg", "bkt"]:
        print(f"  {k:16} AUC={results[k]['auc']:.4f}  "
              f"recall_incorrect={results[k]['recall_incorrect']:.3f}")
    print(f"\nBKT beats best baseline ({best_baseline}) by {delta:+.4f} AUC")
    print(f"Fitted live BKT params (for api/app/bkt.py): {live}")
    print(f"Saved: kt_results.json + 3 figures in {FIG}")


if __name__ == "__main__":
    main()
