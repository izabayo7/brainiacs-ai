# Brainiacs Content Format (the contract)

Every lesson is one human-authored Markdown file in `content/`. A lesson file is the
**single source of truth** for one concept and its exercises. Application code never
invents or edits content; it only parses, validates, and loads these files into
Postgres. If you want to change a lesson, edit the file and re-run the seeder.

## File naming

`<NN>-<slug>.md` — for example `01-algorithmic-thinking.md`.

- `NN` is a zero-padded ordering prefix (`01`, `02`, …).
- `slug` is kebab-case and globally unique across all lessons.

## File structure

Each file has three parts, in this order:

1. YAML front-matter between two `---` fences.
2. A Markdown body containing exactly these level-2 headings: `## Explanation`,
   `## Worked example`, `## Key ideas`.
3. A single fenced ` ```yaml ` block under a `## Exercises` heading.

### 1. Front-matter (all fields required)

| Field | Type | Rule |
|---|---|---|
| `slug` | string | kebab-case, globally unique |
| `name` | string | human-readable lesson title |
| `order` | integer | unique; must be greater than the `order` of every prerequisite |
| `prerequisites` | list of slugs | may be empty (`[]`); each entry must be an existing slug |
| `summary` | string | one sentence |
| `estimated_minutes` | integer | positive |

### 2. Body sections

- `## Explanation` — prose only.
- `## Worked example` — prose plus at least one fenced ` ```pseudocode ` block.
- `## Key ideas` — a Markdown bullet list of 3 to 5 items.

### 3. Exercises

Under `## Exercises`, one ` ```yaml ` block holding a list of **6 or more** exercises.

Fields shared by every exercise: `type`, `difficulty`, `prompt`,
`target_misconception`, `explanation`.

- `type` is one of: `mcq`, `predict_output`, `pseudocode_order`.
- `difficulty` is one of: `easy`, `medium`, `hard`.
- `target_misconception` is one of the values in the enum below.
- `explanation` is a short sentence naming the misconception or idea (never a full solution).

Per-type fields:

- `mcq`: `options` (a list of 2 to 4 strings) and `correct_answer` (a string that
  exactly equals one of the `options`).
- `predict_output`: `correct_answer` (a string). No `options`.
- `pseudocode_order`: `options` (a list of strings, shown shuffled to the learner) and
  `correct_answer` (a list that is a permutation of `options` — same items, correct order).

## Misconception enum

Active values:

`variable_name_semantics`, `assignment_as_equality`, `loop_boundary_offbyone`,
`loop_execution_model`, `scope_confusion`, `recursion_no_base_case`,
`recursion_state_confusion`, `array_index_value_confusion`, `boolean_logic_error`,
`algorithm_sequencing_error`, `type_confusion`, `tracing_error`, `none`.

Note: `type_confusion` (data-types lesson) and `tracing_error` (flowcharts /
hand-tracing) were added to the original 11-label spec. The misconception classifier's
label set and the BKT skill map must include these two before the first seed.

## Pseudocode house style (used in all lessons)

- Assignment: `<-`. Comparison/equality: `=`. Relational: `<`, `>`, `<=`, `>=`, `!=`.
- Keywords in UPPERCASE: `INPUT`, `OUTPUT`, `IF`/`THEN`/`ELSE`/`END IF`,
  `FOR`/`END FOR`, `WHILE`/`END WHILE`, `REPEAT`/`UNTIL`,
  `FUNCTION`/`RETURN`/`END FUNCTION`.
- Arrays are 0-based. Comments use `//`.
- Pedagogical rule: a construct must not appear in a lesson before the lesson that
  teaches it (no `IF` or comparisons in the linear-foundation lessons, etc.). This is
  enforced by author review, not by the validator.

## Validation rules (the validator FAILS the build on any of these)

1. Front-matter has all required fields with correct types.
2. `slug` is kebab-case and unique across all files.
3. Every entry in `prerequisites` resolves to an existing `slug`.
4. The prerequisite graph is acyclic (a topological sort must succeed).
5. Each lesson's `order` is greater than the `order` of all its prerequisites.
6. The three body sections are present, and `## Worked example` contains a
   ` ```pseudocode ` block.
7. There are 6 or more exercises.
8. Every exercise has a valid `type`, `difficulty`, and `target_misconception`, plus a
   non-empty `prompt` and `explanation`.
9. `mcq`: `correct_answer` equals exactly one of `options`.
10. `pseudocode_order`: `correct_answer` is a permutation of `options` (same multiset).
11. `predict_output`: `correct_answer` is a non-empty string.

The validator should also WARN (not fail) when a lesson has no exercise of a given type,
or no `hard` exercise, so authors keep a healthy spread.

## How content becomes data

`parser` (Markdown → structured objects) → `validator` (enforces this contract) →
`loader` (idempotent upsert into Postgres, keyed by `slug` for concepts and a stable key
for exercises). Re-running the loader updates existing rows; it never duplicates.
Content loading is a **seeder**, separate from Alembic schema migrations.

## Flowcharts and other visuals

Lessons and exercises may include flowcharts that the frontend draws. A flowchart is
written as a fenced ` ```flowchart ` block containing JSON with `nodes` and `edges`. The
renderer draws it with light fills and black strokes, matching the printed-manual style;
authors never paste image files.

- Node: `{ "id": string, "shape": "terminal"|"io"|"process"|"decision"|"connector", "text": string }`
- Edge: `{ "from": nodeId, "to": nodeId, "label"?: string }` (the optional `label` is for
  the yes/no branches of a decision, which is only used from the conditionals lesson on)

Shape meanings: `terminal` = oval (start/end), `io` = parallelogram (input/output),
`process` = rectangle (a calculation or assignment), `decision` = diamond (a choice; not
used before the conditionals lesson), `connector` = small circle (page link).

A ` ```flowchart ` block that has `nodes` and no `edges` renders as a labelled **legend**,
used to show the symbol reference.

Validator additions: every ` ```flowchart ` block must be valid JSON; each `shape` must be
in the enum above; each edge `from` and `to` must reference an existing node `id`.

## Visual exercise fields (all optional)

- `prompt_diagram`: a flowchart spec object (`{ "nodes": [...], "edges": [...] }`, same
  schema as the ` ```flowchart ` block) shown above the exercise prompt, so an `mcq` or
  `predict_output` can ask the learner to read or trace a flowchart.
- On a `pseudocode_order` exercise, `format: "flowchart"` tells the engine to render the
  orderable items as draggable flowchart boxes. When `format` is `"flowchart"`, each entry
  in `options` and `correct_answer` is an object `{ "shape": ..., "text": ... }` instead of
  a plain string, and `correct_answer` is still a permutation of `options`. When `format`
  is absent or `"text"`, items are plain strings as before.