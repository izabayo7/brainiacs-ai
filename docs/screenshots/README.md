# App screenshots

These are captured from the **live build** (Next.js app + FastAPI backend), matching
the Brainiacs AI Figma design:

| File | Screen |
|------|--------|
| `dashboard.png` | Dashboard — "what's next" + concept map (locked/available/mastered) |
| `concept.png` | Concept / Learn page — chapter, worked example, lesson sidebar |
| `quiz.png` | Quiz workspace — the three pseudocode-safe question types |
| `quiz-result.png` | Graded quiz — misconception labels, scaffolded feedback, mastery gate |

To re-capture after UI changes: start the backend (`make api`) and frontend
(`make web`), then run the Playwright script (`/tmp/shoot.py` during development) or
simply screenshot the three routes at http://localhost:3000.
