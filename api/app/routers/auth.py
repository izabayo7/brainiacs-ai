"""Auth endpoints: email/password register + login, Google sync, and /me.

All return a backend JWT (TokenOut) that the frontend carries as a Bearer token.
Google users are synced from the Next.js auth layer, which proves itself with the
shared `X-Auth-Sync-Secret` header (NextAuth already verified Google).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    get_current_student,
    hash_password,
    verify_password,
)
from app.config import settings
from app.db import get_db
from app.models import Student
from app.schemas import GoogleSyncIn, LoginIn, RegisterIn, TokenOut, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


def _token_for(student: Student) -> TokenOut:
    return TokenOut(
        access_token=create_access_token(student.id, student.email),
        user=UserOut.model_validate(student),
    )


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn, db: Session = Depends(get_db)) -> TokenOut:
    email = payload.email.strip().lower()
    if db.scalar(select(Student).where(Student.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    student = Student(
        name=payload.name.strip() or email.split("@")[0],
        email=email,
        password_hash=hash_password(payload.password),
        provider="password",
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return _token_for(student)


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)) -> TokenOut:
    email = payload.email.strip().lower()
    student = db.scalar(select(Student).where(Student.email == email))
    if student is None or not verify_password(payload.password, student.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return _token_for(student)


@router.post("/google", response_model=TokenOut)
def google_sync(
    payload: GoogleSyncIn,
    x_auth_sync_secret: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> TokenOut:
    """Upsert a Google user. Called server-side by NextAuth after Google verified them."""
    if x_auth_sync_secret != settings.auth_sync_secret:
        raise HTTPException(status_code=403, detail="Bad sync secret")
    email = payload.email.strip().lower()
    student = db.scalar(select(Student).where(Student.email == email))
    if student is None:
        student = Student(name=payload.name, email=email, provider="google")
        db.add(student)
    # Keep profile fresh on each login.
    student.name = payload.name or student.name
    student.avatar_url = payload.avatar_url or student.avatar_url
    if student.provider != "google" and student.password_hash is None:
        student.provider = "google"
    db.commit()
    db.refresh(student)
    return _token_for(student)


@router.get("/me", response_model=UserOut)
def me(current: Student = Depends(get_current_student)) -> UserOut:
    return UserOut.model_validate(current)
