"""Seed a small, real slice of curriculum so the demo isn't empty.

Run with:  python -m app.seed   (from the api/ directory, with DATABASE_URL set)

Idempotent: clears the content + student tables and reinserts. Safe to re-run.
Exercises double as the deterministic fallback when LLM quiz-gen is unavailable.
"""
from __future__ import annotations

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
    Student,
)

# --- Concepts (a small real prerequisite DAG) --------------------------------
# Algorithmic Thinking -> Variables -> Control Flow -> Loops
#                         Variables -> Functions -> Recursion
CONCEPTS = [
    {
        "slug": "algorithmic-thinking",
        "name": "Algorithmic Thinking",
        "order_hint": 1,
        "explanation_md": (
            "An **algorithm** is a finite, ordered list of unambiguous steps that "
            "solves a problem. Order matters: the same steps in a different order "
            "can give a different result."
        ),
        "worked_example_md": (
            "```\nMAKE TEA:\n  1. Boil water\n  2. Put teabag in cup\n  3. Pour water into cup\n"
            "  4. Wait 3 minutes\n  5. Remove teabag\n```\nSwapping steps 3 and 5 ruins the tea."
        ),
        "prereqs": [],
    },
    {
        "slug": "variables",
        "name": "Variables & Assignment",
        "order_hint": 2,
        "explanation_md": (
            "A **variable** is a named box that stores a value. Assignment `x <- 5` "
            "*puts* 5 into the box `x`. The name is for humans; the computer does not "
            "read meaning from it. `=` here means *store into*, not *is equal to*."
        ),
        "worked_example_md": (
            "```\nx <- 3\ny <- x      # y now holds 3 (a copy)\nx <- 10     # x is 10; y is still 3\n```"
        ),
        "prereqs": ["algorithmic-thinking"],
    },
    {
        "slug": "control-flow",
        "name": "Control Flow (Conditionals)",
        "order_hint": 3,
        "explanation_md": (
            "**Control flow** chooses which steps run. An `IF` checks a boolean "
            "condition; the body runs only when the condition is true. `=` compares, "
            "but storing uses `<-`."
        ),
        "worked_example_md": (
            "```\nIF temperature > 30 THEN\n  PRINT \"hot\"\nELSE\n  PRINT \"mild\"\nEND IF\n```"
        ),
        "prereqs": ["variables"],
    },
    {
        "slug": "loops",
        "name": "Loops & Iteration",
        "order_hint": 4,
        "explanation_md": (
            "A **loop** repeats its body. The body runs once per iteration — not all "
            "at once. Watch the boundaries: `FOR i FROM 1 TO 5` runs five times."
        ),
        "worked_example_md": (
            "```\ntotal <- 0\nFOR i FROM 1 TO 3 DO\n  total <- total + i   # 1, then 3, then 6\nEND FOR\n```"
        ),
        "prereqs": ["control-flow"],
    },
    {
        "slug": "functions",
        "name": "Functions & Scope",
        "order_hint": 5,
        "explanation_md": (
            "A **function** packages steps under a name and may take **parameters**. "
            "A parameter is a local variable filled by the **argument** at the call "
            "site. Variables inside a function are local — invisible outside it."
        ),
        "worked_example_md": (
            "```\nFUNCTION square(n)\n  RETURN n * n\nEND FUNCTION\n\nresult <- square(4)   # n=4 inside; result is 16\n```"
        ),
        "prereqs": ["variables"],
    },
    {
        "slug": "recursion",
        "name": "Recursion",
        "order_hint": 6,
        "explanation_md": (
            "**Recursion** is a function that calls itself on a smaller input. It needs "
            "a **base case** that stops the recursion, or it never ends."
        ),
        "worked_example_md": (
            "```\nFUNCTION factorial(n)\n  IF n = 0 THEN RETURN 1      # base case\n"
            "  RETURN n * factorial(n - 1)  # smaller subproblem\nEND FUNCTION\n```"
        ),
        "prereqs": ["functions"],
    },
]


def _chapter_for(slug: str, name: str, explanation: str, example: str) -> dict:
    return {
        "title": f"{name} — Chapter 1",
        "body_md": f"## {name}\n\n{explanation}\n\n### Worked example\n\n{example}\n",
        "video_url": None,
    }


# --- Exercises: 4-6 per concept, across the three pseudocode-safe types -------
EXERCISES: dict[str, list[dict]] = {
    "algorithmic-thinking": [
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.easy,
            "prompt": "Which best describes an algorithm?",
            "options_json": [
                "A programming language",
                "A finite, ordered list of unambiguous steps to solve a problem",
                "A type of computer",
                "A single mathematical equation",
            ],
            "correct_answer_json": "A finite, ordered list of unambiguous steps to solve a problem",
            "target_misconception": None,
        },
        {
            "type": ExerciseType.pseudocode_order,
            "difficulty": Difficulty.medium,
            "prompt": "Arrange these steps into a correct 'make tea' algorithm.",
            "options_json": [
                "Pour water into cup",
                "Boil water",
                "Remove teabag",
                "Put teabag in cup",
            ],
            "correct_answer_json": [
                "Boil water",
                "Put teabag in cup",
                "Pour water into cup",
                "Remove teabag",
            ],
            "target_misconception": "algorithm_sequencing_error",
        },
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.medium,
            "prompt": "Why does the ORDER of steps matter in an algorithm?",
            "options_json": [
                "It does not matter at all",
                "Because computers are slow",
                "Because different orders can produce different results",
                "Only the first step matters",
            ],
            "correct_answer_json": "Because different orders can produce different results",
            "target_misconception": "algorithm_sequencing_error",
        },
        {
            "type": ExerciseType.predict_output,
            "difficulty": Difficulty.easy,
            "prompt": "Steps: (1) Write 'A' (2) Write 'B'. What is printed, in order?",
            "options_json": None,
            "correct_answer_json": "AB",
            "target_misconception": None,
        },
    ],
    "variables": [
        {
            "type": ExerciseType.predict_output,
            "difficulty": Difficulty.medium,
            "prompt": "x <- 3\ny <- x\nx <- 10\nPRINT y\nWhat is printed?",
            "options_json": None,
            "correct_answer_json": "3",
            "target_misconception": "assignment_as_equality",
        },
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.easy,
            "prompt": "Does the computer understand what a variable NAMED 'speed' means?",
            "options_json": [
                "Yes, it knows it is about speed",
                "No, the name is only a label for humans; the value is what matters",
                "Only if the value is a number",
                "Only in fast programs",
            ],
            "correct_answer_json": "No, the name is only a label for humans; the value is what matters",
            "target_misconception": "variable_name_semantics",
        },
        {
            "type": ExerciseType.predict_output,
            "difficulty": Difficulty.medium,
            "prompt": "a <- 5\nb <- 2\na <- a + b\nPRINT a\nWhat is printed?",
            "options_json": None,
            "correct_answer_json": "7",
            "target_misconception": "assignment_as_equality",
        },
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.hard,
            "prompt": "What does `count <- count + 1` do?",
            "options_json": [
                "Claims count equals count plus one (impossible)",
                "Stores the current value of count plus one back into count",
                "Creates a new variable",
                "Nothing; it is an error",
            ],
            "correct_answer_json": "Stores the current value of count plus one back into count",
            "target_misconception": "assignment_as_equality",
        },
    ],
    "control-flow": [
        {
            "type": ExerciseType.predict_output,
            "difficulty": Difficulty.easy,
            "prompt": "temperature <- 20\nIF temperature > 30 THEN PRINT \"hot\" ELSE PRINT \"mild\"\nWhat is printed?",
            "options_json": None,
            "correct_answer_json": "mild",
            "target_misconception": "boolean_logic_error",
        },
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.medium,
            "prompt": "When does the body of an IF statement run?",
            "options_json": [
                "Always",
                "Only when its condition is true",
                "Only when its condition is false",
                "Never",
            ],
            "correct_answer_json": "Only when its condition is true",
            "target_misconception": "boolean_logic_error",
        },
        {
            "type": ExerciseType.predict_output,
            "difficulty": Difficulty.hard,
            "prompt": "x <- 5\nIF x > 2 AND x < 4 THEN PRINT \"yes\" ELSE PRINT \"no\"\nWhat is printed?",
            "options_json": None,
            "correct_answer_json": "no",
            "target_misconception": "boolean_logic_error",
        },
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.medium,
            "prompt": "Which operator COMPARES two values for equality?",
            "options_json": ["<-", "=", "+", "PRINT"],
            "correct_answer_json": "=",
            "target_misconception": "assignment_as_equality",
        },
    ],
    "loops": [
        {
            "type": ExerciseType.predict_output,
            "difficulty": Difficulty.medium,
            "prompt": "total <- 0\nFOR i FROM 1 TO 3 DO\n  total <- total + i\nEND FOR\nPRINT total\nWhat is printed?",
            "options_json": None,
            "correct_answer_json": "6",
            "target_misconception": "loop_execution_model",
        },
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.medium,
            "prompt": "How many times does `FOR i FROM 1 TO 5` run its body?",
            "options_json": ["4", "5", "6", "Infinite"],
            "correct_answer_json": "5",
            "target_misconception": "loop_boundary_offbyone",
        },
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.hard,
            "prompt": "In a loop, the body...",
            "options_json": [
                "runs all iterations simultaneously",
                "runs once per iteration, in sequence",
                "runs only the last iteration",
                "never runs",
            ],
            "correct_answer_json": "runs once per iteration, in sequence",
            "target_misconception": "loop_execution_model",
        },
        {
            "type": ExerciseType.predict_output,
            "difficulty": Difficulty.hard,
            "prompt": "count <- 0\nFOR i FROM 0 TO 4 DO\n  count <- count + 1\nEND FOR\nPRINT count\nWhat is printed?",
            "options_json": None,
            "correct_answer_json": "5",
            "target_misconception": "loop_boundary_offbyone",
        },
    ],
    "functions": [
        {
            "type": ExerciseType.predict_output,
            "difficulty": Difficulty.medium,
            "prompt": "FUNCTION square(n)\n  RETURN n * n\nEND FUNCTION\nPRINT square(4)\nWhat is printed?",
            "options_json": None,
            "correct_answer_json": "16",
            "target_misconception": "scope_confusion",
        },
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.hard,
            "prompt": "A variable created INSIDE a function is...",
            "options_json": [
                "visible everywhere in the program",
                "local — only visible inside that function",
                "automatically global",
                "deleted before the function runs",
            ],
            "correct_answer_json": "local — only visible inside that function",
            "target_misconception": "scope_confusion",
        },
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.medium,
            "prompt": "In `square(4)`, what is 4 called?",
            "options_json": ["A parameter", "An argument", "A return value", "A loop"],
            "correct_answer_json": "An argument",
            "target_misconception": "scope_confusion",
        },
        {
            "type": ExerciseType.pseudocode_order,
            "difficulty": Difficulty.medium,
            "prompt": "Arrange a function that doubles a number and prints the result.",
            "options_json": [
                "PRINT result",
                "FUNCTION double(n)",
                "  RETURN n + n",
                "END FUNCTION",
                "result <- double(6)",
            ],
            "correct_answer_json": [
                "FUNCTION double(n)",
                "  RETURN n + n",
                "END FUNCTION",
                "result <- double(6)",
                "PRINT result",
            ],
            "target_misconception": "algorithm_sequencing_error",
        },
    ],
    "recursion": [
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.medium,
            "prompt": "What does every recursion NEED to avoid running forever?",
            "options_json": [
                "A loop",
                "A base case that stops the recursion",
                "A global variable",
                "More memory",
            ],
            "correct_answer_json": "A base case that stops the recursion",
            "target_misconception": "recursion_no_base_case",
        },
        {
            "type": ExerciseType.predict_output,
            "difficulty": Difficulty.hard,
            "prompt": "FUNCTION fact(n)\n  IF n = 0 THEN RETURN 1\n  RETURN n * fact(n - 1)\nEND FUNCTION\nPRINT fact(3)\nWhat is printed?",
            "options_json": None,
            "correct_answer_json": "6",
            "target_misconception": "recursion_state_confusion",
        },
        {
            "type": ExerciseType.mcq,
            "difficulty": Difficulty.hard,
            "prompt": "A recursive function with NO base case will...",
            "options_json": [
                "Return 0",
                "Recurse forever (until it crashes)",
                "Run exactly once",
                "Skip the recursion",
            ],
            "correct_answer_json": "Recurse forever (until it crashes)",
            "target_misconception": "recursion_no_base_case",
        },
        {
            "type": ExerciseType.predict_output,
            "difficulty": Difficulty.medium,
            "prompt": "FUNCTION countdown(n)\n  IF n = 0 THEN RETURN\n  PRINT n\n  countdown(n - 1)\nEND FUNCTION\ncountdown(3)\nWhat is printed, in order?",
            "options_json": None,
            "correct_answer_json": "3 2 1",
            "target_misconception": "recursion_state_confusion",
        },
    ],
}

STUDENTS = [
    {"name": "Ada Demo", "email": "ada@example.com"},
    {"name": "Grace Demo", "email": "grace@example.com"},
]


def seed() -> None:
    Base.metadata.create_all(engine)  # safety net if migrations weren't run
    db = SessionLocal()
    try:
        # Clear in FK-safe order.
        db.execute(delete(Attempt))
        db.execute(delete(MasteryEstimate))
        db.execute(delete(Exercise))
        db.execute(delete(Chapter))
        db.execute(delete(ConceptPrerequisite))
        db.execute(delete(Concept))
        db.execute(delete(Student))
        db.commit()

        slug_to_id: dict[str, int] = {}
        for spec in CONCEPTS:
            concept = Concept(
                slug=spec["slug"],
                name=spec["name"],
                order_hint=spec["order_hint"],
                explanation_md=spec["explanation_md"],
                worked_example_md=spec["worked_example_md"],
            )
            db.add(concept)
            db.flush()
            slug_to_id[spec["slug"]] = concept.id

            db.add(
                Chapter(
                    concept_id=concept.id,
                    **_chapter_for(
                        spec["slug"], spec["name"],
                        spec["explanation_md"], spec["worked_example_md"],
                    ),
                )
            )

        # Prerequisite edges.
        for spec in CONCEPTS:
            for prereq_slug in spec["prereqs"]:
                db.add(
                    ConceptPrerequisite(
                        concept_id=slug_to_id[spec["slug"]],
                        prerequisite_concept_id=slug_to_id[prereq_slug],
                    )
                )

        # Exercises.
        for slug, items in EXERCISES.items():
            for item in items:
                db.add(Exercise(concept_id=slug_to_id[slug], **item))

        # Students.
        for s in STUDENTS:
            db.add(Student(**s))

        db.commit()
        print(
            f"Seeded {len(CONCEPTS)} concepts, "
            f"{sum(len(v) for v in EXERCISES.values())} exercises, "
            f"{len(STUDENTS)} students."
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
