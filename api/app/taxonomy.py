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
    "none",                         # answer correct, no misconception
]

MISCONCEPTION_SET = set(MISCONCEPTION_LABELS)


def is_valid_label(label: str | None) -> bool:
    return label in MISCONCEPTION_SET
