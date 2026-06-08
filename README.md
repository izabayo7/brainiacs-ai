# Brainiacs AI

**Brainiacs AI is an adaptive tutor for the fundamentals of programming.** It teaches
a strict prerequisite graph of concepts (algorithmic thinking → variables → control
flow → loops; variables → functions → recursion); a concept stays **locked** until
all its prerequisites are mastered. All learning content is human-authored — the AI
never writes teaching material. Students work in **pseudocode and conceptual answers
only** (there is no code editor, compiler, or execution sandbox anywhere). The AI
does exactly three things: **(1) generate** a per-student quiz from the chapter so
quizzes can't be memorised, **(2) grade and classify** the underlying misconception
from a fixed taxonomy, and **(3) explain** the mistake and **gate** progress —
mastery is tracked per concept with **Bayesian Knowledge Tracing**, and below
threshold the student practises until ready to advance.

> Initial software demo — ML-specialization capstone, African Leadership University.

## Repository

**GitHub:** https://github.com/izabayo7/brainiacs-ai

```
brainiacs-ai/
├── api/    FastAPI + SQLAlchemy + Alembic — the AI loop, BKT, seed content
├── web/    Next.js + Tailwind — dashboard, concept page, quiz page
├── ml/     Jupyter notebook — misconception classifier with real metrics
└── docs/   deployment plan + app screenshots
```

## Set up and run

**Prerequisites:** Python 3.11+, Node 18+, PostgreSQL 14+.

### 1. Database (PostgreSQL)

```bash
# Create the role and database the demo expects:
psql -d postgres -c "CREATE ROLE brainiacs LOGIN PASSWORD 'brainiacs';"
psql -d postgres -c "CREATE DATABASE brainiacs OWNER brainiacs;"
```

### 2. Backend (FastAPI)

```bash
cp .env.example .env          # then edit .env:
#   DATABASE_URL=postgresql+psycopg://brainiacs:brainiacs@localhost:5432/brainiacs
#   ANTHROPIC_API_KEY=...     # OPTIONAL — see note below

make api-install              # creates api/.venv, installs requirements
make migrate                  # alembic upgrade head
make seed                     # load concepts / chapters / exercises / students
make api                      # uvicorn at http://localhost:8000  (Swagger UI at /docs)
```

> **No API key? The demo still runs.** Without `ANTHROPIC_API_KEY`, quiz generation
> falls back to the pre-seeded exercises and grading uses a deterministic offline
> grader (it compares against the reference answer and attributes the exercise's
> authored misconception). With a key, the same endpoints use Claude for
> generation, grading, classification, and explanations. The swap is behind the
> `LLMClient` seam in [`api/app/llm.py`](api/app/llm.py).

### 3. Frontend (Next.js)

```bash
make web-install              # npm install in web/
# optional: cp web/.env.local.example web/.env.local   (defaults to localhost:8000)
make web                      # Next.js at http://localhost:3000
```

### 4. ML notebook

```bash
cd ml && python3 -m venv .venv && .venv/bin/python -m pip install --requirement requirements.txt
make notebook                 # opens ml/brainiacs_misconception_classifier.ipynb
```

The notebook runs **top-to-bottom without any API key** (the public-data validation
and the seed-set baseline are API-free; the two Anthropic-API cells are clearly
marked and optional).

## Navigation & layout (three screens)

- **Dashboard (`/`)** — student picker (no auth in the demo), a "Continue → next
  concept" panel, and the concept map showing each concept as LOCKED / AVAILABLE /
  MASTERED with a calm mastery meter.
- **Concept (`/concept/[id]`)** — the human-authored chapter (markdown + worked
  pseudocode example) and "Start quiz". Locked concepts are unreachable (403).
- **Quiz (`/quiz/[conceptId]`)** — an AI-generated (or seeded) quiz across the three
  pseudocode-safe types: multiple-choice, predict-the-output, and pseudocode-
  ordering. On submit it shows the per-question grade, the named misconception, a
  scaffolded explanation, and an updated mastery meter — then either "practise
  again" or what just unlocked.

## Designs

A polished **Figma** is in progress (separate from this build); the current UI is
clean, neutral, and functional by design. App screenshots live in
[`docs/screenshots/`](docs/screenshots/) — see that folder's README for the three
shots to capture.

<!-- Once captured:
![Dashboard](docs/screenshots/dashboard.png)
![Concept page](docs/screenshots/concept.png)
![Quiz with feedback](docs/screenshots/quiz.png)
-->

## Deployment plan

Target is **Docker + Nginx on a cloud.strettch.com VM** with PostgreSQL, and a
production path that replaces the Anthropic API with a self-hosted **fine-tuned
Qwen3.5-4B** behind the same `LLMClient` interface. Full details:
[`docs/deployment-plan.md`](docs/deployment-plan.md).

## ML notebook summary

[`ml/brainiacs_misconception_classifier.ipynb`](ml/brainiacs_misconception_classifier.ipynb)
builds the misconception classifier that powers grading, and reports **real metrics**:

- **Pipeline validation on public data (SciEntsBank, unseen-answers split).** A
  TF-IDF → classifier pipeline on a 5-way misconception-style target, with full
  precision / recall / F1 and a confusion matrix. Initial results (macro-averaged):

  | Model | Accuracy | Precision | Recall | **F1** |
  |-------|---------:|----------:|-------:|------:|
  | TF-IDF + LinearSVC | 0.56 | 0.42 | 0.40 | 0.40 |
  | TF-IDF + LogisticRegression | 0.46 | 0.37 | 0.39 | 0.37 |
  | **TF-IDF + XGBoost** | **0.59** | **0.48** | **0.44** | **0.45** |

- **Initial baseline for our own task.** On a small, honestly-labelled **synthetic
  seed set** (43 rows) of pseudocode answers tagged with the fixed misconception
  taxonomy, a TF-IDF + SVM baseline reaches **macro-F1 ≈ 0.26** on a held-out split.
  This is a deliberate floor on synthetic data, not a production claim.

- **Limitations & next step.** The seed set is synthetic and small (no
  inter-annotator agreement yet). Next: collect real pilot data, measure **Cohen's
  κ**, expand the seed set via the Anthropic-API generation cell, then **fine-tune
  Qwen3.5-4B** and benchmark it in the notebook's LLM-as-classifier slot.
  **Target: macro-F1 ≥ 0.80.**

Figures are saved under [`ml/figures/`](ml/figures/).

### Misconception taxonomy (fixed)

`variable_name_semantics`, `assignment_as_equality`, `loop_boundary_offbyone`,
`loop_execution_model`, `scope_confusion`, `recursion_no_base_case`,
`recursion_state_confusion`, `array_index_value_confusion`, `boolean_logic_error`,
`algorithm_sequencing_error`, `none` — grounded in Qian & Lehman (2017) and shared
verbatim by the API and the notebook.
