# Brainiacs AI

An adaptive tutor for the **fundamentals of programming**, taught in pseudocode. It
follows a strict prerequisite graph of concepts — a concept stays **locked** until its
prerequisites are mastered — and uses **knowledge tracing** to estimate each learner's
per-concept mastery and decide when to advance them versus give more practice.

Fully **self-hosted**: deterministic grading, no external LLM, no third-party identity
provider — no learner data leaves the system.

- **Live:** https://brainiacs.bwenge.rw
- **Demo video:** _<add link>_

> ML-specialization capstone, African Leadership University.

## The ML contribution — knowledge tracing

The core machine learning is a **Bayesian Knowledge Tracing** model (a 2-state HMM:
hidden state = mastered / not-mastered; evidence = correct / incorrect; with guess, slip
and learn parameters). It estimates per-concept mastery from a learner's attempt history
and drives the unlock gate.

Evaluated on **ASSISTments 2009** (a public knowledge-tracing benchmark), on a
leakage-safe split (students disjoint between train/test, time-ordered) —
[`ml/kt_evaluation.py`](ml/kt_evaluation.py):

| Method | AUC |
|---|---:|
| base rate | 0.500 |
| per-skill mean | 0.608 |
| running average — the "advance at 80%" score gate | 0.696 |
| logistic regression | 0.698 |
| **BKT** | **0.715** |

**BKT beats the simple score-gate baseline** — the comparison that justifies using the
model. The learning curve ([`ml/figures/kt_learning_curve.png`](ml/figures/kt_learning_curve.png))
shows success rising with practice. ASSISTments is mathematics (out of domain), so it
validates the *method*; the in-domain evidence is the platform's own attempt logs (a
small, growing pilot).

> Future work: a fine-tuned small open-weights model for misconception classification and
> a frontier cost comparison — deferred because no public dataset maps pseudocode answers
> to misconceptions.

## Stack

- **api/** — FastAPI + SQLAlchemy + Alembic + PostgreSQL. Email/password JWT auth, the
  seeded exercise bank, deterministic grading, and the BKT mastery gate.
- **web/** — Next.js + Tailwind + NextAuth. Login, dashboard (concept map), lesson, quiz.
- **ml/** — `kt_evaluation.py` (baselines vs BKT + figures), `kt_bkt.py` (NumPy BKT).

## Run locally

Prerequisites: Python 3.11+, Node 20+, PostgreSQL 14+. No API keys needed — grading is
deterministic and quizzes come from the seeded bank.

```bash
# 1. Database
psql -d postgres -c "CREATE ROLE brainiacs LOGIN PASSWORD 'brainiacs';"
psql -d postgres -c "CREATE DATABASE brainiacs OWNER brainiacs;"

# 2. Backend  ->  http://localhost:8000  (Swagger UI at /docs)
cp .env.example .env
make api-install && make migrate && make seed && make api

# 3. Frontend ->  http://localhost:3000
make web-install && make web
```

## Reproduce the ML evaluation

```bash
cd ml && python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt
bash download_data.sh                 # fetch ASSISTments (gitignored, not re-hosted)
.venv/bin/python kt_evaluation.py     # baseline vs BKT table + figures in ml/figures/
```

## Deploy

Docker Compose (`db` + `api` + `web`) behind host **nginx**, on a StrangeCloud VM, with
**push-to-deploy** CI/CD (`.github/workflows/deploy.yml`). Full runbook:
**[DEPLOY.md](DEPLOY.md)**.
