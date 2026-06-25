"""Load test for the Brainiacs AI API.

Simulates concurrent learners hitting the read-heavy endpoints (the concept map and
their progress / learner model). Use it to check the performance budget, e.g.
"95% of requests < 300 ms with 50 concurrent users, error rate < 1%".

Run against a local stack (safest):
    pip install locust
    locust -f api/loadtest/locustfile.py --host http://localhost:8000
    # then open http://localhost:8089 → 50 users, spawn rate 5 → run ~1 min
    # screenshot the Statistics + Charts tabs for the README.
"""
from __future__ import annotations

import uuid

from locust import HttpUser, between, task


class Learner(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        email = f"load-{uuid.uuid4().hex[:12]}@test.com"
        self.client.post(
            "/auth/register",
            json={"name": "Load", "email": email, "password": "pw12345"},
        )
        resp = self.client.post(
            "/auth/login", json={"email": email, "password": "pw12345"}
        )
        token = resp.json().get("access_token") if resp.ok else None
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    @task(3)
    def list_concepts(self):
        self.client.get("/concepts", headers=self.headers, name="GET /concepts")

    @task(2)
    def progress(self):
        self.client.get("/progress", headers=self.headers, name="GET /progress")
