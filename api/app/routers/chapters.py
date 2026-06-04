"""Serve human-authored chapter content."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Chapter
from app.schemas import ChapterOut

router = APIRouter(prefix="/chapters", tags=["chapters"])


@router.get("/{chapter_id}", response_model=ChapterOut)
def get_chapter(chapter_id: int, db: Session = Depends(get_db)) -> ChapterOut:
    chapter = db.get(Chapter, chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return ChapterOut.model_validate(chapter)


@router.get("", response_model=list[ChapterOut])
def list_chapters(concept_id: int, db: Session = Depends(get_db)) -> list[ChapterOut]:
    chapters = db.scalars(
        select(Chapter).where(Chapter.concept_id == concept_id).order_by(Chapter.id)
    ).all()
    return [ChapterOut.model_validate(ch) for ch in chapters]
