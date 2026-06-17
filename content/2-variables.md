---
slug: variables
name: Variables & Assignment
order: 2
prerequisites:
- algorithmic-thinking
summary: A variable is a named box that stores a value
estimated_minutes: 20
---

## Explanation
A **variable** is a named box that stores a value. Assignment `x <- 5` *puts* 5 into the box `x`. The name is for humans; the computer does not read meaning from it. `=` here means *store into*, not *is equal to*.

## Worked example
```
x <- 3
y <- x      # y now holds 3 (a copy)
x <- 10     # x is 10; y is still 3
```

## Exercises
```yaml
- type: predict_output
  difficulty: medium
  prompt: 'x <- 3

    y <- x

    x <- 10

    PRINT y

    What is printed?'
  correct_answer: '3'
  target_misconception: assignment_as_equality
- type: mcq
  difficulty: easy
  prompt: Does the computer understand what a variable NAMED 'speed' means?
  options:
  - Yes, it knows it is about speed
  - No, the name is only a label for humans; the value is what matters
  - Only if the value is a number
  - Only in fast programs
  correct_answer: No, the name is only a label for humans; the value is what matters
  target_misconception: variable_name_semantics
- type: predict_output
  difficulty: medium
  prompt: 'a <- 5

    b <- 2

    a <- a + b

    PRINT a

    What is printed?'
  correct_answer: '7'
  target_misconception: assignment_as_equality
- type: mcq
  difficulty: hard
  prompt: What does `count <- count + 1` do?
  options:
  - Claims count equals count plus one (impossible)
  - Stores the current value of count plus one back into count
  - Creates a new variable
  - Nothing; it is an error
  correct_answer: Stores the current value of count plus one back into count
  target_misconception: assignment_as_equality
```
