# Deployment Plan — Brainiacs AI

This describes how the demo is taken to a deployed environment. It is the
**documented target**, not necessarily executed for this initial submission.

## Target

A single **cloud.strettch.com** VM running Docker, with **Nginx** as a reverse
proxy in front of the FastAPI backend and the Next.js frontend, and a managed (or
containerised) **PostgreSQL**.

```
                     ┌──────────────────────── VM (cloud.strettch.com) ───────────────────────┐
   Internet  ──443──▶│  Nginx (TLS, reverse proxy)                                             │
                     │     ├── /            ──▶  web   (Next.js, :3000)                         │
                     │     └── /api, /docs  ──▶  api   (FastAPI/uvicorn, :8000)                 │
                     │                                   └──▶ postgres (:5432, private network) │
                     └────────────────────────────────────────────────────────────────────────┘
```

## Containerisation

Three services via `docker-compose`:

- **db** — `postgres:16`, named volume for data, not exposed publicly.
- **api** — built from `api/`, runs `alembic upgrade head` on start, then
  `uvicorn app.main:app --host 0.0.0.0 --port 8000`. Reads `DATABASE_URL` and
  `ANTHROPIC_API_KEY` from the environment.
- **web** — built from `web/` (`next build` → `next start`), reads
  `NEXT_PUBLIC_API_BASE_URL` (pointing at the public `/api` path).

> Dockerfiles are intentionally not added in this initial submission to keep the
> repo lean; the build steps above mirror the local `make` targets exactly.

## Reverse proxy (Nginx)

- Terminate TLS (Let's Encrypt / certbot).
- `location /` → `web` upstream (`proxy_pass http://web:3000`).
- `location /api/` and `location /docs` → `api` upstream (`proxy_pass http://api:8000/`).
- Set `proxy_set_header Host`, `X-Forwarded-For`, `X-Forwarded-Proto`.

## Migrations

Schema changes ship as **Alembic** revisions. On deploy, the `api` container runs
`alembic upgrade head` before serving. Seed content is loaded once with
`python -m app.seed` (or a one-off `docker compose run api python -m app.seed`).

## Environment / secrets management

- No secrets in the image or repo. `.env` is git-ignored; `.env.example` documents
  the variables.
- On the VM, secrets are provided via the orchestrator's env/secret mechanism
  (compose `env_file`, or the platform's secret store): `ANTHROPIC_API_KEY`,
  `DATABASE_URL`, `NEXT_PUBLIC_API_BASE_URL`.
- Rotate `ANTHROPIC_API_KEY` independently of deploys.

## The model swap: API → self-hosted Qwen3.5-4B

The demo calls the **Anthropic API** behind the `LLMClient` seam
([`api/app/llm.py`](../api/app/llm.py)). Production does **not** call a paid API:

1. Fine-tune **Qwen3.5-4B** on real, annotated pilot data (the experiment scaffolded
   in the ML notebook).
2. Serve it on the VM (or a GPU node) behind an OpenAI-compatible endpoint
   (e.g. vLLM / TGI).
3. Add a `QwenClient(LLMClient)` implementing `generate_quiz`,
   `grade_and_classify`, and `explain` against that endpoint.
4. Switch the factory `get_llm_client()` via a config flag. **No other code
   changes** — routers, schemas, BKT, and the frontend are untouched.

This is the entire point of the `LLMClient` abstraction: the production model is a
drop-in replacement for the demo's API client.

## Operational notes

- Health check: `GET /health` on the api service.
- Backups: scheduled `pg_dump` of the `db` volume.
- Logs: uvicorn + Nginx access/error logs shipped to the platform's log store.
