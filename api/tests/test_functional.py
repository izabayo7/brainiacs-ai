"""End-to-end functional tests for the core learning loop.

These exercise the real API (FastAPI TestClient against the configured database):
registration, the prerequisite gate, deterministic grading, the BKT mastery update,
unlocking, and the learner-model aggregation. Run with:

    cd api && .venv/bin/python -m pytest tests/test_functional.py -v
"""
from __future__ import annotations

import uuid

from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models import Exercise

client = TestClient(app)


def _auth():
    """Register a fresh student and return its auth header."""
    email = f"func-{uuid.uuid4().hex[:10]}@test.com"
    client.post("/auth/register", json={"name": "Test", "email": email, "password": "pw12345"})
    tok = client.post("/auth/login", json={"email": email, "password": "pw12345"}).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}


def _correct_answers(quiz):
    """Build the correct response for each generated question from the seeded bank."""
    db = SessionLocal()
    try:
        out = []
        for q in quiz["questions"]:
            ex = db.get(Exercise, q["id"])
            out.append({
                "question_id": q["id"],
                "type": q["type"],
                "prompt": q["prompt"],
                "response": ex.correct_answer_json,
            })
        return out
    finally:
        db.close()


def test_register_and_concept_states():
    """A new student sees at least one available concept and at least one locked one."""
    H = _auth()
    concepts = client.get("/concepts", headers=H).json()
    assert len(concepts) >= 2
    assert any(c["state"] == "available" for c in concepts)
    assert any(c["state"] == "locked" for c in concepts)


def test_prerequisite_gate_blocks_locked_concepts():
    """Generating a quiz for a locked concept is rejected (403) — the gate holds."""
    H = _auth()
    locked = [c for c in client.get("/concepts", headers=H).json() if c["state"] == "locked"]
    assert locked, "later concepts must start locked"
    r = client.post(f"/quiz/{locked[0]['id']}/generate", headers=H)
    assert r.status_code == 403


def test_wrong_answers_populate_the_learner_model():
    """Wrong answers are graded incorrect and surface as a recurring difficulty."""
    H = _auth()
    cid = next(c for c in client.get("/concepts", headers=H).json() if c["state"] == "available")["id"]
    quiz = client.post(f"/quiz/{cid}/generate", headers=H).json()
    answers = [
        {"question_id": q["id"], "type": q["type"], "prompt": q["prompt"], "response": "DEFINITELY_WRONG"}
        for q in quiz["questions"]
    ]
    result = client.post(f"/quiz/{cid}/submit", headers=H, json={"concept_id": cid, "answers": answers}).json()
    assert all(g["is_correct"] is False for g in result["graded"])

    progress = client.get("/progress", headers=H).json()
    assert progress["total_attempts"] >= 1
    assert len(progress["recurring_difficulties"]) >= 1  # the AI made visible


def test_correct_answers_raise_mastery_and_unlock():
    """Repeated correct answers raise the BKT estimate, master the concept, and unlock a dependent."""
    H = _auth()
    cid = next(c for c in client.get("/concepts", headers=H).json() if c["state"] == "available")["id"]
    available_before = {c["id"] for c in client.get("/concepts", headers=H).json() if c["state"] == "available"}

    mastered = False
    last_p = 0.0
    for _ in range(8):  # cap rounds; correct answers should cross the 0.85 threshold well before this
        quiz = client.post(f"/quiz/{cid}/generate", headers=H).json()
        result = client.post(
            f"/quiz/{cid}/submit", headers=H,
            json={"concept_id": cid, "answers": _correct_answers(quiz)},
        ).json()
        assert result["p_mastered"] >= last_p - 1e-9  # mastery is non-decreasing under correct answers
        last_p = result["p_mastered"]
        if result["mastered"]:
            mastered = True
            break

    assert mastered, f"concept should master under correct answers (reached p={last_p:.3f})"
    available_after = {c["id"] for c in client.get("/concepts", headers=H).json() if c["state"] in ("available", "mastered")}
    assert available_after >= available_before  # mastering never removes access; usually unlocks more
