"""Auth endpoints: email/password register + login, and /me.

All return a backend JWT (TokenOut) that the frontend carries as a Bearer token.
Auth is email/password only — no external identity provider — so no learner identity
leaves the system (self-hosted, data-sovereign).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    get_current_student,
    hash_password,
    verify_password,
)
from app.db import get_db
from app.models import Student
from app.schemas import LoginIn, RegisterIn, TokenOut, UserOut

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


@router.get("/me", response_model=UserOut)
def me(current: Student = Depends(get_current_student)) -> UserOut:
    return UserOut.model_validate(current)
