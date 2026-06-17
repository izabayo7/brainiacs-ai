---
slug: flowcharts-tracing
name: Flowcharts & Tracing
order: 4
prerequisites: [data-and-types]
summary: How to draw an algorithm as a flowchart using a few standard shapes, and how to pretend to be the computer and trace the steps by hand to find the result.
estimated_minutes: 30
---

## Explanation

You already know how to write an algorithm as a list of steps. A **flowchart** is the same algorithm drawn as a picture. It shows each step as a box and the order they run in as arrows. Many people follow a process more easily when they can see it, and a flowchart is a clear, standard way to show one. The written form and the drawn form say exactly the same thing; being able to move between them is the skill of this lesson.

A flowchart uses a small set of shapes, and each shape means one thing. Here is the reference you will use:

```flowchart
{
  "nodes": [
    {"id": "t", "shape": "terminal", "text": "Start / End"},
    {"id": "i", "shape": "io", "text": "Input / Output"},
    {"id": "p", "shape": "process", "text": "Process (a calculation)"}
  ],
  "edges": []
}
```

A rounded box, the **oval** (terminal), marks the start or the end. A slanted box, the **parallelogram** (io), marks reading a value in or showing one out. A plain **rectangle** (process) marks a calculation or storing a value in a variable. **Arrows** connect the boxes and show the order of flow, normally top to bottom. A few rules keep flowcharts tidy: every flowchart begins and ends with an oval, each box has one arrow in and one arrow out, and you follow the arrows in order.

For now every flowchart you draw will be a straight line of boxes from start to end, with no branching and no repetition. Later, when you learn to make choices, you will meet a new shape, the diamond, for decisions, and later still you will learn how to make a flowchart repeat. We are keeping things linear until those ideas are taught, so nothing here will catch you out.

The second half of this lesson is the most useful habit in all of programming: **tracing**. To trace an algorithm is to pretend you are the computer and walk through the steps one box at a time, writing down what each variable holds after every step. The computer has no imagination; it simply does each step in order. If you do the same, slowly and honestly, you can work out exactly what an algorithm produces without any machine at all. Later, when something goes wrong, tracing is how you find the step where it broke.

A neat way to trace is a **trace table**: one column for each variable, plus a column for anything that is output, and one row for each step. As you walk the steps, you fill in the new value of whatever changed. The danger is rushing: skipping a box, doing steps out of order, forgetting to update a value, or reading the wrong line as the output. Go one box at a time and the answer falls out.

## Worked example

Problem: read a rectangle's length and width, then report both its area and its perimeter. Drawn as a flowchart, it runs straight down:

```flowchart
{
  "nodes": [
    {"id": "s", "shape": "terminal", "text": "Start"},
    {"id": "i1", "shape": "io", "text": "INPUT length"},
    {"id": "i2", "shape": "io", "text": "INPUT width"},
    {"id": "p1", "shape": "process", "text": "area <- length * width"},
    {"id": "p2", "shape": "process", "text": "perimeter <- 2 * (length + width)"},
    {"id": "o1", "shape": "io", "text": "OUTPUT area"},
    {"id": "o2", "shape": "io", "text": "OUTPUT perimeter"},
    {"id": "e", "shape": "terminal", "text": "End"}
  ],
  "edges": [
    {"from": "s", "to": "i1"},
    {"from": "i1", "to": "i2"},
    {"from": "i2", "to": "p1"},
    {"from": "p1", "to": "p2"},
    {"from": "p2", "to": "o1"},
    {"from": "o1", "to": "o2"},
    {"from": "o2", "to": "e"}
  ]
}
```

The same algorithm written as steps:

```pseudocode
INPUT length
INPUT width
area <- length * width
perimeter <- 2 * (length + width)
OUTPUT area
OUTPUT perimeter
```

Now trace it for `length = 5` and `width = 3`, filling a trace table one step at a time:

| Step                               | length | width | area | perimeter | Output |
| ---------------------------------- | ------ | ----- | ---- | --------- | ------ |
| INPUT length                       | 5      | —     | —    | —         |        |
| INPUT width                        | 5      | 3     | —    | —         |        |
| area <- length \* width            | 5      | 3     | 15   | —         |        |
| perimeter <- 2 \* (length + width) | 5      | 3     | 15   | 16        |        |
| OUTPUT area                        | 5      | 3     | 15   | 16        | 15     |
| OUTPUT perimeter                   | 5      | 3     | 15   | 16        | 16     |

Walking one row at a time, the area becomes `5 * 3 = 15` and the perimeter becomes `2 * (5 + 3) = 16`. The algorithm outputs 15, then 16. We found the result purely by hand, the same way the computer would.

## Key ideas

- A flowchart is a picture of an algorithm: boxes are steps and arrows show the order they run in.
- The shapes for a straight-line algorithm are the oval (start or end), the parallelogram (input or output), the rectangle (a process such as a calculation), and arrows (the flow).
- Tracing means pretending to be the computer and walking the steps one at a time, recording each variable's value in a trace table.
- Tracing lets you find an algorithm's output by hand, and going one box at a time is what prevents mistakes like skipping a step or reading the wrong output.

## Exercises

```yaml
- type: mcq
  difficulty: easy
  prompt: "In a flowchart, which shape marks the start or the end of the algorithm?"
  options:
    [
      "An oval (rounded box)",
      "A parallelogram (slanted box)",
      "A rectangle",
      "An arrow",
    ]
  correct_answer: "An oval (rounded box)"
  target_misconception: none
  explanation: "The oval is the start/end terminal; parallelograms are input/output and rectangles are processes."
- type: mcq
  difficulty: easy
  prompt: "Which flowchart shape is used for reading a value in or showing a value out?"
  options:
    ["A parallelogram (slanted box)", "An oval", "A rectangle", "An arrow"]
  correct_answer: "A parallelogram (slanted box)"
  target_misconception: none
  explanation: "Input and output use the parallelogram."
- type: mcq
  difficulty: easy
  prompt: "Which flowchart shape is used for a process such as a calculation or storing a value?"
  options: ["A rectangle", "A parallelogram", "An oval", "An arrow"]
  correct_answer: "A rectangle"
  target_misconception: none
  explanation: "A plain rectangle marks a process step."
- type: mcq
  difficulty: easy
  prompt: "What do the arrows in a flowchart show?"
  options:
    [
      "The order in which the steps run",
      "The names of the variables",
      "The values being stored",
      "Where the program is saved",
    ]
  correct_answer: "The order in which the steps run"
  target_misconception: none
  explanation: "Arrows connect the boxes and show the flow from one step to the next."
- type: mcq
  difficulty: medium
  prompt: "What does it mean to trace an algorithm?"
  options:
    [
      "Follow the steps by hand, one at a time, recording each value",
      "Guess the result from the last line",
      "Run it on a computer and read the screen",
      "Rewrite it in a real programming language",
    ]
  correct_answer: "Follow the steps by hand, one at a time, recording each value"
  target_misconception: tracing_error
  explanation: "Tracing is walking each step in order and writing down what changes; guessing from one line is exactly how mistakes happen."
- type: predict_output
  difficulty: medium
  prompt: "The user enters length = 4 and width = 6. Trace the flowchart shown and state what it outputs."
  prompt_diagram:
    nodes:
      - { id: s, shape: terminal, text: "Start" }
      - { id: i1, shape: io, text: "INPUT length" }
      - { id: i2, shape: io, text: "INPUT width" }
      - { id: p1, shape: process, text: "area <- length * width" }
      - { id: p2, shape: process, text: "perimeter <- 2 * (length + width)" }
      - { id: o1, shape: io, text: "OUTPUT perimeter" }
      - { id: e, shape: terminal, text: "End" }
    edges:
      - { from: s, to: i1 }
      - { from: i1, to: i2 }
      - { from: i2, to: p1 }
      - { from: p1, to: p2 }
      - { from: p2, to: o1 }
      - { from: o1, to: e }
  correct_answer: "20"
  target_misconception: tracing_error
  explanation: "perimeter becomes 2 * (4 + 6) = 20; the output box shows perimeter, not area, so read carefully which value leaves the flowchart."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nINPUT a   (the user types 3)\nb <- a + 5\nc <- b * 2\nOUTPUT c"
  correct_answer: "16"
  target_misconception: tracing_error
  explanation: "b becomes 3 + 5 = 8, then c becomes 8 * 2 = 16; each step uses the value from the step before."
- type: mcq
  difficulty: medium
  prompt: "A trace table shows price = 200, then a row stores total <- price + 50, then a row stores total <- total + 25. What is the final value of total?"
  options: ["275", "250", "225", "200"]
  correct_answer: "275"
  target_misconception: tracing_error
  explanation: "total becomes 200 + 50 = 250, then 250 + 25 = 275; the second update uses the value from the first."
- type: pseudocode_order
  format: flowchart
  difficulty: medium
  prompt: "Arrange these flowchart boxes into the correct order for an algorithm that reads a radius and outputs the area of a circle."
  options:
    - { shape: io, text: "OUTPUT area" }
    - { shape: process, text: "area <- 3.14 * radius * radius" }
    - { shape: io, text: "INPUT radius" }
  correct_answer:
    - { shape: io, text: "INPUT radius" }
    - { shape: process, text: "area <- 3.14 * radius * radius" }
    - { shape: io, text: "OUTPUT area" }
  target_misconception: algorithm_sequencing_error
  explanation: "Input comes before the calculation that uses it, and the result is computed before it is shown."
- type: mcq
  difficulty: medium
  prompt: "In a straight-line flowchart, where does the arrow leaving a process rectangle go?"
  options:
    [
      "Down to the next box in the flow",
      "Back up to the start",
      "To any box you choose",
      "Nowhere; a process has no exit",
    ]
  correct_answer: "Down to the next box in the flow"
  target_misconception: none
  explanation: "Each box has one arrow in and one arrow out; in a linear flowchart the flow moves straight down to the next step."
- type: predict_output
  difficulty: hard
  prompt: "Trace this and state what it outputs.\n\nx <- 10\nx <- x + 5\nx <- x - 3\nOUTPUT x"
  correct_answer: "12"
  target_misconception: tracing_error
  explanation: "x becomes 10, then 10 + 5 = 15, then 15 - 3 = 12; you must update x at each step rather than using the original value."
- type: mcq
  difficulty: hard
  prompt: "Why is it useful to trace an algorithm by hand instead of just trusting it?"
  options:
    [
      "To check what it really outputs and find the exact step where a mistake happens",
      "Because tracing is faster than thinking",
      "Because a flowchart cannot be wrong",
      "To avoid having to write the algorithm at all",
    ]
  correct_answer: "To check what it really outputs and find the exact step where a mistake happens"
  target_misconception: none
  explanation: "Tracing confirms the true output and pinpoints where logic goes wrong, which is the heart of debugging."
```
