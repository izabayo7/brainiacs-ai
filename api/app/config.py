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

    # CORS origin for the Next.js dev server.
    frontend_origin: str = "http://localhost:3000"

    # --- Auth ---
    # Secret used to sign the backend's own JWTs (HS256). Override in .env.
    jwt_secret: str = "dev-only-change-me"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 days


settings = Settings()
