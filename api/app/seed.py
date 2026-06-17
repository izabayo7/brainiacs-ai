"""Seed entrypoint — curriculum now lives in `content/*.md` and is loaded by
`content_loader`. This thin wrapper keeps `python -m app.seed` / `make seed` working.

To author/edit content, edit the markdown files in `content/` (see the format in
`app/content_loader.py`), then re-run this.
"""
from app.content_loader import load


def seed() -> None:
    load()


if __name__ == "__main__":
    seed()
