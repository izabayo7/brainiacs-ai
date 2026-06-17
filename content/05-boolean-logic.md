---
slug: boolean-logic
name: Boolean Logic & Expressions
order: 5
prerequisites: [data-and-types]
summary: How a program produces true or false answers by comparing values, and how to combine those answers with AND, OR, and NOT.
estimated_minutes: 30
---

## Explanation

Every day you ask yourself small yes-or-no questions to decide what to do. Is it raining? Am I old enough to vote? Do I have enough money for this? Each question has only two possible answers, yes or no, true or false. In the data-types lesson you met the **boolean**, a value that is only ever true or false. This lesson is about how a program *produces* those true-or-false answers and how it *combines* them. We are only building and reading the questions here; making the program act on them comes in the next lesson.

The simplest way to get a true-or-false answer is to **compare** two values. A comparison uses a relational operator and always produces a boolean. The operators are `=` (is equal to), `!=` (is not equal to), `<` (less than), `>` (greater than), `<=` (less than or equal to, that is, "at most"), and `>=` (greater than or equal to, "at least"). So `age >= 18` is a boolean expression: for an age of 20 it is true, and for 15 it is false. Notice that `=` here asks a question, "is this equal to that?", and is completely different from the assignment arrow `<-` from the variables lesson, which stores a value. One asks, the other stores.

To build richer questions you combine booleans with three **logical operators**. `AND` gives true only when both of its parts are true. `OR` gives true when at least one part is true. `NOT` flips a value, turning true into false and false into true. The exact behaviour of each operator is captured in a **truth table**, which simply lists every possible combination of inputs and the result.

| a | b | a AND b | a OR b |
|---|---|---|---|
| true | true | true | true |
| true | false | false | true |
| false | true | false | true |
| false | false | false | false |

| a | NOT a |
|---|---|
| true | false |
| false | true |

Two traps catch almost every beginner, and a truth table is how you check yourself. The first comes from everyday speech. We say "I want a number between 1 and 10", and it is tempting to write `x > 1 OR x < 10`, but that is true for almost every number you could pick. The correct condition is `x >= 1 AND x <= 10`, because *both* limits must hold at the same time, which is what `AND` means. The second trap is that `NOT` applies to a whole expression: `NOT (a AND b)` is not the same as `NOT a AND b`, so use brackets and read carefully.

Why does all this matter? Because these true-or-false expressions are the questions your program will ask just before it makes a choice, or decides whether to keep repeating. Everything in the next two lessons rests on being able to write and evaluate a boolean expression correctly.

## Worked example

Problem: decide whether a person qualifies for a teen discount, which applies to ages 13 to 19 inclusive.

The condition has two halves: the age must be at least 13, and it must be at most 19. Both must hold, so we join them with `AND`.

```pseudocode
INPUT age

// build one boolean from two comparisons
isTeen <- (age >= 13) AND (age <= 19)

OUTPUT isTeen
```

Trace it for `age = 15`. The left comparison `15 >= 13` is true. The right comparison `15 <= 19` is true. Looking at the `AND` column of the truth table, true AND true gives true, so `isTeen` becomes true. Now trace `age = 25`. The left part `25 >= 13` is true, but the right part `25 <= 19` is false, and true AND false gives false, so `isTeen` becomes false. The truth table did the deciding for us; we only had to read the right row.

## Key ideas

- A boolean expression evaluates to true or false; the simplest kind is a comparison (`=`, `!=`, `<`, `>`, `<=`, `>=`) between two values.
- The comparison `=` asks "is this equal to that?" and gives true or false; it is not the assignment arrow `<-`, which stores a value.
- `AND` is true only when both parts are true; `OR` is true when at least one part is true; `NOT` flips true and false.
- A truth table lists every combination and its result, and a range like "between 13 and 19" needs `AND` with both limits, not `OR`.

## Exercises

```yaml
- type: mcq
  difficulty: easy
  prompt: "What does the expression 5 > 3 evaluate to?"
  options: ["true", "false", "5", "3"]
  correct_answer: "true"
  target_misconception: none
  explanation: "5 is greater than 3, so the comparison is true; a comparison gives a boolean, not a number."
- type: mcq
  difficulty: easy
  prompt: "For an AND expression to be true, how many of its two parts must be true?"
  options: ["Both parts", "At least one part", "Exactly one part", "Neither part"]
  correct_answer: "Both parts"
  target_misconception: boolean_logic_error
  explanation: "AND requires both parts true; 'at least one' describes OR."
- type: mcq
  difficulty: easy
  prompt: "For an OR expression to be true, how many of its two parts must be true?"
  options: ["At least one part", "Both parts", "Neither part", "Exactly two parts"]
  correct_answer: "At least one part"
  target_misconception: boolean_logic_error
  explanation: "OR is true when one or both parts are true; requiring both describes AND."
- type: mcq
  difficulty: easy
  prompt: "What does the operator NOT do to a boolean value?"
  options: ["Flips it: true becomes false and false becomes true", "Always makes it false", "Always makes it true", "Leaves it unchanged"]
  correct_answer: "Flips it: true becomes false and false becomes true"
  target_misconception: boolean_logic_error
  explanation: "NOT reverses the truth value."
- type: predict_output
  difficulty: medium
  prompt: "State whether this outputs true or false.\n\nOUTPUT (4 > 2) AND (2 > 5)"
  correct_answer: "false"
  target_misconception: boolean_logic_error
  explanation: "4 > 2 is true but 2 > 5 is false, and AND with any false part is false."
- type: predict_output
  difficulty: medium
  prompt: "State whether this outputs true or false.\n\nOUTPUT NOT (3 = 3)"
  correct_answer: "false"
  target_misconception: boolean_logic_error
  explanation: "3 = 3 is true, and NOT flips true to false."
- type: predict_output
  difficulty: medium
  prompt: "State whether this outputs true or false.\n\nage <- 15\nOUTPUT (age >= 13) AND (age <= 19)"
  correct_answer: "true"
  target_misconception: boolean_logic_error
  explanation: "15 >= 13 is true and 15 <= 19 is true, so AND gives true."
- type: mcq
  difficulty: medium
  prompt: "Which expression correctly means 'x is between 1 and 10, inclusive'?"
  options: ["x >= 1 AND x <= 10", "x >= 1 OR x <= 10", "x > 1 AND x > 10", "x = 1 AND x = 10"]
  correct_answer: "x >= 1 AND x <= 10"
  target_misconception: boolean_logic_error
  explanation: "Both limits must hold at once, so it needs AND; OR would be true for almost every number."
- type: mcq
  difficulty: medium
  prompt: "What is the difference between = and <- in these lessons?"
  options: ["= asks whether two values are equal (giving true or false); <- stores a value in a variable", "They are the same thing", "= stores a value; <- compares two values", "= is for numbers and <- is for text"]
  correct_answer: "= asks whether two values are equal (giving true or false); <- stores a value in a variable"
  target_misconception: assignment_as_equality
  explanation: "Comparison asks a question and yields a boolean; assignment stores a value. They are different operations."
- type: pseudocode_order
  difficulty: medium
  prompt: "Arrange these lines into a correct algorithm that reads two numbers and outputs whether the first is greater than the second."
  options: ["OUTPUT isGreater", "INPUT a", "isGreater <- a > b", "INPUT b"]
  correct_answer: ["INPUT a", "INPUT b", "isGreater <- a > b", "OUTPUT isGreater"]
  target_misconception: algorithm_sequencing_error
  explanation: "Both numbers must be read before they can be compared, and the comparison made before its result is shown."
- type: predict_output
  difficulty: medium
  prompt: "State whether this outputs true or false.\n\nOUTPUT (5 > 3) OR (2 > 9)"
  correct_answer: "true"
  target_misconception: boolean_logic_error
  explanation: "5 > 3 is true, and OR needs only one true part."
- type: mcq
  difficulty: hard
  prompt: "Which expression is equivalent to NOT (a AND b)?"
  options: ["(NOT a) OR (NOT b)", "(NOT a) AND (NOT b)", "a OR b", "a AND b"]
  correct_answer: "(NOT a) OR (NOT b)"
  target_misconception: boolean_logic_error
  explanation: "Negating an AND turns it into an OR of the negated parts; checking all four truth-table rows confirms this."
```
