---
slug: functions
name: Functions & Scope
order: 5
prerequisites:
- variables
summary: A function packages steps under a name and may take parameters
estimated_minutes: 20
---

## Explanation
A **function** packages steps under a name and may take **parameters**. A parameter is a local variable filled by the **argument** at the call site. Variables inside a function are local — invisible outside it.

## Worked example
```
FUNCTION square(n)
  RETURN n * n
END FUNCTION

result <- square(4)   # n=4 inside; result is 16
```

## Exercises
```yaml
- type: predict_output
  difficulty: medium
  prompt: "FUNCTION square(n)\n  RETURN n * n\nEND FUNCTION\nPRINT square(4)\nWhat is printed?"
  correct_answer: '16'
  target_misconception: scope_confusion
- type: mcq
  difficulty: hard
  prompt: A variable created INSIDE a function is...
  options:
  - visible everywhere in the program
  - local — only visible inside that function
  - automatically global
  - deleted before the function runs
  correct_answer: local — only visible inside that function
  target_misconception: scope_confusion
- type: mcq
  difficulty: medium
  prompt: In `square(4)`, what is 4 called?
  options:
  - A parameter
  - An argument
  - A return value
  - A loop
  correct_answer: An argument
  target_misconception: scope_confusion
- type: pseudocode_order
  difficulty: medium
  prompt: Arrange a function that doubles a number and prints the result.
  options:
  - PRINT result
  - FUNCTION double(n)
  - '  RETURN n + n'
  - END FUNCTION
  - result <- double(6)
  correct_answer:
  - FUNCTION double(n)
  - '  RETURN n + n'
  - END FUNCTION
  - result <- double(6)
  - PRINT result
  target_misconception: algorithm_sequencing_error
```
