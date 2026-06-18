---
slug: loops
name: Loops & Iteration
order: 7
prerequisites: [conditionals]
summary: How a program repeats a block of steps, using WHILE and FOR loops, counters and running totals, and how to trace a loop without losing track or running it one time too many.
estimated_minutes: 40
---

## Explanation

So far a program could choose between paths, but it still did each step at most once. Many problems need **repetition**: print the numbers 1 to 10, add up a list of prices, keep asking until the answer is right. Doing the same block of steps over and over is called a **loop**, or iteration, and it is what lets a short algorithm do a large amount of work. You repeat things in real life constantly: stir until the pot boils, wash each plate in the stack. A loop is that idea written precisely.

The first form is the **WHILE** loop: `WHILE condition DO ... END WHILE`. It checks the condition, and if it is true it runs the steps inside (the body), then comes back and checks the condition again, repeating until the condition becomes false. Two facts about this matter enormously. First, the condition is checked *before* each pass, so if it is false at the very start, the body runs zero times. Second, something inside the body must eventually make the condition false, or the loop runs forever. Forgetting to update the counter is the classic cause of an endless loop.

The second form is the **FOR** loop: `FOR i FROM 1 TO n DO ... END FOR`. Use it when you know how many times to repeat. It quietly does the counting for you: it starts `i` at 1, runs the body, adds one to `i`, and stops after the pass where `i` equals `n`. So `FOR i FROM 1 TO 5` runs the body exactly five times, with `i` taking the values 1, 2, 3, 4, 5. (There is also `REPEAT ... UNTIL condition`, which checks at the *end*, so its body always runs at least once; we will mostly use WHILE and FOR.)

Two patterns appear again and again. **Counting** uses a variable that goes up by one each pass. **Accumulating** keeps a running total that the body adds to each pass, starting from 0 for a sum or 1 for a product. Summing 1 to n and computing a factorial are both just accumulation inside a loop.

In a flowchart, a loop is drawn with a decision diamond whose true branch runs the body and then **flows back up** to re-check the condition. That backward arrow is the visual signature of a loop. Here is the WHILE loop that sums 1 to n:

```flowchart
{
  "nodes": [
    {"id": "s", "shape": "terminal", "text": "Start"},
    {"id": "i1", "shape": "io", "text": "INPUT n"},
    {"id": "p1", "shape": "process", "text": "sum <- 0"},
    {"id": "p2", "shape": "process", "text": "i <- 1"},
    {"id": "d", "shape": "decision", "text": "i <= n ?"},
    {"id": "b1", "shape": "process", "text": "sum <- sum + i"},
    {"id": "b2", "shape": "process", "text": "i <- i + 1"},
    {"id": "o", "shape": "io", "text": "OUTPUT sum"},
    {"id": "e", "shape": "terminal", "text": "End"}
  ],
  "edges": [
    {"from": "s", "to": "i1"},
    {"from": "i1", "to": "p1"},
    {"from": "p1", "to": "p2"},
    {"from": "p2", "to": "d"},
    {"from": "d", "to": "b1", "label": "Yes"},
    {"from": "b1", "to": "b2"},
    {"from": "b2", "to": "d", "label": "loop back"},
    {"from": "d", "to": "o", "label": "No"},
    {"from": "o", "to": "e"}
  ]
}
```

The most common loop bug by far is the **off-by-one**: running the body one time too many or one too few, usually from the wrong comparison (`<` where you meant `<=`) or starting the counter at the wrong value. The cure is tracing, which now needs one row per pass through the loop. Walk slowly and write down the counter and the running total after every pass.

## Worked example

Problem: read a number n and output the sum 1 + 2 + ... + n.

```pseudocode
INPUT n
sum <- 0
i <- 1
WHILE i <= n DO
    sum <- sum + i
    i <- i + 1
END WHILE
OUTPUT sum
```

Trace it for `n = 3`, one row per check of the condition:

| Pass | i | i <= 3 ? | sum after body | i after body |
|---|---|---|---|---|
| start | 1 | — | 0 | 1 |
| 1 | 1 | true | 0 + 1 = 1 | 2 |
| 2 | 2 | true | 1 + 2 = 3 | 3 |
| 3 | 3 | true | 3 + 3 = 6 | 4 |
| 4 | 4 | false | (loop ends) | 4 |

On the fourth check, `4 <= 3` is false, so the loop ends and the program outputs 6. Notice the body ran three times, once for each of i = 1, 2, 3, and the final check is what stops it. The same algorithm as a FOR loop is shorter, because FOR handles the counter for you:

```pseudocode
INPUT n
sum <- 0
FOR i FROM 1 TO n DO
    sum <- sum + i
END FOR
OUTPUT sum
```

## Key ideas

- A loop repeats a block of steps; WHILE repeats while a condition stays true, and FOR repeats a known number of times using a counter.
- A WHILE checks its condition before each pass, so a condition that is false at the start runs the body zero times; if nothing in the body makes the condition false, the loop runs forever.
- Counting (a variable that rises each pass) and accumulating (a running total starting at 0 for a sum or 1 for a product) are the two core loop patterns.
- In a flowchart, a loop is a decision whose body flows back up to re-check the condition; that backward arrow is what makes it a loop.
- Off-by-one errors, running one pass too many or too few, are the most common loop bug, so trace one row per pass and watch which values the counter takes.

## Exercises

```yaml
- type: mcq
  difficulty: easy
  prompt: "What does a loop let a program do?"
  options: ["Repeat a block of steps", "Choose between two paths", "Store a value in a variable", "Compare two numbers"]
  correct_answer: "Repeat a block of steps"
  target_misconception: none
  explanation: "Looping is repetition; choosing between paths is selection, which is a different idea."
- type: mcq
  difficulty: easy
  prompt: "A WHILE loop keeps repeating its body as long as its condition is what?"
  options: ["True", "False", "Zero", "Equal to the counter"]
  correct_answer: "True"
  target_misconception: loop_execution_model
  explanation: "WHILE repeats while the condition is true and stops once it becomes false."
- type: mcq
  difficulty: easy
  prompt: "How many times does the body run in: FOR i FROM 1 TO 5 DO ... END FOR ?"
  options: ["5 times", "4 times", "6 times", "Once"]
  correct_answer: "5 times"
  target_misconception: loop_boundary_offbyone
  explanation: "i takes the values 1, 2, 3, 4, 5, so the body runs five times."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nsum <- 0\ni <- 1\nWHILE i <= 3 DO\n    sum <- sum + i\n    i <- i + 1\nEND WHILE\nOUTPUT sum"
  correct_answer: "6"
  target_misconception: loop_execution_model
  explanation: "The body runs for i = 1, 2, 3, adding 1 + 2 + 3 = 6 before the condition becomes false."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\ncount <- 0\nFOR i FROM 1 TO 5 DO\n    count <- count + 1\nEND FOR\nOUTPUT count"
  correct_answer: "5"
  target_misconception: loop_boundary_offbyone
  explanation: "The body runs once for each of i = 1..5, so count rises to 5."
- type: predict_output
  difficulty: medium
  prompt: "The user enters n = 3. Trace the flowchart shown and state what it outputs."
  prompt_diagram:
    nodes:
      - {id: s, shape: terminal, text: "Start"}
      - {id: i1, shape: io, text: "INPUT n"}
      - {id: p1, shape: process, text: "sum <- 0"}
      - {id: p2, shape: process, text: "i <- 1"}
      - {id: d, shape: decision, text: "i <= n ?"}
      - {id: b1, shape: process, text: "sum <- sum + i"}
      - {id: b2, shape: process, text: "i <- i + 1"}
      - {id: o, shape: io, text: "OUTPUT sum"}
      - {id: e, shape: terminal, text: "End"}
    edges:
      - {from: s, to: i1}
      - {from: i1, to: p1}
      - {from: p1, to: p2}
      - {from: p2, to: d}
      - {from: d, to: b1, label: "Yes"}
      - {from: b1, to: b2}
      - {from: b2, to: d, label: "loop back"}
      - {from: d, to: o, label: "No"}
      - {from: o, to: e}
  correct_answer: "6"
  target_misconception: loop_execution_model
  explanation: "The body runs for i = 1, 2, 3, accumulating 6; the backward arrow re-checks the condition each pass."
- type: mcq
  difficulty: medium
  prompt: "If a WHILE loop's condition is already false before the first pass, how many times does the body run?"
  options: ["Zero times", "Once", "Forever", "It is not allowed"]
  correct_answer: "Zero times"
  target_misconception: loop_execution_model
  explanation: "WHILE checks the condition first, so a false start means the body is skipped entirely."
- type: mcq
  difficulty: medium
  prompt: "What is the usual cause of a loop that never stops (an infinite loop)?"
  options: ["The body never changes anything that would make the condition false", "The loop has too many steps", "The counter starts at 1 instead of 0", "The output comes after the loop"]
  correct_answer: "The body never changes anything that would make the condition false"
  target_misconception: loop_execution_model
  explanation: "If nothing updates toward the stopping condition (such as forgetting i <- i + 1), the condition stays true forever."
- type: pseudocode_order
  difficulty: medium
  prompt: "Arrange these lines into a correct loop that outputs the numbers 1, 2, 3."
  options: ["END WHILE", "OUTPUT i", "i <- 1", "i <- i + 1", "WHILE i <= 3 DO"]
  correct_answer: ["i <- 1", "WHILE i <= 3 DO", "OUTPUT i", "i <- i + 1", "END WHILE"]
  target_misconception: algorithm_sequencing_error
  explanation: "Set the counter before the loop, then inside the loop output it and increase it, then close with END WHILE."
- type: mcq
  difficulty: medium
  prompt: "In FOR i FROM 1 TO n, which values does the counter i take?"
  options: ["1, 2, 3, ..., up to and including n", "0, 1, 2, ..., up to n", "1, 2, 3, ..., up to n minus 1", "Only the value n"]
  correct_answer: "1, 2, 3, ..., up to and including n"
  target_misconception: loop_boundary_offbyone
  explanation: "FOR ... TO n includes n, so the counter runs from 1 through n."
- type: predict_output
  difficulty: hard
  prompt: "Trace this and state what it outputs.\n\nn <- 4\nfact <- 1\ni <- 1\nWHILE i <= n DO\n    fact <- fact * i\n    i <- i + 1\nEND WHILE\nOUTPUT fact"
  correct_answer: "24"
  target_misconception: loop_execution_model
  explanation: "fact accumulates 1*1, then *2, *3, *4, giving 1, 2, 6, 24; the product starts at 1, not 0."
- type: mcq
  difficulty: hard
  prompt: "To print the numbers 1 to 10, a learner writes: i <- 1; WHILE i < 10 DO OUTPUT i; i <- i + 1 END WHILE. What goes wrong?"
  options: ["It stops after printing 9, because i < 10 is false when i reaches 10", "It prints 1 to 11, one too many", "It prints nothing at all", "It runs forever"]
  correct_answer: "It stops after printing 9, because i < 10 is false when i reaches 10"
  target_misconception: loop_boundary_offbyone
  explanation: "To include 10 the condition must be i <= 10; using < drops the final value, a classic off-by-one."
```
