# Build context is the repo root (so we can copy ../content).
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 CONTENT_DIR=/content
WORKDIR /app

# Dependencies first for layer caching.
COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --requirement requirements.txt

# App code, migrations, and curriculum content.
COPY api/ ./
COPY content/ /content
RUN chmod +x ./entrypoint.sh

EXPOSE 8000
CMD ["./entrypoint.sh"]
