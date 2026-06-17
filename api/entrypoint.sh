#!/usr/bin/env bash
# Container start: wait for DB, run migrations, load content once, then serve.
set -e

echo "Waiting for the database…"
python - <<'PY'
import os, time, psycopg
url = os.environ["DATABASE_URL"].replace("postgresql+psycopg://", "postgresql://")
for attempt in range(60):
    try:
        psycopg.connect(url).close()
        print("Database is up.")
        break
    except Exception as exc:
        print(f"  not ready ({exc}); retrying…")
        time.sleep(2)
else:
    raise SystemExit("Database never became ready")
PY

echo "Running migrations…"
alembic upgrade head

echo "Loading curriculum (only if empty)…"
python -m app.content_loader --if-empty

echo "Starting API…"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
