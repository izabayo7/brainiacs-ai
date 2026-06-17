"""Content pipeline: parse → validate → load the curriculum from `content/*.md`.

The markdown files are the single source of truth (see content/CONTENT_FORMAT.md).
This module keeps the three concerns separate as functions — `parse_file` (pure,
no DB), `validate` (enforces the contract, no DB), and `load` (idempotent reload
into Postgres) — in one file because the job is small; splitting into three modules
would be configurability we don't need (software is a liability).

CLI (long-form flags):
    python -m app.content_loader --validate-only       # check the contract, no DB
    python -m app.content_loader --dry-run             # validate + report, no writes
    python -m app.content_loader --path content/       # choose the content dir
    python -m app.content_loader --if-empty            # load only if DB has no concepts

Content loading is a SEEDER, not an Alembic migration — schema lives in migrations,
data lives here, and the two have different lifecycles.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
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
from app.taxonomy import MISCONCEPTION_SET

VALID_TYPES = {"mcq", "predict_output", "pseudocode_order"}
VALID_DIFFICULTY = {"easy", "medium", "hard"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


# --- locate content ----------------------------------------------------------

def _content_dir() -> Path:
    if os.environ.get("CONTENT_DIR"):
        return Path(os.environ["CONTENT_DIR"])
    return Path(__file__).resolve().parents[2] / "content"


# --- parser (pure) ------------------------------------------------------------

def _split_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError("missing YAML frontmatter (--- ... ---)")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def _sections(body: str) -> dict[str, str]:
    out: dict[str, str] = {}
    current, buf = None, []
    for line in body.splitlines():
        if line.startswith("## "):
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current, buf = line[3:].strip(), []
        else:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    return out


def _exercises_from(section: str) -> list[dict]:
    if not section:
        return []
    m = re.search(r"```ya?ml\n(.*?)```", section, re.DOTALL)
    data = yaml.safe_load(m.group(1) if m else section)
    return data or []


def parse_file(path: Path) -> dict:
    meta, body = _split_frontmatter(path.read_text(encoding="utf-8"))
    secs = _sections(body)
    explanation = secs.get("Explanation", "").strip()
    worked = secs.get("Worked example", "").strip()
    key_ideas = secs.get("Key ideas", "").strip()

    # The page already shows the concept title, so the lesson body starts at the
    # explanation (no repeated heading).
    parts = [explanation]
    if worked:
        parts += ["### Worked example", worked]
    if key_ideas:
        parts += ["### Key ideas", key_ideas]

    return {
        "file": path.name,
        "meta": meta,
        "slug": meta.get("slug"),
        "name": meta.get("name"),
        "order": meta.get("order"),
        "prerequisites": meta.get("prerequisites", []) or [],
        "summary": meta.get("summary"),
        "estimated_minutes": meta.get("estimated_minutes"),
        "explanation_md": explanation,
        "worked_example_md": worked,
        "worked_has_pseudocode": "```pseudocode" in worked,
        "key_ideas": key_ideas,
        "chapter_body": "\n\n".join(p for p in parts if p).strip(),
        "video_url": meta.get("video_url"),
        "exercises": _exercises_from(secs.get("Exercises", "")),
        "has_sections": {k: (k in secs) for k in ("Explanation", "Worked example", "Key ideas")},
    }


def parse_all(content_dir: Path) -> list[dict]:
    files = sorted(f for f in content_dir.glob("*.md") if re.match(r"\d+-", f.name))
    if not files:
        raise SystemExit(f"No content files (NN-slug.md) found in {content_dir}")
    return [parse_file(f) for f in files]


# --- validator (enforces content/CONTENT_FORMAT.md) ---------------------------

def validate(lessons: list[dict]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    slugs: dict[str, int] = {}  # slug -> order

    for L in lessons:
        f = L["file"]
        # 1. required front-matter + types
        for field, typ in [("slug", str), ("name", str), ("order", int),
                           ("summary", str), ("estimated_minutes", int)]:
            if not isinstance(L["meta"].get(field), typ):
                errors.append(f"{f}: front-matter '{field}' missing or not a {typ.__name__}")
        if not isinstance(L["prerequisites"], list):
            errors.append(f"{f}: 'prerequisites' must be a list")
        if isinstance(L["estimated_minutes"], int) and L["estimated_minutes"] <= 0:
            errors.append(f"{f}: 'estimated_minutes' must be positive")
        # 2. slug kebab-case + unique
        if isinstance(L["slug"], str):
            if not SLUG_RE.match(L["slug"]):
                errors.append(f"{f}: slug '{L['slug']}' is not kebab-case")
            if L["slug"] in slugs:
                errors.append(f"{f}: duplicate slug '{L['slug']}'")
            slugs[L["slug"]] = L["order"] if isinstance(L["order"], int) else -1
        # 6. sections present + pseudocode block
        for sec, present in L["has_sections"].items():
            if not present:
                errors.append(f"{f}: missing '## {sec}' section")
        if not L["worked_has_pseudocode"]:
            errors.append(f"{f}: '## Worked example' must contain a ```pseudocode block")
        # 7/8/9/10/11. exercises
        _validate_exercises(L, errors, warnings)

    # 3/4/5. prerequisite graph (needs all slugs known)
    for L in lessons:
        for pre in L["prerequisites"]:
            if pre not in slugs:
                errors.append(f"{L['file']}: prerequisite '{pre}' is not an existing slug")
            elif isinstance(L["order"], int) and slugs[pre] >= L["order"]:
                errors.append(
                    f"{L['file']}: order {L['order']} must exceed prerequisite '{pre}' order {slugs[pre]}")
    if _has_cycle(lessons):
        errors.append("prerequisite graph has a cycle (must be acyclic)")

    return errors, warnings


def _validate_exercises(L: dict, errors: list[str], warnings: list[str]) -> None:
    f = L["file"]
    exs = L["exercises"]
    if len(exs) < 6:
        errors.append(f"{f}: needs 6+ exercises, found {len(exs)}")
    seen_types, has_hard = set(), False
    for i, ex in enumerate(exs):
        where = f"{f} exercise[{i}]"
        t = ex.get("type")
        seen_types.add(t)
        if ex.get("difficulty") == "hard":
            has_hard = True
        if t not in VALID_TYPES:
            errors.append(f"{where}: invalid type '{t}'"); continue
        if ex.get("difficulty") not in VALID_DIFFICULTY:
            errors.append(f"{where}: invalid difficulty '{ex.get('difficulty')}'")
        if ex.get("target_misconception") not in MISCONCEPTION_SET:
            errors.append(f"{where}: invalid target_misconception '{ex.get('target_misconception')}'")
        if not (ex.get("prompt") or "").strip():
            errors.append(f"{where}: empty prompt")
        if not (ex.get("explanation") or "").strip():
            errors.append(f"{where}: empty explanation")
        ca, opts = ex.get("correct_answer"), ex.get("options")
        if t == "mcq":
            if not isinstance(opts, list) or not (2 <= len(opts) <= 4):
                errors.append(f"{where}: mcq needs 2–4 options")
            elif ca not in opts:
                errors.append(f"{where}: mcq correct_answer is not one of options")
        elif t == "pseudocode_order":
            if not isinstance(opts, list) or not isinstance(ca, list) or sorted(map(str, opts)) != sorted(map(str, ca)):
                errors.append(f"{where}: pseudocode_order correct_answer must be a permutation of options")
        elif t == "predict_output":
            if not isinstance(ca, str) or not ca.strip():
                errors.append(f"{where}: predict_output correct_answer must be a non-empty string")
    for missing in VALID_TYPES - seen_types:
        warnings.append(f"{f}: no '{missing}' exercise (consider adding one)")
    if not has_hard:
        warnings.append(f"{f}: no 'hard' exercise")


def _has_cycle(lessons: list[dict]) -> bool:
    graph = {L["slug"]: list(L["prerequisites"]) for L in lessons if L["slug"]}
    state: dict[str, int] = {}  # 0=visiting, 1=done

    def visit(node: str) -> bool:
        if state.get(node) == 1:
            return False
        if state.get(node) == 0:
            return True  # back-edge → cycle
        state[node] = 0
        for nxt in graph.get(node, []):
            if nxt in graph and visit(nxt):
                return True
        state[node] = 1
        return False

    return any(visit(s) for s in graph)


# --- loader (idempotent reload) ----------------------------------------------

def _load_into_db(lessons: list[dict]) -> None:
    lessons = sorted(lessons, key=lambda c: c["order"])
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        for model in (Attempt, MasteryEstimate, Exercise, Chapter, ConceptPrerequisite, Concept):
            db.execute(delete(model))
        db.commit()

        slug_to_id: dict[str, int] = {}
        for c in lessons:
            concept = Concept(
                slug=c["slug"], name=c["name"], order_hint=c["order"],
                summary=c["summary"] or "",
                explanation_md=c["explanation_md"], worked_example_md=c["worked_example_md"],
            )
            db.add(concept); db.flush()
            slug_to_id[c["slug"]] = concept.id
            db.add(Chapter(concept_id=concept.id, title=f"{c['name']} — Chapter 1",
                           body_md=c["chapter_body"], video_url=c["video_url"]))

        for c in lessons:
            for pre in c["prerequisites"]:
                db.add(ConceptPrerequisite(concept_id=slug_to_id[c["slug"]],
                                           prerequisite_concept_id=slug_to_id[pre]))

        n_ex = 0
        for c in lessons:
            for ex in c["exercises"]:
                db.add(Exercise(
                    concept_id=slug_to_id[c["slug"]],
                    type=ExerciseType(ex["type"]),
                    difficulty=Difficulty(ex.get("difficulty", "medium")),
                    prompt=ex["prompt"], options_json=ex.get("options"),
                    correct_answer_json=ex["correct_answer"],
                    target_misconception=ex.get("target_misconception"),
                    explanation=ex.get("explanation"),
                ))
                n_ex += 1
        db.commit()
        print(f"Loaded {len(lessons)} concepts, {n_ex} exercises.")
    finally:
        db.close()


def load(content_dir: Path | None = None, if_empty: bool = False) -> None:
    """Programmatic entry used by seed.py and the container entrypoint."""
    if if_empty:
        db = SessionLocal()
        try:
            if db.query(Concept).first() is not None:
                print("Content already present; skipping load (--if-empty).")
                return
        finally:
            db.close()
    lessons = parse_all(content_dir or _content_dir())
    errors, warnings = validate(lessons)
    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        raise SystemExit("Content validation failed:\n  - " + "\n  - ".join(errors))
    _load_into_db(lessons)


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate and load Brainiacs curriculum.")
    ap.add_argument("--path", default=None, help="content directory (default: ./content)")
    ap.add_argument("--validate-only", action="store_true", help="check the contract, no DB writes")
    ap.add_argument("--dry-run", action="store_true", help="validate and report, no DB writes")
    ap.add_argument("--if-empty", action="store_true", help="load only if no concepts exist")
    args = ap.parse_args()

    content_dir = Path(args.path) if args.path else _content_dir()
    lessons = parse_all(content_dir)
    errors, warnings = validate(lessons)
    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        print("Content validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Valid: {len(lessons)} lessons, {sum(len(l['exercises']) for l in lessons)} exercises.")

    if args.validate_only:
        return
    if args.dry_run:
        for L in lessons:
            print(f"  would load {L['slug']} (order {L['order']}, {len(L['exercises'])} exercises)")
        return
    load(content_dir, if_empty=args.if_empty)


if __name__ == "__main__":
    main()
