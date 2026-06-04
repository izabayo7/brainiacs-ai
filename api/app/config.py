"""Centralised settings, loaded from environment / .env.

Single source of truth for configuration so nothing reads os.environ ad hoc.
"""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Read from the repo-root .env (one level above api/) and process env.
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"), env_file_encoding="utf-8", extra="ignore"
    )

    database_url: str = "postgresql+psycopg://brainiacs:brainiacs@localhost:5432/brainiacs"

    # LLM. Key is optional so the app boots without it; the AnthropicClient only
    # requires it at call time, and the quiz route falls back to seeded exercises.
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"

    # CORS origin for the Next.js dev server.
    frontend_origin: str = "http://localhost:3000"


settings = Settings()
