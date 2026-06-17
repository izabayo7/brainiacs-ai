---
slug: data-and-types
name: Data & Data Types
order: 3
prerequisites: [variables-assignment]
summary: The different kinds of values a program works with, how the kind of a value decides what you can do with it, and why text that looks like a number is not the same as a number.
estimated_minutes: 25
---

## Explanation

In everyday life you treat different things in different ways without thinking about it. You can pour water, but you cannot pour a brick. You can add two amounts of money, but it makes no sense to add a person's name to a number. The things around us come in different kinds, and the kind decides what you can sensibly do. Values inside a program are exactly the same: each value has a **type**, and the type tells the computer two things, what the value means and what you are allowed to do with it.

There are four kinds of value you need now. An **integer** is a whole number, like 0, 7, or -3. A **real** is a number with a decimal part, like 3.14 or 36.6 (you will also hear these called floating-point numbers). A **string** is text, such as a name, a word, or a whole sentence, and we write a string inside quotation marks, like `"Kigali"`. A **boolean** is a truth value, and it can only ever be one of two things: true or false. A boolean is the answer to a yes-or-no question, such as "is the light on?"

The type matters because it decides which operations make sense. With numbers, integer or real, you can do arithmetic: add, subtract, multiply, divide. With strings you cannot do arithmetic, but you can **join** them, sticking one piece of text onto the end of another, which is sometimes called concatenation. Joining `"Ki"` and `"gali"` gives `"Kigali"`. Notice that joining is not adding; it simply puts the text together. A boolean is never added or joined; it is just true or false. Trying to use the wrong operation for a type, like adding the word `"cat"` to the number 3, is meaningless, and a real computer would refuse to do it.

There is one trap that catches almost everyone. The text `"5"`, written in quotation marks, is not the same as the number 5. The first is a string that happens to look like a digit; the second is an integer you can do arithmetic with. They look alike on the page, but the computer treats them as completely different things, and you cannot do sums with the text version. Whenever you read a value or store one in a variable, it is worth pausing to ask what type it is.

This connects straight back to the last lesson. A variable is a box that holds one value, and that value always has a type. When you read someone's name you are storing a string; when you read their age you are storing an integer. Choosing the right type for each piece of data is part of designing a correct algorithm, because it decides which operations you will be able to use later.

## Worked example

Problem: read a person's name and their age, then greet them and say how old they will be next year.

First decide the type of each value. The name is a **string**. The age is an **integer**. The greeting we build is a **string**, made by joining. Next year's age is an **integer**, made by adding.

```pseudocode
INPUT personName     // a string, for example "Aline"
INPUT age            // an integer, for example 17

greeting <- "Hello, " + personName   // joining two strings
ageNextYear <- age + 1               // arithmetic on a number

OUTPUT greeting
OUTPUT ageNextYear
```

Trace it for `personName = "Aline"` and `age = 17`. The greeting line joins the text `"Hello, "` with the text `"Aline"`, giving the string `"Hello, Aline"`. The next line adds the number 1 to the number 17, giving the integer 18. So the program outputs `Hello, Aline` and then `18`. Two different types appeared, and each used the operation that fits it: joining for text, addition for numbers. Swapping those operations would be meaningless.

## Key ideas

- Every value has a type; the four basic kinds are integer (whole numbers), real (numbers with a decimal part), string (text written in quotes), and boolean (only true or false).
- The type decides which operations make sense: arithmetic on numbers, joining on strings, while a boolean is simply true or false.
- The text `"5"` (a string) is not the number 5 (an integer); they look alike but the computer treats them as different things.
- A variable holds a value and that value has a type, so choosing the right type is part of designing a correct algorithm.

## Exercises

```yaml
- type: mcq
  difficulty: easy
  prompt: "What type best fits a person's name, such as \"Mukamana\"?"
  options: ["String", "Integer", "Real", "Boolean"]
  correct_answer: "String"
  target_misconception: none
  explanation: "Text is a string; integers and reals are numbers and a boolean is only true or false."
- type: mcq
  difficulty: easy
  prompt: "What type best fits the answer to the question \"is the light on?\""
  options: ["Boolean", "String", "Integer", "Real"]
  correct_answer: "Boolean"
  target_misconception: none
  explanation: "A yes-or-no, true-or-false fact is a boolean."
- type: mcq
  difficulty: easy
  prompt: "What type best fits a body temperature of 36.6?"
  options: ["Real", "Integer", "String", "Boolean"]
  correct_answer: "Real"
  target_misconception: none
  explanation: "A number with a decimal part is a real; an integer holds only whole numbers."
- type: mcq
  difficulty: easy
  prompt: "What type best fits the number of students in a class, such as 30?"
  options: ["Integer", "Real", "String", "Boolean"]
  correct_answer: "Integer"
  target_misconception: none
  explanation: "A count of whole things is an integer."
- type: mcq
  difficulty: medium
  prompt: "Is the text \"5\" (written in quotes) the same as the number 5?"
  options: ["No: \"5\" is text (a string); 5 is a number (an integer)", "Yes, they are exactly the same", "Yes, both are integers", "No: \"5\" is a real and 5 is an integer"]
  correct_answer: "No: \"5\" is text (a string); 5 is a number (an integer)"
  target_misconception: type_confusion
  explanation: "They look alike but are different types; you cannot do arithmetic with the text version."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nfirstName <- \"Jean\"\nlastName <- \"Bosco\"\nfullName <- firstName + \" \" + lastName\nOUTPUT fullName"
  correct_answer: "Jean Bosco"
  target_misconception: type_confusion
  explanation: "Joining strings sticks them together in order; the + here does not do arithmetic because the values are text."
- type: mcq
  difficulty: medium
  prompt: "Which operation makes sense for two strings?"
  options: ["Joining them end to end, like \"Ki\" and \"gali\" into \"Kigali\"", "Adding them to get a numeric sum", "Multiplying them together", "Dividing one by the other"]
  correct_answer: "Joining them end to end, like \"Ki\" and \"gali\" into \"Kigali\""
  target_misconception: type_confusion
  explanation: "Strings are joined, not added; arithmetic is for numbers."
- type: mcq
  difficulty: medium
  prompt: "How many different values can a boolean hold?"
  options: ["Two: true and false", "One", "Any whole number", "As many as you like"]
  correct_answer: "Two: true and false"
  target_misconception: none
  explanation: "A boolean is a truth value, so it is only ever true or false."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\npriceEach <- 2.5\nquantity <- 4\ntotal <- priceEach * quantity\nOUTPUT total"
  correct_answer: "10"
  target_misconception: none
  explanation: "These are numbers, so multiplication is valid: 2.5 * 4 = 10."
- type: pseudocode_order
  difficulty: medium
  prompt: "Arrange these lines into a correct algorithm that reads a name and an age and outputs a greeting using the name."
  options: ["OUTPUT \"Hello, \" + userName", "INPUT userName", "INPUT userAge"]
  correct_answer: ["INPUT userName", "INPUT userAge", "OUTPUT \"Hello, \" + userName"]
  target_misconception: algorithm_sequencing_error
  explanation: "A value must be read before it can be used; the name is needed before the greeting can be built."
- type: mcq
  difficulty: hard
  prompt: "Which of these operations does NOT make sense, given the types of its values?"
  options: ["Adding the text \"cat\" to the number 3", "Joining the text \"Ki\" and the text \"gali\"", "Adding the number 2 and the number 4", "Storing true in a boolean"]
  correct_answer: "Adding the text \"cat\" to the number 3"
  target_misconception: type_confusion
  explanation: "Text and a number are different types; arithmetic on a word is meaningless and a computer would reject it."
```
