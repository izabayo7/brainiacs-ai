---
slug: recursion
name: Recursion
order: 6
prerequisites:
- functions
summary: Recursion is a function that calls itself on a smaller input
estimated_minutes: 20
---

## Explanation
**Recursion** is a function that calls itself on a smaller input. It needs a **base case** that stops the recursion, or it never ends.

## Worked example
```
FUNCTION factorial(n)
  IF n = 0 THEN RETURN 1      # base case
  RETURN n * factorial(n - 1)  # smaller subproblem
END FUNCTION
```

## Exercises
```yaml
- type: mcq
  difficulty: medium
  prompt: What does every recursion NEED to avoid running forever?
  options:
  - A loop
  - A base case that stops the recursion
  - A global variable
  - More memory
  correct_answer: A base case that stops the recursion
  target_misconception: recursion_no_base_case
- type: predict_output
  difficulty: hard
  prompt: "FUNCTION fact(n)\n  IF n = 0 THEN RETURN 1\n  RETURN n * fact(n - 1)\nEND FUNCTION\nPRINT fact(3)\n\
    What is printed?"
  correct_answer: '6'
  target_misconception: recursion_state_confusion
- type: mcq
  difficulty: hard
  prompt: A recursive function with NO base case will...
  options:
  - Return 0
  - Recurse forever (until it crashes)
  - Run exactly once
  - Skip the recursion
  correct_answer: Recurse forever (until it crashes)
  target_misconception: recursion_no_base_case
- type: predict_output
  difficulty: medium
  prompt: "FUNCTION countdown(n)\n  IF n = 0 THEN RETURN\n  PRINT n\n  countdown(n - 1)\nEND FUNCTION\n\
    countdown(3)\nWhat is printed, in order?"
  correct_answer: 3 2 1
  target_misconception: recursion_state_confusion
```
