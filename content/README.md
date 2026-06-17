# Curriculum content

Each concept is one markdown file: `<order>-<slug>.md`. These are the **source of
truth** for the curriculum; `make content` (or `python -m app.content_loader`) imports
them into the database, and the app serves them from there.

See the existing files (e.g. `4-loops.md`) for the exact format, or generate new ones
with the prompt in `.local/course-content-generation-prompt.md`.

**Format:** YAML frontmatter (`slug`, `name`, `order`, `prerequisites`, `summary`,
`estimated_minutes`) then `## Explanation`, `## Worked example`, `## Key ideas`, and a
`## Exercises` section containing a ` ```yaml ` list of exercises (each with `type`,
`difficulty`, `prompt`, `options`, `correct_answer`, `target_misconception`).

> Re-running the loader does a full reload and resets student progress (it's a
> seed-time operation), so load content before a demo, not during one.
