# Dataset landscape for Brainiacs AI (verified research, June 2026)

**Headline finding — say this to the board:** *No public dataset maps a
pseudocode/conceptual answer to a programming-misconception taxonomy.* This was
verified, not assumed. The pseudocode-only constraint plus a misconception target
is a genuine gap in available data — so building a small, documented labeled set is
a **legitimate contribution**, not a shortcut.

> ⚠️ License caveat: the candidates below were verified via search results. Before
> ingesting any dataset into the project, open the actual repo/rules page and
> confirm the license (especially McMining, SPRAG, and the Eedi competition terms).

## What exists, ranked by fit

| Dataset | Link | License | What it is | Serves | Fit /5 | The catch |
|---|---|---|---|---|---|---|
| **Eedi – Mining Misconceptions in Math (Kaggle 2024)** | [kaggle](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics) | Competition (non-commercial/research), **gated** (Kaggle login) | MCQ distractors each mapped to a named misconception | Grade+classify (design template) | 4 | It's **math**, not programming |
| **McMining / McMiner** (arXiv 2510.08827, Oct 2025) | [arxiv](https://arxiv.org/abs/2510.08827) · [repo](https://github.com/taisazero/mcminer) | Academic (verify repo) | 1,063 code samples ↔ 67 misconceptions | Misconception taxonomy + classification | 4 | Real **code**, not pseudocode; labels LLM-injected |
| **progmiscon.org** | [site](https://progmiscon.org/) · [JSON](https://progmiscon.org/share/) | Catalog, CC (verify) | Hundreds of misconception *descriptions* (Java/JS/Python) | **Taxonomy seed** for your 11 classes | 4 | A catalog, **not** labeled answers |
| **SPRAG** | [repo](https://github.com/sridevibonthu/SPRAG) | Public (verify Zenodo) | Python short-answer grading, annotated | Grading (ASAG) + feedback | 4 | No misconception taxonomy |
| **MMLU – CS subsets** | [HF cais/mmlu](https://huggingface.co/datasets/cais/mmlu) | **MIT**, ungated | ~474 CS MCQs (college/HS CS, ML, security) | Exercise-generation few-shots / eval | 3 | No misconception labels |
| **SemEval-2013 (Beetle+SciEntsBank)** ← *what we used* | [HF](https://huggingface.co/datasets/Atomi/semeval_2013_task_7_beetle_5way) | **CC-BY-SA** | ~13k short answers, 5-way correctness | Grading-pipeline validation | 3 | **Science**, not programming |
| Mohler/Texas ASAG (data structures) | via SemEval lineage | Research | 630 / 2,273 CS short answers + grades | ASAG in CS | 3 | Small, dated, request-only |
| Eedi NeurIPS 2020 (KT) | [arxiv](https://arxiv.org/abs/2007.12061) | Research, gated | 20M answer logs | Knowledge tracing | 2 | Answer logs, sparse misconception tags |
| CSEDM / ProgSnap2 / CodeWorkout | [csedm](https://sites.google.com/ncsu.edu/csedm-dc-2021/dataset) | Research | CS1 Java code process logs | Process mining | 2 | Real code, no misconception labels |
| CS1QA (KAIST) | [repo](https://github.com/cyoon47/cs1qa) | Research/request | 9,237 Python QA pairs | Q&A / feedback | 2 | Python, no taxonomy |
| **FCS1 / SCS1 / SCS2** concept inventories | [case study](https://dl.acm.org/doi/fullHtml/10.1145/3446871.3469744) | **Secured** | ~27 pseudocode-style MCQs; distractors embody misconceptions | Item-design inspiration | 1 (data), 2 (design) | **Deliberately withheld** to protect validity |
| BDSI | [LASSO](https://lassoeducation.org/basic-data-structures-inventory/) | Secured | Validated CS2 MCQ inventory | Design inspiration | 1 | Request-only |

## The three that actually matter for you

1. **progmiscon.org** — download the JSON; use it (with your Qian & Lehman 2017 base)
   to *justify and seed* your 11-class taxonomy. Citation for "where my labels come from."
2. **McMining** (arXiv 2510.08827) — the closest *programming* misconception work;
   cite it as prior art and a taxonomy cross-check. Confirms misconception
   classification is an active, real research problem (good for your defense).
3. **Eedi 2024** — the *design template*: MCQ distractor → named misconception. You
   mirror this structure with pseudocode items. (Math domain, so structure not content.)

Plus **MMLU-CS (MIT)** for grounding/evaluating exercise *generation*, and
**SemEval/SPRAG** as real-text sanity checks for the *grading* pipeline.

## Model recommendation (verified reasoning)

- **Misconception classification = 11-class text classification.** Smallest
  defensible model: **DistilBERT (66M)** or **RoBERTa-base (125M)** with a
  classification head. Trains in **5–20 min** for 3–4 epochs on a single GPU.
- **Generation/explanation** = where a small **Qwen (0.5B–1.5B, LoRA)** earns its
  keep as the self-hosted, low-cost, open model — benchmarked against a frontier API
  as the honesty baseline.
- **Cleanest architecture:** DistilBERT/RoBERTa classifier (the measurable ML
  contribution) **+** small fine-tuned Qwen generator (the open-model requirement)
  **+** frontier-API comparison.

## "If I only had 2 days" plan

1. Seed the 11-class taxonomy from progmiscon.org + McMining.
2. Generate ~1–2k pseudocode items (MCQ / predict-output / line-ordering) with a
   frontier LLM, distractors labeled to the 11 classes (Eedi-style).
3. Fine-tune **DistilBERT** (11-class) → report macro-F1 + confusion matrix.
4. LoRA fine-tune **Qwen2.5-0.5B/1.5B** on exercise/explanation pairs → benchmark vs API.
5. Defense line: *"No public pseudocode→misconception dataset exists (verified); I
   built one seeded from progmiscon + McMining, trained a 66M DistilBERT classifier
   and a small open Qwen generator, and benchmarked against a frontier API."*
