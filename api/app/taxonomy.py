"""Fixed misconception taxonomy, grounded in Qian & Lehman (2017).

Shared single source of truth between the API and the ML notebook. These labels
are conceptual and pseudocode-safe (no language-specific syntax errors), so the
same scheme works whether the student writes pseudocode or answers conceptually.
"""
from __future__ import annotations

# Order matters only for stable display / confusion-matrix axes.
MISCONCEPTION_LABELS: list[str] = [
    "variable_name_semantics",      # thinks the computer reads meaning from variable names
    "assignment_as_equality",       # treats = as bidirectional/algebraic; confuses = vs ==
    "loop_boundary_offbyone",       # off-by-one in loop bounds
    "loop_execution_model",         # thinks the loop body runs all at once
    "scope_confusion",              # local vs global; params vs arguments
    "recursion_no_base_case",       # recursion without a terminating base case
    "recursion_state_confusion",    # misreads how recursive call state unwinds
    "array_index_value_confusion",  # index vs value; 0- vs 1-based indexing
    "boolean_logic_error",          # wrong boolean / comparison logic
    "algorithm_sequencing_error",   # wrong order of steps; comparison-swap mechanics
    "type_confusion",               # confuses data types (e.g. number vs text "5")
    "tracing_error",                # mis-traces step-by-step execution / hand-tracing
    "conditional_flow_error",       # misreads which IF/ELSE branch runs (control flow)
    "none",                         # answer correct, no misconception
]

MISCONCEPTION_SET = set(MISCONCEPTION_LABELS)

# Short, plain-language phrasing of each label — for showing the learner model to the
# student ("the system has noticed you tend to…").
MISCONCEPTION_HUMAN: dict[str, str] = {
    "variable_name_semantics": "reading meaning into variable names",
    "assignment_as_equality": "treating = as equality, not assignment",
    "loop_boundary_offbyone": "off-by-one in loop bounds",
    "loop_execution_model": "how a loop runs step by step",
    "scope_confusion": "variable scope (local vs global)",
    "recursion_no_base_case": "missing the recursion base case",
    "recursion_state_confusion": "how recursive calls unwind",
    "array_index_value_confusion": "index vs value in arrays",
    "boolean_logic_error": "boolean and comparison logic",
    "algorithm_sequencing_error": "the order of the steps",
    "type_confusion": "data types (a number vs the text \"5\")",
    "tracing_error": "hand-tracing execution line by line",
    "conditional_flow_error": "which IF/ELSE branch runs",
    "none": "no recurring difficulty",
}


def humanize(label: str | None) -> str:
    return MISCONCEPTION_HUMAN.get(label or "none", "a recurring difficulty")


def is_valid_label(label: str | None) -> bool:
    return label in MISCONCEPTION_SET
