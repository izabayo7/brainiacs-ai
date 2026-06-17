---
slug: variables-assignment
name: Variables & Assignment
order: 2
prerequisites: [algorithmic-thinking]
summary: How a program remembers and changes information using named boxes, and why the assignment arrow is an instruction to store a value rather than a statement that two things are equal.
estimated_minutes: 30
---

## Explanation

When you followed the tea or bread algorithm in the last lesson, you had to keep track of things as you went: the water is now boiling, the mixture is now in the pan. A computer program has the same need. As it works through its steps it has to *remember* information, like the number someone typed in or a running total it is building up. The tool a program uses to remember is called a **variable**.

The easiest way to picture a variable is a labelled jar on a kitchen shelf. You write a label on the jar, that is its **name**, and you can put one thing inside, that is its **value**. The label stays the same, but you can empty the jar and put something new in whenever you like. So a variable is simply a named box that holds one value at a time. We choose the name, and we choose what value goes in. In this course a value is usually a number or a piece of text, and the next lesson looks more closely at the different kinds of values.

Putting a value into the box is called **assignment**, and we write it with a left arrow. The line `count <- 0` means "store the value 0 in the box named count." It is very important to understand what the computer does here, because this is where most beginners get confused. The computer first looks at the right-hand side and works out its value. Then it takes that result and drops it into the box named on the left. The arrow is an *instruction to store*, it is not the word "equals". Reading `<-` as "equals" will tie you in knots later, so read it as "becomes" or "gets": "count becomes 0."

Because the arrow is an instruction and not an equation, a line that would look impossible in mathematics makes perfect sense in a program. Take `count <- count + 1`. If `<-` meant "equals", this would be nonsense, since nothing equals itself plus one. But as an instruction it is clear: work out `count + 1` using the value currently in the box, then store that answer back in the same box. If `count` held 4, the right side works out to 5, and 5 is stored back, so `count` now holds 5. This is how programs count and add things up, and you will use it constantly.

Two more facts follow from "a box holds one value at a time." First, when you store a new value, the old one is gone for good. If you wanted to keep the old value, you needed to save it in another box first. This is exactly why swapping the contents of two boxes needs a third, temporary box to hold a value while you move things around. Second, assignment **copies** a value, it does not tie two boxes together. After `a <- b`, the box `a` holds its own copy of whatever `b` had; changing `b` later does not reach back and change `a`. And the direction matters: `a <- b` is not the same as `b <- a`, and you can never write something like `7 <- x`, because a plain value is not a box you can store into.

One small habit that pays off forever: choose **descriptive names**. A box called `total` or `studentCount` tells you and the next reader what it holds. A box called `x` or `t` tells you nothing. The name is only a label, a handle for finding the value, so make the label say what the box is for.

## Worked example

**Example A: building up a total.** A shop adds the price of two items into one running total.

```pseudocode
// start the total empty
total <- 0

// add the first price (read old value, store new value)
total <- total + 200

// add the second price the same way
total <- total + 50

OUTPUT total
```

Trace it. `total` starts at 0. The next line works out `0 + 200`, which is 200, and stores it back, so `total` is now 200. The next line works out `200 + 50`, which is 250, and stores it, so `total` is now 250. The output is 250. Each step quietly read the old value before storing the new one.

**Example B: swapping two boxes.** We want `a` and `b` to trade values. Because a box holds only one value, we need a temporary box, `temp`, so nothing is lost.

```pseudocode
a <- 5
b <- 9

temp <- a    // save a's value (5) before it gets overwritten
a <- b       // a now holds 9
b <- temp    // b now holds the saved 5

OUTPUT a     // shows 9
OUTPUT b     // shows 5
```

Trace it. `temp` saves the 5. Then `a` is overwritten with `b`'s value, 9. Then `b` takes the 5 we parked in `temp`. They have traded. If we had skipped `temp` and written `a <- b` first, the 5 would have been wiped out before we could move it, and both boxes would end up holding 9.

## Key ideas

- A variable is a named box that holds one value at a time; assignment, `name <- value`, stores a value in the box.
- The arrow is an instruction, not equality: the computer works out the right side first, then stores the result in the box named on the left, so read `<-` as "becomes".
- Because the arrow is an instruction, `count <- count + 1` makes sense: it reads the current value, adds one, and stores the answer back.
- A box holds only one value, so storing a new value erases the old one; swapping two variables needs a third box to hold a value temporarily.
- A name is a label you choose as a handle for the value, not the value itself, so pick descriptive names like `total` or `studentCount`.

## Exercises

```yaml
- type: mcq
  difficulty: easy
  prompt: "What does the line score <- 10 do?"
  options: ["Stores the value 10 in the box named score", "Checks whether score is the same as 10", "Creates a value named score", "Compares 10 with the name score"]
  correct_answer: "Stores the value 10 in the box named score"
  target_misconception: assignment_as_equality
  explanation: "The arrow is an instruction to store a value, read as 'becomes', not a test for equality."
- type: mcq
  difficulty: easy
  prompt: "Which best describes a variable?"
  options: ["A named box that holds one value at a time", "A fixed number that can never change", "A list of instructions", "The name of the whole program"]
  correct_answer: "A named box that holds one value at a time"
  target_misconception: variable_name_semantics
  explanation: "A variable is a named container; the name is its label and the value is what is currently inside."
- type: predict_output
  difficulty: easy
  prompt: "Trace this and state what it outputs.\n\nx <- 5\nx <- 8\nOUTPUT x"
  correct_answer: "8"
  target_misconception: assignment_as_equality
  explanation: "A box holds one value at a time, so storing 8 replaces the 5."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\ncount <- 0\ncount <- count + 1\ncount <- count + 1\ncount <- count + 1\nOUTPUT count"
  correct_answer: "3"
  target_misconception: assignment_as_equality
  explanation: "Each line reads the current value and stores one more, so count goes 0, 1, 2, 3."
- type: mcq
  difficulty: medium
  prompt: "What does the line count <- count + 1 mean?"
  options: ["Work out count + 1 using the current value, then store the result back in count", "It is impossible, because count cannot be equal to itself plus one", "Create a new box called count plus one", "Compare count with count + 1"]
  correct_answer: "Work out count + 1 using the current value, then store the result back in count"
  target_misconception: assignment_as_equality
  explanation: "The right side is computed first using the old value, then the answer is stored back; the arrow is not an equals sign."
- type: mcq
  difficulty: medium
  prompt: "Are the lines a <- b and b <- a the same instruction?"
  options: ["No: each copies the value on the right into the box on the left, so they do opposite things", "Yes: both make a and b hold the same value", "Yes: the order of the names does not matter", "No, but only because of alphabetical order"]
  correct_answer: "No: each copies the value on the right into the box on the left, so they do opposite things"
  target_misconception: assignment_as_equality
  explanation: "Assignment has a direction; the arrow points to where the value goes."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nb <- 5\na <- b\nb <- 9\nOUTPUT a"
  correct_answer: "5"
  target_misconception: variable_name_semantics
  explanation: "a <- b copied 5 into a's own box; changing b to 9 afterwards does not reach back and change a."
- type: pseudocode_order
  difficulty: medium
  prompt: "Arrange these lines to swap the values of a and b correctly, so a ends with b's old value and b ends with a's old value."
  options: ["a <- b", "b <- temp", "temp <- a"]
  correct_answer: ["temp <- a", "a <- b", "b <- temp"]
  target_misconception: algorithm_sequencing_error
  explanation: "Save a in temp first; otherwise a <- b erases a's value before it can be moved to b."
- type: mcq
  difficulty: medium
  prompt: "Which is the clearest name for a box that holds the number of students?"
  options: ["studentCount", "s", "x2", "thing"]
  correct_answer: "studentCount"
  target_misconception: variable_name_semantics
  explanation: "A name is a label; a descriptive label tells the reader what the box is for."
- type: predict_output
  difficulty: hard
  prompt: "Trace this and state what it outputs.\n\ntotal <- 0\nprice <- 200\ntotal <- total + price\nprice <- 50\ntotal <- total + price\nOUTPUT total"
  correct_answer: "250"
  target_misconception: assignment_as_equality
  explanation: "total becomes 0 + 200 = 200, then 200 + 50 = 250; each update uses the value price holds at that moment."
- type: mcq
  difficulty: hard
  prompt: "Why is the line 7 <- x not a valid instruction?"
  options: ["A plain value like 7 is not a box, so nothing can be stored into it", "Because 7 is usually smaller than x", "Because the arrow must always point to the right", "It is valid and stores x into 7"]
  correct_answer: "A plain value like 7 is not a box, so nothing can be stored into it"
  target_misconception: assignment_as_equality
  explanation: "Assignment stores the right-hand value into a named box on the left; a bare value cannot be assigned to."
- type: predict_output
  difficulty: hard
  prompt: "Trace this and state what it outputs.\n\na <- 5\nb <- 9\ntemp <- a\na <- b\nb <- temp\nOUTPUT b"
  correct_answer: "5"
  target_misconception: none
  explanation: "temp saved a's 5, then b received that saved value, so b ends holding 5."
```
