# Exploratory (superseded) — misconception classification

`brainiacs_misconception_classifier.ipynb` was an **earlier exploration**: validating
a text-classification pipeline on the public SciEntsBank dataset and a small synthetic
seed set tagged with the misconception taxonomy.

**Why it's here and not the headline.** Research confirmed there is **no public dataset
that maps pseudocode/conceptual answers to programming misconceptions** (see
`docs/dataset-landscape.md`). Training a misconception classifier would have rested on
fabricated data. So the ML contribution was **deliberately moved** to **knowledge
tracing** (real data, established models) — see the primary notebooks in `ml/`:

- `kt_knowledge_tracing_assistments.ipynb` — BKT vs DKT on ASSISTments (the core ML)
- `grading_mohler.ipynb` — automatic grading on the Mohler CS dataset

Misconception labelling is still a **product feature** — produced by the LLM at
inference time (behind `LLMClient`), not by a trained model. This notebook is kept as
honest evidence of the exploration that motivated the pivot.
