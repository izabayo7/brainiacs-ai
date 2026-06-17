---
slug: algorithmic-thinking
name: Algorithmic Thinking
order: 1
prerequisites: []
summary: An algorithm is a finite, ordered list of unambiguous steps that solves a
  problem
estimated_minutes: 20
---

## Explanation
An **algorithm** is a finite, ordered list of unambiguous steps that solves a problem. Order matters: the same steps in a different order can give a different result.

## Worked example
```
MAKE TEA:
  1. Boil water
  2. Put teabag in cup
  3. Pour water into cup
  4. Wait 3 minutes
  5. Remove teabag
```
Swapping steps 3 and 5 ruins the tea.

## Exercises
```yaml
- type: mcq
  difficulty: easy
  prompt: Which best describes an algorithm?
  options:
  - A programming language
  - A finite, ordered list of unambiguous steps to solve a problem
  - A type of computer
  - A single mathematical equation
  correct_answer: A finite, ordered list of unambiguous steps to solve a problem
- type: pseudocode_order
  difficulty: medium
  prompt: Arrange these steps into a correct 'make tea' algorithm.
  options:
  - Pour water into cup
  - Boil water
  - Remove teabag
  - Put teabag in cup
  correct_answer:
  - Boil water
  - Put teabag in cup
  - Pour water into cup
  - Remove teabag
  target_misconception: algorithm_sequencing_error
- type: mcq
  difficulty: medium
  prompt: Why does the ORDER of steps matter in an algorithm?
  options:
  - It does not matter at all
  - Because computers are slow
  - Because different orders can produce different results
  - Only the first step matters
  correct_answer: Because different orders can produce different results
  target_misconception: algorithm_sequencing_error
- type: predict_output
  difficulty: easy
  prompt: 'Steps: (1) Write ''A'' (2) Write ''B''. What is printed, in order?'
  correct_answer: AB
```
