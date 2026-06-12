# Presentation guide — Brainiacs AI ML notebooks

Everything you need to walk through the notebooks confidently and answer questions.
Read the "Big picture" and "Must-know numbers" first; the rest is reference.

---

## 0. The 20-second pitch (say this first)

> "Brainiacs AI is a pseudocode-only programming tutor. My machine-learning
> contribution is **knowledge tracing** — a model that tracks how much each student
> has mastered each concept, so the app can unlock the next concept only when they're
> ready. I built and validated it on real data (ASSISTments), comparing a classic
> model (BKT) against a deep-learning model (DKT)."

---

## 1. The big picture (the "why")

**The problem the product solves:** existing AI tutors (CS50.ai, ChatGPT) are
*stateless* — they forget the learner between sessions. Brainiacs AI **remembers each
learner and adapts**. The model that makes that possible is **knowledge tracing**.

**Why knowledge tracing is the ML contribution (and not "misconception classification"):**
My proposal originally mentioned classifying misconceptions. But research showed there
is **no public dataset** that maps pseudocode answers to programming misconceptions —
training that would mean inventing fake data. So I made the honest, stronger choice:
**knowledge tracing**, which has large real datasets and well-established models, and
which is exactly what fixes the statelessness gap. (Misconception *labels* are still a
product feature — produced by the LLM at answer time, not a trained model.)

**The three ML jobs and how each is handled:**
1. **Track the learner (mastery over time)** → *this is my trained ML* — BKT + DKT.
2. **Generate exercises + grade answers** → a frontier LLM behind an interface
   (re-training generation is wasteful); I *demonstrate* grading on the Mohler CS
   dataset as a benchmark.
3. **The platform logs every interaction** → becomes my own dataset over time.

---

## 2. Must-know numbers (memorise these)

**Knowledge tracing (notebook 1), on ASSISTments, evaluated on unseen students:**

| Model | AUC | Accuracy | Precision | Recall | F1 |
|-------|----:|---------:|----------:|-------:|---:|
| **BKT** | 0.714 | 0.718 | 0.741 | 0.883 | 0.806 |
| **DKT** | 0.755 | 0.736 | 0.752 | 0.890 | 0.815 |

- Published ASSISTments BKT AUC is ~0.73–0.76, so **my numbers are in the right range**
  — that's the sanity check.
- **DKT slightly beats BKT** (0.755 vs 0.714) — expected: the deep model captures more.
- Data: **346,860 raw rows → 283,105 after cleaning**, **4,163 students**, top-30 skills
  cover **~68%** of interactions, **~38,000 held-out predictions**.

**Grading (notebook 2), on the Mohler CS dataset:**
- **2,273** real student answers, graded 0–5 by humans.
- TF-IDF + SVR: **Pearson 0.54, RMSE 0.94** (published baselines ~0.63 / ~0.91 with
  heavier embeddings — so mine is a solid, honest baseline).

---

## 3. Concept cheat-sheet (explain these in one breath each)

- **Knowledge tracing (KT):** estimate a student's hidden "mastery" of a skill from their
  past answers, and predict whether they'll get the *next* question right.
- **BKT (Bayesian Knowledge Tracing):** a simple, *interpretable* model. It treats
  mastery as a hidden true/false state and updates the probability you've mastered a
  skill after each answer, using **four numbers per skill**:
  - **prior (p_L0)** — chance you already knew it before starting.
  - **learn (p_T)** — chance you learn it after one practice attempt.
  - **slip (p_S)** — chance you slip and answer wrong even though you know it.
  - **guess (p_G)** — chance you guess right even though you don't know it.
- **DKT (Deep Knowledge Tracing):** a neural network (an **LSTM** — a sequence model
  with memory) that reads the student's whole history and predicts the next answer. It
  learns patterns *across* skills automatically; no per-skill parameters.
- **AUC (0.5–1.0):** probability the model ranks a random correct answer above a random
  wrong one. 0.5 = guessing, 1.0 = perfect. **We use it because the data is imbalanced**
  (~two-thirds of answers are correct), so plain accuracy can be misleading.
- **Precision / Recall / F1:** treat "will get it right" as a yes/no prediction at 0.5.
  Recall is high (~0.88) because most answers are correct and the model catches them;
  precision (~0.75) is a bit lower; F1 (~0.81) balances the two.
- **Why split by student (not by row):** so the *same* student never appears in both
  train and test. That tests whether the model generalises to **new learners**, not
  whether it memorised known ones. (This is how we avoid data leakage.)

---

## 4. Notebook 1 walkthrough — `kt_knowledge_tracing_assistments.ipynb`

Go cell by cell. For each, here's *what it does* and *what to say*.

**A. Framing (markdown).**
Say: "This sets up the problem — knowledge tracing is the model behind the unlock map,
and here's the dataset, ASSISTments, with its citation."

**Imports cell.**
Say: "Standard stack — pandas, scikit-learn for metrics, and `kt_bkt`, my own BKT
implementation."

**B. Load & data engineering.**
What it does: reads the **corrected** ASSISTments CSV, keeps the relevant columns, drops
rows with no skill or non-binary correctness, sorts chronologically by `order_id`.
Say: "I use the *corrected* file on purpose — the original has duplicate rows that
inflate scores by ~25%. After cleaning I have 283,000 interactions from 4,163 students.
Sorting by order matters because knowledge tracing is sequential."

**C. Visualization (two cells).**
1. Top-15 skills bar + sequence-length histogram.
2. **The learning curve** — average correctness vs practice-opportunity number.
Say: "The learning curve is the key one: accuracy *rises* as students get more practice
on a skill. That upward trend is exactly the learning that a knowledge-tracing model has
to capture."

**D. BKT (three cells).**
1. Pick top-30 skills (~68% of data), split students 80/20, fit the 4 BKT parameters per
   skill by maximum likelihood, evaluate next-step prediction on held-out students.
2. Print a table of fitted parameters.
3. **Mastery-trajectory plot** for one student.
Say: "I fit BKT per skill. AUC 0.71 — in the published range. The parameters are
*interpretable*: for example a high prior means students often already know that skill.
And this trajectory plot is the punchline — it shows P(mastered) climbing as the student
answers correctly and dipping when they slip; when it crosses 0.85, the app unlocks the
next concept. **This number literally drives my product.**"

**E. DKT (one big cell).**
What it does: encodes each (skill, correct) pair, an **Embedding → LSTM → Linear** network
predicts next-step correctness, trained 8 epochs with the **Adam** optimizer and binary
cross-entropy loss, on the *same* split as BKT.
Say: "DKT is the deep model. Each answer is embedded, an LSTM reads the sequence — its
hidden state is the student's evolving knowledge — and a linear layer predicts the next
answer. Same train/test split as BKT for a fair comparison. AUC 0.755 — it edges out BKT."

**F. Comparison.**
A bar chart + a full metrics table (AUC, accuracy, precision, recall, F1).
Say: "Side by side: DKT wins slightly. Both are solid. BKT stays my interpretable
headline because its mastery number is what the product uses."

**G. Conclusion (markdown).**
Say: "Real numbers, in the published range, and they plug straight into the unlock gate.
Honest limitations: I model the top-30 skills, and scaling to EdNet is the next step."

---

## 5. Notebook 2 walkthrough — `grading_mohler.ipynb` (shorter)

What it does: parses the Mohler CS short-answer dataset, visualises the grade
distribution, then trains **TF-IDF + SVR / Ridge** to predict the human grade, reporting
**Pearson correlation and RMSE**, with a predicted-vs-actual scatter.
Say: "This proves I can grade with classical ML on real CS data — Pearson 0.54, RMSE
about 0.9 points on a 0–5 scale. In production I use an LLM for grading because it
handles open-ended answers better, and this is the benchmark I measure it against."

---

## 6. Anticipated questions + crisp answers

**Q: What is knowledge tracing?**
A: A model that estimates a student's mastery of each skill from their answer history and
predicts whether they'll get the next question right.

**Q: Why knowledge tracing instead of the misconception classifier you proposed?**
A: There's no public dataset mapping pseudocode answers to misconceptions — I verified
that. Rather than fabricate data, I made KT the contribution: real data, established
models, and it's what fixes the statelessness gap. Misconception labels are still in the
product, produced by the LLM at inference time.

**Q: Difference between BKT and DKT?**
A: BKT is an interpretable 4-parameter-per-skill probabilistic model (a hidden Markov
model). DKT is a neural network (LSTM) that learns patterns across all skills. DKT scored
slightly higher (0.755 vs 0.714 AUC).

**Q: Why did DKT only win by a little?**
A: That's a known result (Khajah et al. 2016) — a well-set-up BKT is competitive with
deep models on ASSISTments. Both are valid; I report it honestly.

**Q: Why AUC and not accuracy?**
A: The data is imbalanced — about two-thirds of answers are correct — so accuracy can look
high just by predicting "correct." AUC is threshold-independent and handles imbalance.

**Q: Your recall is higher than precision — why?**
A: Same imbalance. Most answers are correct, so the model leans toward predicting
"correct," which catches almost all true positives (high recall) at some cost to precision.

**Q: How did you avoid overfitting / data leakage?**
A: I split by *student*, so no student is in both train and test — it measures
generalisation to new learners.

**Q: What are slip and guess?**
A: Slip = you know the skill but answer wrong; guess = you don't know it but answer right.
I bound both at 0.30 to avoid BKT's known identifiability problem (where the model can flip
the meaning of "known").

**Q: Why did you implement BKT yourself instead of a library?**
A: The standard library (pyBKT) wouldn't build on this Python version — but more
importantly, implementing it myself means I understand and can explain every line.

**Q: Which dataset and why the "corrected" version?**
A: ASSISTments 2009–2010 skill-builder. The original file has duplicate rows (~25% of
records) that inflate scores, so the corrected one-row-per-attempt version is mandatory.

**Q: How does the ML connect to the app I'm demoing?**
A: BKT outputs a per-concept mastery probability. When it crosses 0.85 the next concept
unlocks. The mastery-trajectory plot in the notebook is that exact signal.

**Q: Limitations / next steps?**
A: I model the top-30 skills (68% of data) on one dataset; next is all skills + EdNet for
scale, then applying the same pipeline to my platform's own logged interactions.

---

## 7. Suggested order for the video (ML portion, ~2–3 min)

1. One-line pitch (section 0).
2. Show the **learning curve** — "students learn with practice; this is what KT models."
3. Show **BKT AUC + the mastery-trajectory plot** — "0.71, in the published range, and
   this curve is what unlocks concepts in my app."
4. Show **DKT AUC** and the **BKT-vs-DKT comparison** — "deep model edges it out, both solid."
5. One sentence on **Mohler grading** as the grading benchmark.
6. Close: "So my ML contribution is a stateful knowledge-tracing model, validated on real
   data, that powers the adaptive unlock map."

Keep the rubric in mind — the graders care most about: you **understand** what you built,
your **environment is set up**, and your app **navigates cleanly**. You have all three.
