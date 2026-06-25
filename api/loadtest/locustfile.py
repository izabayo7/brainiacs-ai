"""Load test for the Brainiacs AI API — measures the read hot path under concurrency.

Design note: this creates ONE account once (at test start) and all simulated learners
reuse its token. That's deliberate. Registration/login use bcrypt password hashing, which
is intentionally CPU-expensive; if every virtual user registered its own account, the test
would just measure "how many bcrypt hashes can one dev worker do at once" (and time out),
not how the app serves real learners. Real traffic is overwhelmingly *reads* (loading the
concept map and progress), so that's what we load here.

Run it so it stops on its own and prints a summary (recommended for the screenshot):
    pip install locust
    locust -f api/loadtest/locustfile.py --headless -u 30 -r 5 -t 60s \
           --host http://localhost:8000
    # -u 30 = 30 users, -r 5 = ramp 5/s, -t 60s = run 60s then exit.

Or with the web UI (remember to click STOP — the UI runs until you stop it):
    locust -f api/loadtest/locustfile.py --host http://localhost:8000
    # open http://localhost:8089

Point --host at https://api.brainiacs.bwenge.rw to test the deployed API instead (keep the
user count modest — don't hammer production).
"""
from __future__ import annotations

import uuid

import requests
from locust import HttpUser, between, events, task

_TOKEN = {"value": None}


@events.test_start.add_listener
def _create_shared_account(environment, **kwargs):
    host = environment.host or "http://localhost:8000"
    email = f"load-{uuid.uuid4().hex[:12]}@test.com"
    requests.post(f"{host}/auth/register",
                  json={"name": "Load", "email": email, "password": "pw12345"}, timeout=30)
    resp = requests.post(f"{host}/auth/login",
                         json={"email": email, "password": "pw12345"}, timeout=30)
    _TOKEN["value"] = resp.json().get("access_token") if resp.ok else None
    if not _TOKEN["value"]:
        print("WARNING: could not obtain a token — is the API running at", host, "?")


class Learner(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.headers = {"Authorization": f"Bearer {_TOKEN['value']}"} if _TOKEN["value"] else {}

    @task(3)
    def list_concepts(self):
        self.client.get("/concepts", headers=self.headers, name="GET /concepts")

    @task(2)
    def progress(self):
        self.client.get("/progress", headers=self.headers, name="GET /progress")
