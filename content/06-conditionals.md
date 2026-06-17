---
slug: conditionals
name: Conditionals (Selection)
order: 6
prerequisites: [boolean-logic, flowcharts-tracing]
summary: How a program chooses what to do based on a true or false condition, using IF, ELSE, and nested decisions, drawn with the decision diamond.
estimated_minutes: 35
---

## Explanation

Every algorithm so far ran straight through: each step happened, every time, in order. But real problems need **choices**. If it is raining you take an umbrella, otherwise you wear sunglasses. You do one thing or another depending on the answer to a yes-or-no question. Making a choice based on a true-or-false condition is called **selection**, or branching, and it is exactly where the boolean expressions from the last lesson get used.

The simplest form is `IF ... THEN ... END IF`. It runs the steps inside only when the condition is true. If the condition is false, those steps are skipped completely and the program carries on from after `END IF`. So `IF score >= 50 THEN OUTPUT "Pass" END IF` shows "Pass" only when the score is at least 50; for any lower score, nothing is shown and the program moves on.

More often you want to choose between two paths, and for that you add `ELSE`. With `IF ... THEN ... ELSE ... END IF`, the steps after `THEN` run when the condition is true, and the steps after `ELSE` run when it is false. The single most important fact about this is that **exactly one** of the two branches runs, never both and never neither. A common beginner mistake is to imagine both branches happen; they do not. The condition decides which single path is taken.

In a flowchart, a choice is drawn with the **decision** shape, a diamond. It has one arrow coming in and two arrows going out, labelled Yes and No (or true and false). The two paths do their separate work and then rejoin afterwards. Here is the flowchart for choosing the larger of two numbers:

```flowchart
{
  "nodes": [
    {"id": "s", "shape": "terminal", "text": "Start"},
    {"id": "i1", "shape": "io", "text": "INPUT num1"},
    {"id": "i2", "shape": "io", "text": "INPUT num2"},
    {"id": "d", "shape": "decision", "text": "num1 > num2 ?"},
    {"id": "o1", "shape": "io", "text": "OUTPUT num1"},
    {"id": "o2", "shape": "io", "text": "OUTPUT num2"},
    {"id": "e", "shape": "terminal", "text": "End"}
  ],
  "edges": [
    {"from": "s", "to": "i1"},
    {"from": "i1", "to": "i2"},
    {"from": "i2", "to": "d"},
    {"from": "d", "to": "o1", "label": "Yes"},
    {"from": "d", "to": "o2", "label": "No"},
    {"from": "o1", "to": "e"},
    {"from": "o2", "to": "e"}
  ]
}
```

When you must choose among more than two options, you chain conditions with `ELSE IF`, which makes a ladder. The program checks each condition in order and takes the **first one that is true**, skipping all the rest. If none are true, the final `ELSE` runs. A grade boundary is the classic case: check `score >= 80` first, then `score >= 60`, otherwise a fail. Getting the condition itself right still matters, because a wrong comparison sends the program down the wrong branch, so everything you learned about boolean expressions carries straight into this lesson.

## Worked example

Problem: read two numbers and output the larger one. The flowchart above shows it; here is the same algorithm in pseudocode.

```pseudocode
INPUT num1
INPUT num2
IF num1 > num2 THEN
    OUTPUT num1
ELSE
    OUTPUT num2
END IF
```

Trace it for `num1 = 8` and `num2 = 5`. The condition `8 > 5` is true, so the Yes branch runs and the program outputs 8; the ELSE branch is skipped entirely. Now trace `num1 = 3` and `num2 = 7`. The condition `3 > 7` is false, so the THEN branch is skipped and the ELSE branch runs, outputting 7. In both runs, exactly one branch executed.

For three numbers you nest the idea. Start by assuming the first is largest, then let each of the others challenge it:

```pseudocode
largest <- a
IF b > largest THEN
    largest <- b
END IF
IF c > largest THEN
    largest <- c
END IF
OUTPUT largest
```

## Key ideas

- Selection lets a program choose what to do based on a true-or-false condition; before this, algorithms ran every step every time.
- `IF ... THEN ... END IF` runs its steps only when the condition is true and skips them when false; adding `ELSE` chooses between two paths.
- Exactly one branch of an IF/ELSE runs: never both, never neither.
- In a flowchart, a decision is a diamond with one way in and two labelled ways out (Yes/No) that rejoin afterwards.
- An `ELSE IF` ladder checks conditions in order and takes the first one that is true, skipping the rest.

## Exercises

```yaml
- type: mcq
  difficulty: easy
  prompt: "What does selection (an IF statement) let a program do?"
  options: ["Choose what to do based on a true-or-false condition", "Repeat a step many times", "Store a value in a variable", "Read input from the user"]
  correct_answer: "Choose what to do based on a true-or-false condition"
  target_misconception: none
  explanation: "Selection is about making a choice; repeating is a different idea you meet later."
- type: mcq
  difficulty: easy
  prompt: "In an IF/THEN/ELSE statement, how many of the two branches run?"
  options: ["Exactly one", "Both of them", "Neither of them", "It depends on how long each branch is"]
  correct_answer: "Exactly one"
  target_misconception: conditional_flow_error
  explanation: "The condition selects a single branch; the other is skipped completely."
- type: mcq
  difficulty: easy
  prompt: "Which flowchart shape represents a decision?"
  options: ["A diamond", "A parallelogram", "An oval", "A rectangle"]
  correct_answer: "A diamond"
  target_misconception: none
  explanation: "A decision is a diamond with one entry and two labelled exits."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nnum1 <- 8\nnum2 <- 5\nIF num1 > num2 THEN\n    OUTPUT num1\nELSE\n    OUTPUT num2\nEND IF"
  correct_answer: "8"
  target_misconception: conditional_flow_error
  explanation: "8 > 5 is true, so only the THEN branch runs and outputs 8; the ELSE branch is skipped."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nx <- 5\nIF x > 10 THEN\n    x <- 0\nEND IF\nOUTPUT x"
  correct_answer: "5"
  target_misconception: conditional_flow_error
  explanation: "5 > 10 is false, so the THEN step is skipped and x keeps its value of 5."
- type: predict_output
  difficulty: medium
  prompt: "The user enters num1 = 8 and num2 = 5. Trace the flowchart shown and state what it outputs."
  prompt_diagram:
    nodes:
      - {id: s, shape: terminal, text: "Start"}
      - {id: i1, shape: io, text: "INPUT num1"}
      - {id: i2, shape: io, text: "INPUT num2"}
      - {id: d, shape: decision, text: "num1 > num2 ?"}
      - {id: o1, shape: io, text: "OUTPUT num1"}
      - {id: o2, shape: io, text: "OUTPUT num2"}
      - {id: e, shape: terminal, text: "End"}
    edges:
      - {from: s, to: i1}
      - {from: i1, to: i2}
      - {from: i2, to: d}
      - {from: d, to: o1, label: "Yes"}
      - {from: d, to: o2, label: "No"}
      - {from: o1, to: e}
      - {from: o2, to: e}
  correct_answer: "8"
  target_misconception: conditional_flow_error
  explanation: "The condition 8 > 5 is true, so the Yes path runs and outputs 8; the No path is not taken."
- type: mcq
  difficulty: medium
  prompt: "Which condition correctly tests whether age is a teenager (13 to 19 inclusive)?"
  options: ["age >= 13 AND age <= 19", "age >= 13 OR age <= 19", "age > 13 AND age < 19", "age = 13 AND age = 19"]
  correct_answer: "age >= 13 AND age <= 19"
  target_misconception: boolean_logic_error
  explanation: "Both limits must hold, so use AND with inclusive comparisons; a wrong condition sends the IF down the wrong branch."
- type: pseudocode_order
  difficulty: medium
  prompt: "Arrange these lines into a correct IF/ELSE that outputs Pass when score is at least 50, and Fail otherwise."
  options: ["ELSE", "IF score >= 50 THEN", "OUTPUT \"Fail\"", "END IF", "OUTPUT \"Pass\""]
  correct_answer: ["IF score >= 50 THEN", "OUTPUT \"Pass\"", "ELSE", "OUTPUT \"Fail\"", "END IF"]
  target_misconception: algorithm_sequencing_error
  explanation: "The THEN branch comes after the condition, the ELSE branch after it, and END IF closes the statement."
- type: mcq
  difficulty: medium
  prompt: "After an IF/ELSE finishes, which statements have executed?"
  options: ["Only the one branch whose side of the condition was taken", "Both branches, top to bottom", "Neither branch, since they are optional", "All statements, including those after END IF, only if the condition was true"]
  correct_answer: "Only the one branch whose side of the condition was taken"
  target_misconception: conditional_flow_error
  explanation: "Exactly one branch runs; statements after END IF always run regardless of the condition."
- type: predict_output
  difficulty: hard
  prompt: "Trace this and state what it outputs.\n\nscore <- 75\nIF score >= 80 THEN\n    grade <- \"A\"\nELSE IF score >= 60 THEN\n    grade <- \"B\"\nELSE\n    grade <- \"C\"\nEND IF\nOUTPUT grade"
  correct_answer: "B"
  target_misconception: conditional_flow_error
  explanation: "75 >= 80 is false, then 75 >= 60 is true, so grade becomes B and the final ELSE is skipped."
- type: predict_output
  difficulty: hard
  prompt: "Trace this and state what it outputs.\n\na <- 4\nb <- 9\nc <- 7\nlargest <- a\nIF b > largest THEN\n    largest <- b\nEND IF\nIF c > largest THEN\n    largest <- c\nEND IF\nOUTPUT largest"
  correct_answer: "9"
  target_misconception: conditional_flow_error
  explanation: "largest starts at 4; 9 > 4 is true so it becomes 9; 7 > 9 is false so it stays 9."
- type: mcq
  difficulty: hard
  prompt: "In an ELSE IF ladder, if more than one condition is true, which branch runs?"
  options: ["The first true one, and the rest are skipped", "Every branch whose condition is true", "The last true one", "None of them, because it is ambiguous"]
  correct_answer: "The first true one, and the rest are skipped"
  target_misconception: conditional_flow_error
  explanation: "The ladder is checked top to bottom and stops at the first true condition."
```
