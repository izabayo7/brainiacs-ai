# Deployment Plan — Brainiacs AI

Target: a **StrangeCloud** (cloud.strettch.com) VM running **Docker** with **Caddy** as
the reverse proxy (automatic HTTPS). The whole stack is defined in
[`docker-compose.yml`](../docker-compose.yml).

## Architecture

```
                 ┌──────────────── StrangeCloud VM ─────────────────┐
  Internet ─443─▶│  Caddy (auto-HTTPS)                              │
                 │    APP_DOMAIN      ──▶  web  (Next.js, :3000)     │
                 │    API_DOMAIN      ──▶  api  (FastAPI, :8000)     │
                 │                              └──▶ db (postgres)   │
                 └──────────────────────────────────────────────────┘
```

Two hostnames (e.g. `brainiacs.example.com` and `api.brainiacs.example.com`) keep the
web app and API on separate origins, so NextAuth's own `/api/auth/*` routes never clash
with the backend.

## Services (docker-compose)
- **db** — `postgres:16`, data on a named volume.
- **api** — built from [`api/Dockerfile`](../api/Dockerfile). On start
  ([`api/entrypoint.sh`](../api/entrypoint.sh)) it waits for the DB, runs
  `alembic upgrade head`, loads the curriculum once (`content_loader --if-empty`, so
  restarts don't wipe progress), then serves uvicorn.
- **web** — built from [`web/Dockerfile`](../web/Dockerfile) (Next.js standalone). The
  public API URL is baked at build time via the `NEXT_PUBLIC_API_BASE_URL` build arg.
- **caddy** — terminates TLS and reverse-proxies the two domains
  ([`Caddyfile`](../Caddyfile)).

## Deploy steps (on the VM)
1. Install Docker + the compose plugin.
2. Point DNS **A records** for `APP_DOMAIN` and `API_DOMAIN` at the VM's IP.
3. Clone the repo; `cp .env.deploy.example .env` and fill it in (domains, secrets,
   Google OAuth creds, optional `ANTHROPIC_API_KEY`).
4. In Google Cloud, add the redirect URI `https://APP_DOMAIN/api/auth/callback/google`.
5. `docker compose up -d --build`.
6. Caddy provisions HTTPS automatically. Visit `https://APP_DOMAIN`.

## Environment / secrets
All config is env-driven ([`.env.deploy.example`](../.env.deploy.example)); nothing is
baked into images except the public API URL. `JWT_SECRET`, `NEXTAUTH_SECRET`, and
`AUTH_SYNC_SECRET` must be strong random values; `AUTH_SYNC_SECRET` must match between
`web` and `api`.

## Migrations & content
Schema changes ship as Alembic revisions and run on container start. Curriculum lives in
[`content/`](../content) as markdown and is imported into the DB by the loader.

## Verification (deployment is tested, not just planned)
Both images were built and run locally: the **api** container migrates, loads content,
and serves authenticated endpoints; the **web** container serves the app and NextAuth.
On the VM, verify by signing in and completing a quiz over HTTPS.

## Production model swap
LLM calls sit behind the `LLMClient` interface ([`api/app/llm.py`](../api/app/llm.py)).
Demo uses the Anthropic API; the production plan is a self-hosted fine-tuned **Qwen**
served behind an OpenAI-compatible endpoint — implement one `QwenClient(LLMClient)` and
switch the factory; nothing else changes. With no key set, the app falls back to seeded
quizzes + a deterministic offline grader, so it runs without paid API calls.
