"""Load human-authored curriculum from markdown files into the database.

Content lives in `content/<order>-<slug>.md` (version-controlled, reviewable). This
importer parses each file and upserts the concept graph, chapters, and exercises so
the app serves curriculum from the DB.

File format (see content/ examples or .local/course-content-generation-prompt.md):

    ---
    slug: loops
    name: Loops & Iteration
    order: 4
    prerequisites: [control-flow]
    summary: ...
    estimated_minutes: 20
    ---

    ## Explanation
    <markdown>

    ## Worked example
    <markdown with a pseudocode block>

    ## Key ideas
    - ...

    ## Exercises
    ```yaml
    - type: mcq
      difficulty: easy
      prompt: "..."
      options: ["...", "..."]
      correct_answer: "..."
      target_misconception: loop_boundary_offbyone
      explanation: "..."
    ```

Run:  python -m app.content_loader            (uses ./content or $CONTENT_DIR)
A full load CLEARS existing content + progress (dev/seed-time operation).
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import yaml
from sqlalchemy import delete

from app.db import Base, SessionLocal, engine
from app.models import (
    Attempt,
    Chapter,
    Concept,
    ConceptPrerequisite,
    Difficulty,
    Exercise,
    ExerciseType,
    MasteryEstimate,
)


def _content_dir() -> Path:
    if os.environ.get("CONTENT_DIR"):
        return Path(os.environ["CONTENT_DIR"])
    # Default: <repo>/content  (this file is at <repo>/api/app/content_loader.py)
    return Path(__file__).resolve().parents[2] / "content"


def _split_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError("missing YAML frontmatter (--- ... ---)")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def _sections(body: str) -> dict[str, str]:
    """Split a markdown body into {h2 title: content} on `## ` headers."""
    out: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    return out


def _exercises_from(section: str) -> list[dict]:
    """Pull the ```yaml ...``` block out of the Exercises section and parse it."""
    if not section:
        return []
    m = re.search(r"```ya?ml\n(.*?)```", section, re.DOTALL)
    raw = m.group(1) if m else section
    data = yaml.safe_load(raw)
    return data or []


def parse_file(path: Path) -> dict:
    meta, body = _split_frontmatter(path.read_text(encoding="utf-8"))
    secs = _sections(body)
    explanation = secs.get("Explanation", "").strip()
    worked = secs.get("Worked example", "").strip()
    key_ideas = secs.get("Key ideas", "").strip()

    # Compose the chapter the concept page renders.
    parts = [f"## {meta['name']}", explanation]
    if worked:
        parts += ["### Worked example", worked]
    if key_ideas:
        parts += ["### Key ideas", key_ideas]
    chapter_body = "\n\n".join(p for p in parts if p).strip()

    return {
        "slug": meta["slug"],
        "name": meta["name"],
        "order": int(meta.get("order", 0)),
        "prerequisites": meta.get("prerequisites", []) or [],
        "explanation_md": explanation,
        "worked_example_md": worked,
        "chapter_body": chapter_body,
        "video_url": meta.get("video_url"),
        "exercises": _exercises_from(secs.get("Exercises", "")),
    }


def load(content_dir: Path | None = None, if_empty: bool = False) -> None:
    # On container boot we pass if_empty=True so restarts don't wipe student progress.
    if if_empty:
        db = SessionLocal()
        try:
            from app.models import Concept as _C  # local import to avoid cycle at top
            if db.query(_C).first() is not None:
                print("Content already present; skipping load (--if-empty).")
                return
        finally:
            db.close()

    content_dir = content_dir or _content_dir()
    # Concept files are named "<order>-<slug>.md"; skip README and other docs.
    files = sorted(f for f in content_dir.glob("*.md") if re.match(r"\d+-", f.name))
    if not files:
        raise SystemExit(f"No content files found in {content_dir}")

    parsed = [parse_file(f) for f in files]
    parsed.sort(key=lambda c: c["order"])

    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        # Full reload (dev/seed-time): clear in FK-safe order.
        for model in (Attempt, MasteryEstimate, Exercise, Chapter, ConceptPrerequisite, Concept):
            db.execute(delete(model))
        db.commit()

        slug_to_id: dict[str, int] = {}
        for c in parsed:
            concept = Concept(
                slug=c["slug"], name=c["name"], order_hint=c["order"],
                explanation_md=c["explanation_md"], worked_example_md=c["worked_example_md"],
            )
            db.add(concept)
            db.flush()
            slug_to_id[c["slug"]] = concept.id
            db.add(Chapter(
                concept_id=concept.id, title=f"{c['name']} — Chapter 1",
                body_md=c["chapter_body"], video_url=c["video_url"],
            ))

        for c in parsed:
            for prereq in c["prerequisites"]:
                if prereq not in slug_to_id:
                    raise ValueError(f"{c['slug']}: unknown prerequisite '{prereq}'")
                db.add(ConceptPrerequisite(
                    concept_id=slug_to_id[c["slug"]],
                    prerequisite_concept_id=slug_to_id[prereq],
                ))

        n_ex = 0
        for c in parsed:
            for ex in c["exercises"]:
                db.add(Exercise(
                    concept_id=slug_to_id[c["slug"]],
                    type=ExerciseType(ex["type"]),
                    difficulty=Difficulty(ex.get("difficulty", "medium")),
                    prompt=ex["prompt"],
                    options_json=ex.get("options"),
                    correct_answer_json=ex["correct_answer"],
                    target_misconception=ex.get("target_misconception"),
                ))
                n_ex += 1

        db.commit()
        print(f"Loaded {len(parsed)} concepts, {n_ex} exercises from {content_dir}")
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    load(if_empty="--if-empty" in sys.argv)
