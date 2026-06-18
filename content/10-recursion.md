---
slug: recursion
name: Recursion
order: 10
prerequisites: [functions-scope]
summary: How a function can solve a problem by calling itself on a smaller version of the same problem, and why every recursion needs a base case that stops it.
estimated_minutes: 35
---

## Explanation

A function is allowed to call itself. That sounds strange at first, but it is just a way of solving a problem by solving a smaller version of the *same* problem, over and over, until the version is small enough to answer outright. This is called **recursion**. Think of a set of Russian nesting dolls: to open them all, you open one doll and find a smaller doll inside, and you do the very same thing to that one, and so on, until you reach the tiniest solid doll that does not open. The task "open all the dolls" is defined in terms of a smaller copy of itself, with a clear stopping point.

Every recursion has exactly two parts, and both are essential. The **base case** is the smallest version of the problem, the one whose answer you know directly without any more calls. It is what stops the recursion. The **recursive case** is where the function calls itself on a smaller input and builds its answer from what comes back. For factorial, the base case is `factorial(0) = 1`, and the recursive case is `factorial(n) = n * factorial(n - 1)`. Each call hands the problem to a slightly smaller call, until the base case is reached.

The single most common recursion mistake is **forgetting the base case**, or writing one that is never actually reached. With no base case to stop it, a function calls itself forever, exactly like a loop with no way to become false. The cure is to always ask two questions: what is the smallest case I can answer directly, and does each recursive call move *closer* to that case?

The other thing that confuses beginners is what actually happens during the calls. Recursion is not a loop. Each call is a fresh copy of the function with its own value of the parameter, and it **pauses**, waiting, until the call it made comes back with an answer. The calls stack up going in (winding down to the base case), and then the answers come back out in reverse order (unwinding). Picture it for `factorial(3)`:

```text
factorial(3)
  = 3 * factorial(2)
      = 2 * factorial(1)
          = 1 * factorial(0)
              = 1                (base case, stops here)
          = 1 * 1 = 1
      = 2 * 1 = 2
  = 3 * 2 = 6
```

Reading top to bottom, each call waits while a smaller one runs; reading the answers back up, each waiting call finishes its multiplication once the inner result arrives.

## Worked example

Problem: compute the factorial of n (for example 3! = 3 * 2 * 1 = 6).

```pseudocode
FUNCTION factorial(n)
    IF n = 0 THEN
        RETURN 1
    ELSE
        RETURN n * factorial(n - 1)
    END IF
END FUNCTION

OUTPUT factorial(3)
```

The body as a flowchart: a single decision picks the base case or the recursive case.

```flowchart
{
  "nodes": [
    {"id": "s", "shape": "terminal", "text": "Start factorial(n)"},
    {"id": "d", "shape": "decision", "text": "n = 0 ?"},
    {"id": "r1", "shape": "io", "text": "RETURN 1"},
    {"id": "r2", "shape": "io", "text": "RETURN n * factorial(n - 1)"},
    {"id": "e", "shape": "terminal", "text": "End"}
  ],
  "edges": [
    {"from": "s", "to": "d"},
    {"from": "d", "to": "r1", "label": "Yes"},
    {"from": "d", "to": "r2", "label": "No"},
    {"from": "r1", "to": "e"},
    {"from": "r2", "to": "e"}
  ]
}
```

Trace `factorial(3)` using the indented picture above. The calls wind down 3, then 2, then 1, then 0, where the base case returns 1 without calling further. Then they unwind: `factorial(1)` returns `1 * 1 = 1`, `factorial(2)` returns `2 * 1 = 2`, and `factorial(3)` returns `3 * 2 = 6`. The output is 6. Notice each call sat paused, holding its own value of `n`, until the smaller call answered.

## Key ideas

- Recursion is a function that calls itself, solving a problem by reducing it to a smaller version of the same problem.
- Every recursion needs a base case (a smallest case answered directly, which stops it) and a recursive case (which calls itself on a smaller input).
- Without a base case that is actually reached, the function calls itself forever, just like an endless loop.
- Each call is a fresh copy with its own value that pauses until its inner call returns; the answers come back in reverse order as the calls unwind.

## Exercises

```yaml
- type: mcq
  difficulty: easy
  prompt: "What is recursion?"
  options: ["A function that calls itself on a smaller version of the same problem", "A loop that counts down", "A function with many parameters", "A variable that holds many values"]
  correct_answer: "A function that calls itself on a smaller version of the same problem"
  target_misconception: none
  explanation: "Recursion solves a problem in terms of a smaller copy of itself."
- type: mcq
  difficulty: easy
  prompt: "Which two parts does every recursive function need?"
  options: ["A base case and a recursive case", "A loop and a counter", "An array and an index", "Two parameters"]
  correct_answer: "A base case and a recursive case"
  target_misconception: none
  explanation: "The base case stops it; the recursive case calls itself on a smaller input."
- type: mcq
  difficulty: easy
  prompt: "What is the job of the base case?"
  options: ["To give a direct answer for the smallest case and stop the recursion", "To call the function one more time", "To make the input larger", "To print the result"]
  correct_answer: "To give a direct answer for the smallest case and stop the recursion"
  target_misconception: recursion_no_base_case
  explanation: "The base case is reached when no further calls are needed, which is what ends the recursion."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nFUNCTION factorial(n)\n    IF n = 0 THEN\n        RETURN 1\n    ELSE\n        RETURN n * factorial(n - 1)\n    END IF\nEND FUNCTION\n\nOUTPUT factorial(3)"
  correct_answer: "6"
  target_misconception: recursion_state_confusion
  explanation: "The calls unwind as 1, then 1*1, then 2*1, then 3*2, giving 6."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nFUNCTION factorial(n)\n    IF n = 0 THEN\n        RETURN 1\n    ELSE\n        RETURN n * factorial(n - 1)\n    END IF\nEND FUNCTION\n\nOUTPUT factorial(0)"
  correct_answer: "1"
  target_misconception: recursion_no_base_case
  explanation: "factorial(0) hits the base case directly and returns 1 with no further calls."
- type: mcq
  difficulty: medium
  prompt: "What happens if a recursive function never reaches a base case?"
  options: ["It calls itself forever and never stops", "It returns 0", "It runs exactly once", "It turns into a loop automatically"]
  correct_answer: "It calls itself forever and never stops"
  target_misconception: recursion_no_base_case
  explanation: "With nothing to stop it, recursion runs endlessly, like an infinite loop."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nFUNCTION sumTo(n)\n    IF n = 0 THEN\n        RETURN 0\n    ELSE\n        RETURN n + sumTo(n - 1)\n    END IF\nEND FUNCTION\n\nOUTPUT sumTo(3)"
  correct_answer: "6"
  target_misconception: recursion_state_confusion
  explanation: "The calls add 3 + 2 + 1 + 0 as they unwind, giving 6."
- type: mcq
  difficulty: medium
  prompt: "While computing factorial(3), what must happen before factorial(3) can finish its multiplication?"
  options: ["factorial(2) must return its value first; factorial(3) is paused until then", "factorial(3) finishes first, then calls factorial(2)", "All calls run at the same time", "factorial(3) ignores factorial(2)"]
  correct_answer: "factorial(2) must return its value first; factorial(3) is paused until then"
  target_misconception: recursion_state_confusion
  explanation: "Each call waits for the inner call to return before completing its own work."
- type: pseudocode_order
  difficulty: medium
  prompt: "Arrange these lines into a correct recursive factorial function."
  options: ["RETURN 1", "ELSE", "FUNCTION factorial(n)", "RETURN n * factorial(n - 1)", "IF n = 0 THEN", "END IF", "END FUNCTION"]
  correct_answer: ["FUNCTION factorial(n)", "IF n = 0 THEN", "RETURN 1", "ELSE", "RETURN n * factorial(n - 1)", "END IF", "END FUNCTION"]
  target_misconception: algorithm_sequencing_error
  explanation: "The base case comes first inside the IF, the recursive case in the ELSE, then the blocks are closed."
- type: mcq
  difficulty: medium
  prompt: "In the factorial function, which line is the base case?"
  options: ["IF n = 0 THEN RETURN 1", "RETURN n * factorial(n - 1)", "FUNCTION factorial(n)", "OUTPUT factorial(3)"]
  correct_answer: "IF n = 0 THEN RETURN 1"
  target_misconception: recursion_no_base_case
  explanation: "n = 0 returning 1 is the case answered directly, with no further call."
- type: predict_output
  difficulty: hard
  prompt: "Trace this and state what it outputs.\n\nFUNCTION fib(n)\n    IF n = 0 THEN\n        RETURN 0\n    ELSE IF n = 1 THEN\n        RETURN 1\n    ELSE\n        RETURN fib(n - 1) + fib(n - 2)\n    END IF\nEND FUNCTION\n\nOUTPUT fib(4)"
  correct_answer: "3"
  target_misconception: recursion_state_confusion
  explanation: "fib values are 0, 1, 1, 2, 3 for n = 0..4, so fib(4) is 3."
- type: mcq
  difficulty: hard
  prompt: "What guarantees that a recursion eventually stops?"
  options: ["Each recursive call uses a smaller input that moves toward the base case", "The function has a return statement", "The function takes only one parameter", "The base case comes last in the code"]
  correct_answer: "Each recursive call uses a smaller input that moves toward the base case"
  target_misconception: recursion_no_base_case
  explanation: "Progress toward a reachable base case is what makes recursion terminate."
```
