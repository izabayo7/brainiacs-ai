"""FastAPI entrypoint: CORS, routers, OpenAPI/Swagger at /docs."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, chapters, concepts, progress, quiz

app = FastAPI(
    title="Brainiacs AI API",
    description=(
        "Adaptive tutoring for programming fundamentals. Pseudocode-only; the AI "
        "generates quizzes, grades + classifies misconceptions, and explains — it "
        "never generates learning content and never executes code."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(concepts.router)
app.include_router(chapters.router)
app.include_router(quiz.router)
app.include_router(progress.router)


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok", "service": "brainiacs-api"}
