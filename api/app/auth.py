"""Authentication core: password hashing, JWT issue/verify, current-user dependency.

The backend is the source of truth for identity. It issues its own HS256 JWT; the
Next.js layer (NextAuth) carries that token and sends it as a Bearer on every API call.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import Student

ALGORITHM = "HS256"


# --- Passwords ---------------------------------------------------------------

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str | None) -> bool:
    if not hashed:
        return False
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


# --- JWT ---------------------------------------------------------------------

def create_access_token(student_id: int, email: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(student_id),
        "email": email,
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def _decode(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:  # expired / invalid signature / malformed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc


# --- Current-user dependency -------------------------------------------------

def get_current_student(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Student:
    """Resolve the authenticated learner from the `Authorization: Bearer <jwt>` header."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.split(" ", 1)[1].strip()
    payload = _decode(token)
    student = db.get(Student, int(payload.get("sub", 0)))
    if student is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return student
