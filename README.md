# Brainiacs AI

Adaptive tutoring for the **fundamentals of programming**. Brainiacs AI teaches a
strict prerequisite graph of concepts (algorithmic thinking → variables → control
flow → loops; variables → functions → recursion). A concept stays **locked** until
all its prerequisites are mastered. All learning content is human-authored — the AI
never generates teaching material.

The AI does exactly three things, on **pseudocode and conceptual answers only**
(no code editor, no compiler, no execution sandbox anywhere):

1. **Quiz generation** — a per-student quiz from the chapter content, so quizzes
   can't be memorised.
2. **Grading + misconception classification** — grades the answer and labels the
   underlying misconception from a fixed taxonomy.
3. **Explanation + gating** — explains the mistake; if mastery is below threshold,
   the student practises until ready to advance.

Mastery is tracked per concept per student with **Bayesian Knowledge Tracing**.

> 🚧 Initial software demo (ML-specialization capstone, African Leadership
> University). Repo link: _<add GitHub URL here>_

See the full setup, screenshots, deployment plan, and ML notebook summary below —
this README is expanded in the final section of the build. For now:

## Quick start

```bash
# 1. Backend
make api-install                 # creates api/.venv, installs deps
cp .env.example .env             # fill ANTHROPIC_API_KEY + DATABASE_URL
make migrate                     # alembic upgrade head
make seed                        # load concepts/chapters/exercises
make api                         # FastAPI at http://localhost:8000/docs

# 2. Frontend
make web-install
make web                         # Next.js at http://localhost:3000

# 3. ML notebook
make notebook                    # ml/brainiacs_misconception_classifier.ipynb
```

## Repository layout

```
brainiacs-ai/
├── api/   FastAPI + SQLAlchemy + Alembic (the AI loop, BKT, seed content)
├── web/   Next.js + Tailwind (dashboard, concept page, quiz page)
├── ml/    Jupyter notebook: misconception classifier with real metrics
└── docs/  deployment plan + app screenshots
```
