---
slug: control-flow
name: Control Flow (Conditionals)
order: 3
prerequisites:
- variables
summary: Control flow chooses which steps run
estimated_minutes: 20
---

## Explanation
**Control flow** chooses which steps run. An `IF` checks a boolean condition; the body runs only when the condition is true. `=` compares, but storing uses `<-`.

## Worked example
```
IF temperature > 30 THEN
  PRINT "hot"
ELSE
  PRINT "mild"
END IF
```

## Exercises
```yaml
- type: predict_output
  difficulty: easy
  prompt: 'temperature <- 20

    IF temperature > 30 THEN PRINT "hot" ELSE PRINT "mild"

    What is printed?'
  correct_answer: mild
  target_misconception: boolean_logic_error
- type: mcq
  difficulty: medium
  prompt: When does the body of an IF statement run?
  options:
  - Always
  - Only when its condition is true
  - Only when its condition is false
  - Never
  correct_answer: Only when its condition is true
  target_misconception: boolean_logic_error
- type: predict_output
  difficulty: hard
  prompt: 'x <- 5

    IF x > 2 AND x < 4 THEN PRINT "yes" ELSE PRINT "no"

    What is printed?'
  correct_answer: 'no'
  target_misconception: boolean_logic_error
- type: mcq
  difficulty: medium
  prompt: Which operator COMPARES two values for equality?
  options:
  - <-
  - '='
  - +
  - PRINT
  correct_answer: '='
  target_misconception: assignment_as_equality
```
