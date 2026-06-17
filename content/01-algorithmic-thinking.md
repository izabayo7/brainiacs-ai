---
slug: algorithmic-thinking
name: Computers, Algorithms & Problem Solving
order: 1
prerequisites: []
summary: What a computer actually does, how every task fits the input-process-output pattern, and how to break a problem into a clear, ordered list of steps called an algorithm.
estimated_minutes: 30
---

## Explanation

Before we touch anything that looks like programming, look at the machines around you. A juice blender takes in fruit, does something to it, and gives you juice. An ATM takes your card and a request, does its work, and gives you cash. A kettle takes cold water and hands back hot water. Each one is a **system**: something goes in, work happens, something comes out. We can describe almost any system in three words: **input, process, output**. Hold on to those three words, because every program you ever meet is built on them.

A computer is a system too, with one special talent and one important weakness. Its talent is that it follows instructions exactly, very fast, without ever getting bored. Its weakness is that it has no common sense at all: it does *exactly* what it is told and nothing more, and it will never guess what you meant. If you leave out a step, it does not fill in the gap the way a friend would. That sounds like a problem, but it is actually the whole reason this course exists. Our job is to learn how to write instructions so clear and so complete that something with no imagination can follow them perfectly.

A clear, ordered list of instructions for solving a problem is called an **algorithm**. You already make algorithms every day without using the word. A recipe for making tea is an algorithm. Directions to your house are an algorithm. The steps a baker follows to make bread, preheat the oven, mix the flour and sugar, pour the batter into a pan, bake it, then take it out, form an algorithm. An algorithm is simply a precise, step-by-step method that takes you from a starting point to a finished result. It is plain thinking written down, and it does not belong to any computer or language.

What separates a *good* algorithm from a vague plan comes down to three habits. First, every step must be clear and mean exactly one thing. "Bake for thirty minutes" is clear; "bake until it looks about right" is not, because two people would do something different. Second, the steps must be in the correct order, because the order carries the meaning: you cannot pour the batter before you have mixed it. Third, the algorithm must finish. It has to reach an end after a limited number of steps, not run on forever.

The reason all of this matters is a skill called **decomposition**: breaking one big, scary problem into small steps that are each obvious. "Make bread" feels hard. "Preheat the oven, then mix, then pour, then bake, then remove it" is five easy steps that anyone can follow. Learning to break problems down this way is the single most useful habit in all of programming, and notice that we have not mentioned a computer or a programming language even once. It is careful thinking, nothing more.

One last word about where we are going. In this course you will write your algorithms as **pseudocode**, a plain and readable way of writing steps, and sometimes as **flowcharts**, a picture of those steps. Neither is tied to a real language like Python or C. A **program** is what you get later when you rewrite your algorithm in one of those real languages for a specific machine. We are practising the thinking first, on purpose, so that when you do pick up a real language one day, the hard part, working out the steps, is already second nature to you.

## Worked example

**Example A: an everyday algorithm.** Suppose the task is "make a cup of tea." We decompose it into clear, ordered steps:

1. Boil the water.
2. Put a tea bag in a cup.
3. Pour the boiled water into the cup.
4. Wait two minutes.
5. Remove the tea bag.

Each step is clear, the order matters (you cannot pour before you boil), and the list ends. That is a complete algorithm, written in plain language, with no computer in sight.

**Example B: a computing algorithm.** Now the same kind of thinking for a problem a computer can do: find the area of a circle. Think input, process, output. Input: the circle's radius. Process: multiply 3.14 by the radius twice. Output: the area.

```pseudocode
// INPUT: read the circle's radius
INPUT radius

// PROCESS: apply the area formula
area <- 3.14 * radius * radius

// OUTPUT: show the answer
OUTPUT area
```

Let us trace it the way the computer would, for a radius of 10. The first line reads 10 into `radius`. The second line works out `3.14 * 10 * 10`, which is 314, and stores it in `area`. The last line shows 314. The computer made no decisions and used no cleverness. It simply followed three steps in order, exactly as written. Every program in this course is built from that same idea.

## Key ideas

- A system takes input, does a process, and produces output. A computer is a system that follows instructions exactly and never guesses what you meant.
- An algorithm is a clear, ordered, finite list of steps that solves a problem, and you already use algorithms, like recipes and directions, every day.
- A good algorithm has steps that are unambiguous, in the correct order, and that always come to an end.
- Decomposition, breaking a big problem into small obvious steps, is the core thinking skill, and it has nothing to do with any programming language.

## Exercises

```yaml
- type: mcq
  difficulty: easy
  prompt: "A juice blender takes in fruit, blends it, and produces juice. In the input-process-output model, what is the juice?"
  options: ["The output", "The input", "The process", "The system"]
  correct_answer: "The output"
  target_misconception: none
  explanation: "The juice is what comes out at the end, so it is the output; the fruit is the input and blending is the process."
- type: mcq
  difficulty: easy
  prompt: "Which of these is an algorithm?"
  options: ["A recipe: an ordered list of steps for making a dish", "A photograph of a finished cake", "The price of a bag of flour", "A single number, such as 42"]
  correct_answer: "A recipe: an ordered list of steps for making a dish"
  target_misconception: none
  explanation: "An algorithm is an ordered list of steps that solves a problem; a photo, a price, and a lone number are not."
- type: mcq
  difficulty: easy
  prompt: "Which instruction is too unclear to belong in a good algorithm?"
  options: ["Stir until it looks about right", "Stir for two minutes", "Add two cups of flour", "Wait ten seconds"]
  correct_answer: "Stir until it looks about right"
  target_misconception: none
  explanation: "Every step must mean exactly one thing; 'looks about right' would be done differently by different people."
- type: pseudocode_order
  difficulty: easy
  prompt: "Arrange these everyday steps into a correct algorithm for making a cup of tea."
  options: ["Pour the boiled water into the cup", "Boil the water", "Remove the tea bag after two minutes", "Put a tea bag in the cup"]
  correct_answer: ["Boil the water", "Put a tea bag in the cup", "Pour the boiled water into the cup", "Remove the tea bag after two minutes"]
  target_misconception: algorithm_sequencing_error
  explanation: "Order carries the meaning: you cannot pour water you have not boiled, or remove a bag you have not added."
- type: pseudocode_order
  difficulty: easy
  prompt: "Arrange these steps into a correct algorithm for baking bread."
  options: ["Take the bread out of the oven", "Preheat the oven", "Pour the mixture into a baking pan", "Mix the flour, sugar and other ingredients", "Bake for thirty minutes"]
  correct_answer: ["Preheat the oven", "Mix the flour, sugar and other ingredients", "Pour the mixture into a baking pan", "Bake for thirty minutes", "Take the bread out of the oven"]
  target_misconception: algorithm_sequencing_error
  explanation: "Each step depends on the ones before it; you cannot pour a mixture you have not made or take out bread you have not baked."
- type: mcq
  difficulty: medium
  prompt: "Why must every algorithm come to an end after a limited number of steps?"
  options: ["Because an algorithm that never finishes can never give a result", "Because computers dislike long lists", "Because steps must always be fewer than ten", "Because the output must come before the input"]
  correct_answer: "Because an algorithm that never finishes can never give a result"
  target_misconception: none
  explanation: "Finiteness means the algorithm terminates; a process that runs forever never produces its answer."
- type: predict_output
  difficulty: medium
  prompt: "Trace this algorithm and state what it outputs.\n\nINPUT radius   (the user types 10)\narea <- 3.14 * radius * radius\nOUTPUT area"
  correct_answer: "314"
  target_misconception: none
  explanation: "area becomes 3.14 * 10 * 10 = 314, which is then shown."
- type: predict_output
  difficulty: medium
  prompt: "Trace this algorithm and state what it outputs.\n\nINPUT a   (the user types 7)\nINPUT b   (the user types 4)\nsum <- a + b\nOUTPUT sum"
  correct_answer: "11"
  target_misconception: none
  explanation: "The two inputs are read, then sum becomes 7 + 4 = 11 before it is shown."
- type: pseudocode_order
  difficulty: medium
  prompt: "Arrange these lines into a correct algorithm that reads a radius and outputs the area of a circle."
  options: ["OUTPUT area", "INPUT radius", "area <- 3.14 * radius * radius"]
  correct_answer: ["INPUT radius", "area <- 3.14 * radius * radius", "OUTPUT area"]
  target_misconception: algorithm_sequencing_error
  explanation: "Input comes first, then the calculation that uses it, then the result is shown; this is the input, process, output order."
- type: mcq
  difficulty: medium
  prompt: "What is the difference between an algorithm and a program?"
  options: ["An algorithm is the plan of steps; a program is that plan written in a real language for a machine", "They are exactly the same thing", "An algorithm runs on a computer; a program is only on paper", "A program has no steps, but an algorithm does"]
  correct_answer: "An algorithm is the plan of steps; a program is that plan written in a real language for a machine"
  target_misconception: none
  explanation: "We design the algorithm first (in pseudocode or a flowchart); a program is the same idea expressed in a specific programming language."
- type: predict_output
  difficulty: hard
  prompt: "Trace this algorithm and state what it outputs.\n\nINPUT price      (the user types 200)\nINPUT quantity   (the user types 3)\nsubtotal <- price * quantity\ntotal <- subtotal + 50\nOUTPUT total"
  correct_answer: "650"
  target_misconception: none
  explanation: "subtotal becomes 200 * 3 = 600, then total becomes 600 + 50 = 650, which is shown."
- type: mcq
  difficulty: hard
  prompt: "You must write an algorithm that reports both the area and the perimeter of a rectangle. Which is a correct way to break the task into ordered steps?"
  options: ["Read the length and width, compute the area, compute the perimeter, then show both results", "Show both results, then read the length and width", "Compute the area before reading the length and width", "Read the length, show the area, then read the width"]
  correct_answer: "Read the length and width, compute the area, compute the perimeter, then show both results"
  target_misconception: algorithm_sequencing_error
  explanation: "You must read all the inputs before any calculation can use them, and compute results before showing them."
```