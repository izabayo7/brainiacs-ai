---
slug: arrays
name: Arrays
order: 8
prerequisites: [loops]
summary: How one named container can hold many values in order, how to reach each value by its index, and how to visit every value with a loop.
estimated_minutes: 35
---

## Explanation

Until now, one variable held one value: a single box. But problems often involve many related values at once. Imagine storing the test scores of thirty students. You would not want thirty separate variables called `score1`, `score2`, and so on; that is unmanageable. Instead you use an **array**: a single named container that holds many values, kept in order. Picture a row of numbered lockers under one sign, or an egg carton with numbered slots. One name covers the whole row, and each slot has a position.

That position number is called the **index**, and you use it to reach a particular value. We write the array name followed by the index in square brackets: `scores[0]` means "the value in position 0 of the array `scores`". Indexing starts at **0**, not 1, so the first value is at index 0, the second at index 1, and so on. This takes a little getting used to but it is the convention you will meet in almost every real language. Here is an array of five scores:

| index | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| value | 85 | 90 | 70 | 60 | 95 |

Because indexing starts at 0, an array of five values has indices 0, 1, 2, 3, 4. The **last** index is always one less than the number of values, here `5 - 1 = 4`. Asking for `scores[5]` is a mistake: there is no position 5, and reaching past the end is called going **out of bounds**.

The single most important idea in this lesson is the difference between the **index** and the **value**. The index is the position; the value is what is stored there. In the table above, `scores[2]` is 70, the value at position 2; it is not 2. Confusing the position with the contents is the classic array mistake. Keep asking yourself: am I talking about *where* a value is, or *what* the value is?

Arrays come alive when you combine them with loops. To do something to every value, you loop a counter over the indices, from 0 up to the last index, and use that counter inside the brackets. `FOR i FROM 0 TO 4 DO ... scores[i] ... END FOR` visits each value in turn. This is why arrays come after loops: traversing an array is just a loop whose counter is used as an index. And the off-by-one care you learned for loops matters doubly here, because looping one step too far runs you straight out of bounds.

## Worked example

Problem: add up all the scores in the array and output the total. The flowchart loops a counter `i` over the indices 0 to 4, adding each `scores[i]` to a running total:

```flowchart
{
  "nodes": [
    {"id": "s", "shape": "terminal", "text": "Start"},
    {"id": "p0", "shape": "process", "text": "scores <- [85, 90, 70, 60, 95]"},
    {"id": "p1", "shape": "process", "text": "total <- 0"},
    {"id": "p2", "shape": "process", "text": "i <- 0"},
    {"id": "d", "shape": "decision", "text": "i <= 4 ?"},
    {"id": "b1", "shape": "process", "text": "total <- total + scores[i]"},
    {"id": "b2", "shape": "process", "text": "i <- i + 1"},
    {"id": "o", "shape": "io", "text": "OUTPUT total"},
    {"id": "e", "shape": "terminal", "text": "End"}
  ],
  "edges": [
    {"from": "s", "to": "p0"},
    {"from": "p0", "to": "p1"},
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

The same algorithm in pseudocode:

```pseudocode
scores <- [85, 90, 70, 60, 95]
total <- 0
FOR i FROM 0 TO 4 DO
    total <- total + scores[i]
END FOR
OUTPUT total
```

Trace it, one row per pass, watching the index `i` and the value it reaches:

| i | scores[i] | total after body |
|---|---|---|
| 0 | 85 | 85 |
| 1 | 90 | 175 |
| 2 | 70 | 245 |
| 3 | 60 | 305 |
| 4 | 95 | 400 |

After `i` reaches 4 the body has run for every index 0 to 4, the total is 400, and the loop stops. Notice we used `i` as the position to pull out each value `scores[i]`, never confusing the position with the contents.

## Key ideas

- An array is one named container holding many values in order; each value is reached by its index (position).
- Indexing starts at 0, so an array of n values has indices 0 to n-1, and the last index is n-1.
- The index is the position, not the value: `scores[2]` means "the value stored at position 2", which is usually not 2.
- You visit every value by looping a counter over the indices 0 to n-1; looping past n-1 goes out of bounds.

## Exercises

```yaml
- type: mcq
  difficulty: easy
  prompt: "What is an array?"
  options: ["One named container that holds many values in order", "A single value that can change", "A loop that repeats forever", "A true-or-false condition"]
  correct_answer: "One named container that holds many values in order"
  target_misconception: none
  explanation: "An array groups many ordered values under one name, each reached by its index."
- type: mcq
  difficulty: easy
  prompt: "An array holds 5 values. What are its valid indices?"
  options: ["0, 1, 2, 3, 4", "1, 2, 3, 4, 5", "0, 1, 2, 3, 4, 5", "1, 2, 3, 4"]
  correct_answer: "0, 1, 2, 3, 4"
  target_misconception: loop_boundary_offbyone
  explanation: "Indexing starts at 0, so five values occupy indices 0 to 4; the last index is 5 - 1 = 4."
- type: mcq
  difficulty: easy
  prompt: "At which index is the first value of an array stored?"
  options: ["0", "1", "-1", "It depends on the array"]
  correct_answer: "0"
  target_misconception: array_index_value_confusion
  explanation: "The first value sits at index 0."
- type: predict_output
  difficulty: medium
  prompt: "The array scores holds [85, 90, 70, 60, 95]. State what this outputs.\n\nOUTPUT scores[2]"
  correct_answer: "70"
  target_misconception: array_index_value_confusion
  explanation: "scores[2] is the value at position 2, which is 70, not the number 2."
- type: predict_output
  difficulty: medium
  prompt: "The array scores holds [85, 90, 70, 60, 95]. State what this outputs.\n\nOUTPUT scores[0]"
  correct_answer: "85"
  target_misconception: array_index_value_confusion
  explanation: "Index 0 is the first value, 85."
- type: mcq
  difficulty: medium
  prompt: "Given scores = [85, 90, 70, 60, 95], what does scores[3] mean?"
  options: ["The value stored at position 3, which is 60", "The number 3", "The third value, 70", "The position of the value 3"]
  correct_answer: "The value stored at position 3, which is 60"
  target_misconception: array_index_value_confusion
  explanation: "The brackets give the value at that position; counting from 0, position 3 holds 60."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\nscores <- [85, 90, 70, 60, 95]\ntotal <- 0\nFOR i FROM 0 TO 4 DO\n    total <- total + scores[i]\nEND FOR\nOUTPUT total"
  correct_answer: "400"
  target_misconception: array_index_value_confusion
  explanation: "The loop adds scores[0] through scores[4]: 85 + 90 + 70 + 60 + 95 = 400."
- type: mcq
  difficulty: medium
  prompt: "An array has 5 values. Why is scores[5] a mistake?"
  options: ["There is no position 5; the last valid index is 4, so it is out of bounds", "It returns the first value again", "It always returns 0", "It is fine and returns the fifth value"]
  correct_answer: "There is no position 5; the last valid index is 4, so it is out of bounds"
  target_misconception: loop_boundary_offbyone
  explanation: "Indices run 0 to 4 for five values; index 5 is past the end."
- type: pseudocode_order
  difficulty: medium
  prompt: "Arrange these lines into a correct algorithm that adds up the values in the array scores (indices 0 to 4) and outputs the total."
  options: ["END WHILE", "total <- 0", "i <- 0", "total <- total + scores[i]", "WHILE i <= 4 DO", "i <- i + 1", "OUTPUT total"]
  correct_answer: ["total <- 0", "i <- 0", "WHILE i <= 4 DO", "total <- total + scores[i]", "i <- i + 1", "END WHILE", "OUTPUT total"]
  target_misconception: algorithm_sequencing_error
  explanation: "Initialise total and the index before the loop, add the current element and advance inside it, then output after the loop ends."
- type: mcq
  difficulty: medium
  prompt: "In an array of n values, the last value is at which index?"
  options: ["n - 1", "n", "n + 1", "1"]
  correct_answer: "n - 1"
  target_misconception: loop_boundary_offbyone
  explanation: "Because indexing starts at 0, the last index is one less than the count."
- type: predict_output
  difficulty: hard
  prompt: "Trace this and state what it outputs.\n\nscores <- [4, 9, 7]\nmax <- scores[0]\ni <- 1\nWHILE i <= 2 DO\n    IF scores[i] > max THEN\n        max <- scores[i]\n    END IF\n    i <- i + 1\nEND WHILE\nOUTPUT max"
  correct_answer: "9"
  target_misconception: array_index_value_confusion
  explanation: "max starts at scores[0] = 4; scores[1] = 9 is larger so max becomes 9; scores[2] = 7 is not larger, so max stays 9."
- type: predict_output
  difficulty: hard
  prompt: "The array scores holds [10, 20, 30]. State what this outputs.\n\nOUTPUT scores[1] + scores[2]"
  correct_answer: "50"
  target_misconception: array_index_value_confusion
  explanation: "scores[1] is 20 and scores[2] is 30, so the sum is 50; the brackets give values, not the indices 1 and 2."
```
