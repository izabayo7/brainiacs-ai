---
slug: functions-scope
name: Functions & Scope
order: 9
prerequisites: [loops]
summary: How to package a block of steps into a named, reusable function with inputs and a returned value, and why the variables inside a function stay private to it.
estimated_minutes: 35
---

## Explanation

As programs grow, two problems appear. You find yourself writing the same block of steps in several places, and your algorithm becomes one long list that is hard to read. A **function** solves both. It is a named, reusable block of steps that does one job. You write it once, give it a name, and then **call** it whenever you need that job done. This is the decomposition habit from the very first lesson made real: break a big program into small named tasks, each a function.

You define a function like this: `FUNCTION name(parameters) ... RETURN value ... END FUNCTION`. The **parameters** are the inputs the function expects, listed in the brackets. Inside the body you do the work, and `RETURN` hands one value back to whoever called the function. To **call** it, you write its name with actual values in the brackets, such as `larger(8, 5)`. The call is then replaced by whatever the function returns, so `result <- larger(8, 5)` stores the returned value in `result`.

Two words are easy to mix up. The **argument** is the actual value you pass in at the call, like the 8 and 5 above. The **parameter** is the name inside the function that receives it, like `a` and `b`. When you call `larger(8, 5)`, the parameter `a` receives the argument 8 and `b` receives 5. The parameter is a fresh copy of the value, which is why changing a parameter inside the function does not change the caller's original variable.

This brings us to **scope**, the most important new idea here. A variable created inside a function is **local**: it exists only while the function runs and disappears the moment the function returns. Code outside the function cannot see it. Equally, the function cannot see the caller's variables by their names; the only data it receives from outside is through its parameters. Each function is like a private workroom: it gets the materials you hand it at the door (the arguments), does its work on its own bench (its local variables), and passes one finished result back out (the return value). Confusing this, expecting a function's local variable to be visible outside, or expecting the function to magically see a variable it was never passed, is the classic scope mistake.

## Worked example

Problem: write a function that returns the larger of two numbers, then use it.

```pseudocode
FUNCTION larger(a, b)
    IF a > b THEN
        RETURN a
    ELSE
        RETURN b
    END IF
END FUNCTION

x <- 8
y <- 5
result <- larger(x, y)
OUTPUT result
```

The function body as a flowchart, starting where the call enters and ending where it returns:

```flowchart
{
  "nodes": [
    {"id": "s", "shape": "terminal", "text": "Start larger(a, b)"},
    {"id": "d", "shape": "decision", "text": "a > b ?"},
    {"id": "r1", "shape": "io", "text": "RETURN a"},
    {"id": "r2", "shape": "io", "text": "RETURN b"},
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

Trace the whole thing. In the main steps, `x` becomes 8 and `y` becomes 5. The call `larger(x, y)` runs the function: the parameter `a` receives 8, `b` receives 5. Inside, `8 > 5` is true, so the function returns 8. That returned value replaces the call, so `result` becomes 8, and the program outputs 8. Note that `a` and `b` existed only inside `larger`; out here in the main steps, only `x`, `y`, and `result` exist. Because functions return a value, you can even feed one into another: `larger(larger(4, 9), 7)` first works out `larger(4, 9) = 9`, then `larger(9, 7) = 9`.

## Key ideas

- A function is a named, reusable block of steps that does one job; you define it once and call it many times.
- A function receives inputs called parameters and usually hands back one value with RETURN; a call is replaced by the value it returns.
- Arguments are the actual values you pass in at the call; parameters are the names inside the function that receive copies of them.
- Variables created inside a function are local: they exist only during the call and are invisible outside, and the function sees the caller's data only through its parameters.

## Exercises

```yaml
- type: mcq
  difficulty: easy
  prompt: "What is a function?"
  options: ["A named, reusable block of steps that does one job", "A single value stored in a box", "A loop that never ends", "A true-or-false condition"]
  correct_answer: "A named, reusable block of steps that does one job"
  target_misconception: none
  explanation: "A function packages a task under a name so it can be called whenever needed."
- type: mcq
  difficulty: easy
  prompt: "What does RETURN do in a function?"
  options: ["Hands one value back to whoever called the function", "Repeats the function from the start", "Stores a value in a global box", "Prints a value to the screen"]
  correct_answer: "Hands one value back to whoever called the function"
  target_misconception: none
  explanation: "RETURN passes a result back to the caller, which is different from printing output."
- type: mcq
  difficulty: easy
  prompt: "What are the parameters of a function?"
  options: ["The inputs the function receives", "The values the function prints", "The names of other functions", "The number of times it runs"]
  correct_answer: "The inputs the function receives"
  target_misconception: none
  explanation: "Parameters are the named inputs listed in the function's brackets."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nFUNCTION parkingFee(hours)\n    RETURN hours * 500\nEND FUNCTION\n\nresult <- parkingFee(3)\nOUTPUT result"
  correct_answer: "1500"
  target_misconception: none
  explanation: "The call passes 3 as the argument; the function returns 3 * 500 = 1500."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nFUNCTION larger(a, b)\n    IF a > b THEN\n        RETURN a\n    ELSE\n        RETURN b\n    END IF\nEND FUNCTION\n\nresult <- larger(8, 5)\nOUTPUT result"
  correct_answer: "8"
  target_misconception: none
  explanation: "a receives 8 and b receives 5; 8 > 5 is true, so the function returns 8."
- type: mcq
  difficulty: medium
  prompt: "A function creates a variable called temp inside its body. Can the code that called the function use temp afterwards?"
  options: ["No: temp is local to the function and disappears when it returns", "Yes: all variables are shared everywhere", "Yes, but only if the function is called twice", "Only if temp holds a number"]
  correct_answer: "No: temp is local to the function and disappears when it returns"
  target_misconception: scope_confusion
  explanation: "Local variables exist only during the call and are invisible outside the function."
- type: mcq
  difficulty: medium
  prompt: "Inside a function, can you refer to a variable from the caller that was not passed in as a parameter?"
  options: ["No: the function only receives the caller's data through its parameters", "Yes: a function can see every variable in the program", "Yes, as long as the names are different", "Only the first variable the caller made"]
  correct_answer: "No: the function only receives the caller's data through its parameters"
  target_misconception: scope_confusion
  explanation: "A function's only window onto the caller's data is its parameters."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nFUNCTION addTen(n)\n    n <- n + 10\n    RETURN n\nEND FUNCTION\n\nx <- 5\nresult <- addTen(x)\nOUTPUT x"
  correct_answer: "5"
  target_misconception: scope_confusion
  explanation: "The parameter n is a copy of x; changing n inside the function does not change x, which is still 5."
- type: pseudocode_order
  difficulty: medium
  prompt: "Arrange these lines into a correct program that defines a function to square a number and then uses it."
  options: ["OUTPUT result", "RETURN x * x", "FUNCTION square(x)", "result <- square(4)", "END FUNCTION"]
  correct_answer: ["FUNCTION square(x)", "RETURN x * x", "END FUNCTION", "result <- square(4)", "OUTPUT result"]
  target_misconception: algorithm_sequencing_error
  explanation: "The function must be defined and closed before it is called, and the result computed before it is shown."
- type: mcq
  difficulty: medium
  prompt: "In the call larger(8, 5), what are 8 and 5 called, and what are a and b inside the function called?"
  options: ["8 and 5 are arguments; a and b are parameters", "8 and 5 are parameters; a and b are arguments", "Both are arguments", "Both are parameters"]
  correct_answer: "8 and 5 are arguments; a and b are parameters"
  target_misconception: none
  explanation: "Arguments are the values passed at the call; parameters are the names that receive them inside."
- type: predict_output
  difficulty: hard
  prompt: "Trace this and state what it outputs.\n\nFUNCTION larger(a, b)\n    IF a > b THEN\n        RETURN a\n    ELSE\n        RETURN b\n    END IF\nEND FUNCTION\n\nresult <- larger(larger(4, 9), 7)\nOUTPUT result"
  correct_answer: "9"
  target_misconception: none
  explanation: "larger(4, 9) returns 9; then larger(9, 7) returns 9, so result is 9."
- type: mcq
  difficulty: hard
  prompt: "Why are functions useful in a large program?"
  options: ["They let you write a task once and reuse it, and break a big program into clear named parts", "They make the program run without any steps", "They remove the need for variables", "They guarantee the program has no mistakes"]
  correct_answer: "They let you write a task once and reuse it, and break a big program into clear named parts"
  target_misconception: none
  explanation: "Functions give reuse and decomposition, which is exactly the problem-breaking habit from the first lesson."
```
