# Dataset & Model Research Brief — Brainiacs AI capstone

> Paste this into a deep-research agent (Claude, Gemini, or Perplexity) — or have
> the in-repo assistant run it. Goal: find **real, usable datasets** to defend the
> ML claims of a pseudocode-only programming tutor, and decide what to fine-tune.

## Context (read first)

I am building **Brainiacs AI**, an adaptive tutor for the **fundamentals of
programming**. Hard constraints:

- **Pseudocode only.** Students never write runnable/compilable code. There is no
  compiler, editor, or execution sandbox. Answers are conceptual: multiple-choice,
  predict-the-output (reading pseudocode), and pseudocode-ordering.
- The AI does exactly three jobs:
  1. **Generate exercises** from human-authored chapter content + what the student
     has covered so far (so quizzes can't be memorised).
  2. **Grade + classify the misconception** behind a wrong answer, using a FIXED
     taxonomy (variable_name_semantics, assignment_as_equality,
     loop_boundary_offbyone, loop_execution_model, scope_confusion,
     recursion_no_base_case, recursion_state_confusion,
     array_index_value_confusion, boolean_logic_error,
     algorithm_sequencing_error, none). Grounded in Qian & Lehman (2017).
  3. **Explain** the mistake (scaffolded, no full answer) and **gate** progress with
     Bayesian Knowledge Tracing thresholds.
- Proposal commitment: **fine-tune a small open model (Qwen family)**. I must be able
  to defend "what model did I train and why" to a capstone board.

The dataset I used so far (SciEntsBank / SemEval-2013) is **science short-answers,
not programming** — it only validates the classification pipeline, not the domain.
I need better-fitting data.

## What I need you to find

For EACH of the four needs below, find concrete datasets/resources. For every
candidate, return a row with: **name · direct link · license · size · format/labels ·
which AI job it serves · publicly downloadable? (yes / gated / on-request) · fit
verdict (1–5) · 1-line why**.

1. **Programming misconception data** — datasets where novice answers/programs are
   labelled with *conceptual misconceptions* (not just pass/fail). Especially
   anything **language-independent / pseudocode / concept-level** rather than tied to
   one language's syntax. Check these candidates and find more:
   - Progmiscon.org (programming misconceptions inventory)
   - Qian & Lehman (2017) survey and any released artifacts
   - FCS1 / SCS1 / SCS2 CS concept inventories (Tew & Guzdial; Parker et al.) — are
     the items or response data publicly available, or access-restricted?
   - BDSI (Basic Data Structures Inventory)
2. **Misconception-tagged multiple-choice data** (methodology analogue for job 2):
   - Eedi "Mining Misconceptions in Mathematics" (Kaggle / NeurIPS 2020 Education
     Challenge) — MCQ wrong-answers tagged with misconceptions. Math, not code, but
     same task shape. License + usability?
   - Any CS/programming MCQ banks with distractor rationales.
3. **CS question / exercise generation grounding** (job 1):
   - MMLU computer-science subsets (cais/mmlu, MIT) — usable as a CS MCQ bank?
   - CS1QA (KAIST) — student questions + answers from an intro Python course.
   - Any "generate a question from a passage" CS datasets, or CS exam-question banks
     with open licenses.
4. **Real novice-programming process datasets** (for future pilot-data realism, even
   if code-based):
   - CSEDM / ProgSnap2, CodeWorkout, BlueJ Blackbox/Falcon, Code.org "Hour of Code"
     (Piech et al. program embeddings), ITAP/iSnap. Note license + whether
     misconception or just correctness labels.

## Hard requirements / filters

- **License must allow research + a class demo** (CC-BY, MIT, Apache, or clearly
  permissive). Flag anything non-commercial-only or gated.
- **Do not invent datasets.** If you're unsure a dataset exists or is downloadable,
  say so and give the closest verified alternative.
- Prefer datasets I can **load at runtime** (Hugging Face Hub, Kaggle, GitHub
  release) — I will not re-host raw third-party data.
- Note the **catch** for each: e.g., concept inventories are often kept secure to
  protect validity; large process datasets are code-based not pseudocode.

## Also answer these decision questions

A. Given the pseudocode-only constraint, is there **any** dataset that directly
   matches "pseudocode answer → programming misconception"? If not, state it plainly.
B. For the **discriminative** task (misconception classification), recommend the
   smallest defensible model to **fine-tune** (e.g., DistilBERT/RoBERTa vs a small
   Qwen), with rough compute/time on a free Colab/Kaggle GPU.
C. For the **generative** tasks (exercise generation, explanation), is fine-tuning a
   small Qwen justified vs. using a frontier API behind an abstraction? What minimal
   fine-tune would still let me honestly claim "I fine-tuned Qwen"?
D. Propose a **data-bootstrapping plan** to reach a fine-tunable set: synthetic
   generation (LLM "answer as a novice who believes X"), augmentation volume, and how
   to add real pilot data + inter-annotator agreement (Cohen's κ) for validity.
E. Give me a **3-sentence defense script** I can say to the board for "what model did
   you train and why," that is honest about synthetic-data limitations.

## Output format

A ranked shortlist (best-fit first) as a markdown table, then the answers to A–E,
then a "if I only had 2 days" recommendation.
