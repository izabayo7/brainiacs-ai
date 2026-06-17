# Convenience targets for the Brainiacs AI demo.
# These assume a Python venv at api/.venv and a running PostgreSQL.

.PHONY: help api-install migrate seed content api web-install web notebook

help:
	@echo "Targets:"
	@echo "  api-install   Create api/.venv and install backend deps"
	@echo "  migrate       Apply Alembic migrations (alembic upgrade head)"
	@echo "  seed          Load human-authored concepts/chapters/exercises"
	@echo "  api           Run the FastAPI backend (uvicorn, :8000, /docs)"
	@echo "  web-install   npm install in web/"
	@echo "  web           Run the Next.js dev server (:3000)"
	@echo "  notebook      Launch the ML notebook"

api-install:
	cd api && python3 -m venv .venv && .venv/bin/python -m pip install --upgrade pip \
		&& .venv/bin/python -m pip install --requirement requirements.txt

migrate:
	cd api && .venv/bin/alembic upgrade head

seed: content    ## alias — load curriculum from content/*.md

content:    ## load human-authored curriculum (content/*.md) into the DB
	cd api && .venv/bin/python -m app.content_loader

api:
	cd api && .venv/bin/uvicorn app.main:app --reload --port 8000

web-install:
	cd web && npm install

web:
	cd web && npm run dev

notebook:
	cd ml && jupyter notebook kt_knowledge_tracing_assistments.ipynb
