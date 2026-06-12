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
bash download_data.sh         # fetch ASSISTments + Mohler (gitignored, not re-hosted)
make notebook                 # opens ml/kt_knowledge_tracing_assistments.ipynb
```

The knowledge-tracing and grading notebooks run **top-to-bottom with no API key**
(BKT is pure NumPy; DKT uses PyTorch; grading uses scikit-learn). Datasets are loaded
locally via `download_data.sh`.

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

## ML contribution — Knowledge Tracing

The core machine-learning contribution is a **knowledge-tracing** model that
*remembers each learner and tracks mastery per concept* — the signal that drives the
strict prerequisite unlock map, and the fix for the **statelessness gap** in existing
tutors (CS50.ai, CodeHelp, plain ChatGPT). It is built and validated on **real,
public data**.

> Why knowledge tracing and not a misconception classifier? Research confirmed there
> is **no public dataset** mapping pseudocode/conceptual answers to programming
> misconceptions (see [`docs/dataset-landscape.md`](docs/dataset-landscape.md)).
> Rather than train on fabricated data, the ML contribution is knowledge tracing —
> real data, established models. Misconception labelling remains a **product
> feature**, produced by the LLM at inference time, not by a trained model.

### 1. Knowledge tracing — [`ml/kt_knowledge_tracing_assistments.ipynb`](ml/kt_knowledge_tracing_assistments.ipynb)

Trained on **ASSISTments 2009–2010 (corrected)** — ~283k cleaned interactions, 4,163
students. Next-question-correctness **AUC** on an unseen-students split:

| Model | AUC | Accuracy | Notes |
|-------|----:|---------:|-------|
| **BKT** (our NumPy implementation, `ml/kt_bkt.py`) | **0.714** | 0.718 | interpretable; its per-skill mastery probability drives the 0.85 unlock gate |
| **DKT** (LSTM, PyTorch) | **0.755** | 0.736 | the deep model edges out BKT, as expected |

Both land in the published ASSISTments range (BKT ≈ 0.73–0.76). The mastery
trajectory ([`ml/figures/kt_mastery_trajectory.png`](ml/figures/kt_mastery_trajectory.png))
shows P(mastered) crossing the unlock threshold — exactly how the product gates progress.
*Dataset: cite the dataset URL + Feng, Heffernan & Koedinger (2009); no formal license.*

### 2. Automatic grading demo — [`ml/grading_mohler.ipynb`](ml/grading_mohler.ipynb)

On the **Mohler / UNT CS short-answer dataset** (2,273 real answers, graded 0–5), a
TF-IDF + SVR baseline predicts human grades at **Pearson ≈ 0.54 / RMSE ≈ 0.94**
(published baselines ~0.63 / ~0.91 use heavier embeddings). This *demonstrates ML
grading on real CS data* and benchmarks the production LLM grader. *Dataset: GPL; cite
Mohler, Bunescu & Mihalcea (2011).*

### How the ML fits the product

```
BRAINIACS AI
├─ KNOWLEDGE TRACING (BKT + DKT)  ← core ML; tracks mastery → drives concept unlock
├─ LLM behind LLMClient           → generates exercises, grades, labels misconceptions
│     ↑ Mohler dataset benchmarks the grading capability
└─ platform logs every interaction → its own dataset over time (future work)
```

**One-sentence defense:** *"My ML contribution is a stateful knowledge-tracing model —
built and validated on ASSISTments — that fixes the statelessness gap in existing
tutors; I use an LLM for generation and grading because re-training those is wasteful,
and I demonstrate grading on the Mohler CS dataset. There's no public pseudocode→
misconception dataset, so I track mastery on real data and let the platform collect its
own interactions for future work."*

> Optional/stretch (honoring the original proposal's Qwen fine-tune): a small QLoRA
> adapter on Qwen for *exercise generation*, kept only if time allows; production
> generation otherwise wraps a frontier LLM behind `LLMClient`.

Figures are saved under [`ml/figures/`](ml/figures/). An earlier misconception-
classification exploration (now superseded) lives in
[`ml/exploratory/`](ml/exploratory/).

### Misconception taxonomy (product feature, applied by the LLM)

`variable_name_semantics`, `assignment_as_equality`, `loop_boundary_offbyone`,
`loop_execution_model`, `scope_confusion`, `recursion_no_base_case`,
`recursion_state_confusion`, `array_index_value_confusion`, `boolean_logic_error`,
`algorithm_sequencing_error`, `none` — grounded in Qian & Lehman (2017), used by the
LLM grader at inference time (not a trained classifier).
