---
slug: loops
name: Loops & Iteration
order: 4
prerequisites:
- control-flow
summary: A loop repeats its body
estimated_minutes: 20
---

## Explanation
A **loop** repeats its body. The body runs once per iteration — not all at once. Watch the boundaries: `FOR i FROM 1 TO 5` runs five times.

## Worked example
```
total <- 0
FOR i FROM 1 TO 3 DO
  total <- total + i   # 1, then 3, then 6
END FOR
```

## Exercises
```yaml
- type: predict_output
  difficulty: medium
  prompt: "total <- 0\nFOR i FROM 1 TO 3 DO\n  total <- total + i\nEND FOR\nPRINT total\nWhat is printed?"
  correct_answer: '6'
  target_misconception: loop_execution_model
- type: mcq
  difficulty: medium
  prompt: How many times does `FOR i FROM 1 TO 5` run its body?
  options:
  - '4'
  - '5'
  - '6'
  - Infinite
  correct_answer: '5'
  target_misconception: loop_boundary_offbyone
- type: mcq
  difficulty: hard
  prompt: In a loop, the body...
  options:
  - runs all iterations simultaneously
  - runs once per iteration, in sequence
  - runs only the last iteration
  - never runs
  correct_answer: runs once per iteration, in sequence
  target_misconception: loop_execution_model
- type: predict_output
  difficulty: hard
  prompt: "count <- 0\nFOR i FROM 0 TO 4 DO\n  count <- count + 1\nEND FOR\nPRINT count\nWhat is printed?"
  correct_answer: '5'
  target_misconception: loop_boundary_offbyone
```
