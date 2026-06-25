---
slug: searching-sorting
name: Searching & Sorting
order: 11
prerequisites: [arrays]
summary: How to find a value in an array by checking each element, how to put an array in order by repeatedly selecting the smallest, and why sorting makes searching far faster.
estimated_minutes: 45
---

## Explanation

This lesson puts everything together. Two of the most common things a program does with a collection of values are **searching** (finding whether, and where, a value is in the array) and **sorting** (arranging the values into order). Both are built entirely from tools you already have: arrays, loops, conditionals, comparisons, and the swap.

The simplest way to search is **linear search**: start at the first element and check each one in turn until you either find the value you want or run off the end of the array. If you find it, you report its position; if you reach the end without finding it, you report that it is not there, usually with a marker like -1 (since -1 is never a valid index). It is just a loop over the indices with a comparison inside. Here is the idea as a flowchart, scanning for `target` in an array of `n` values and remembering the position in `foundIndex`:

```flowchart
{
  "nodes": [
    {"id": "s", "shape": "terminal", "text": "Start"},
    {"id": "p1", "shape": "process", "text": "foundIndex <- -1"},
    {"id": "p2", "shape": "process", "text": "i <- 0"},
    {"id": "d1", "shape": "decision", "text": "i <= n - 1 ?"},
    {"id": "d2", "shape": "decision", "text": "arr[i] = target ?"},
    {"id": "p3", "shape": "process", "text": "foundIndex <- i"},
    {"id": "p4", "shape": "process", "text": "i <- i + 1"},
    {"id": "o", "shape": "io", "text": "OUTPUT foundIndex"},
    {"id": "e", "shape": "terminal", "text": "End"}
  ],
  "edges": [
    {"from": "s", "to": "p1"},
    {"from": "p1", "to": "p2"},
    {"from": "p2", "to": "d1"},
    {"from": "d1", "to": "d2", "label": "Yes"},
    {"from": "d1", "to": "o", "label": "No"},
    {"from": "d2", "to": "p3", "label": "Yes"},
    {"from": "d2", "to": "p4", "label": "No"},
    {"from": "p3", "to": "p4"},
    {"from": "p4", "to": "d1", "label": "loop back"},
    {"from": "o", "to": "e"}
  ]
}
```

Sorting takes more work. One clear method is **selection sort**: repeatedly find the smallest value in the part of the array that is not yet sorted, and swap it to the front of that part. After the first pass the smallest value sits at index 0; after the second pass the next smallest sits at index 1; and so on. It takes several passes, one per position, to fully sort the array. Each pass reuses two things you already know: finding the smallest (a loop with a comparison, as you did to find a maximum) and the swap with a temporary variable.

Finally, why does sorting matter so much? Because a sorted array can be searched far faster with **binary search**. Instead of checking every element, you look at the middle one: if it is your target you are done; if your target is smaller you throw away the whole upper half; if larger you throw away the lower half. Each step halves what is left, so even a huge sorted array is searched in very few steps. The catch, and the key idea, is that binary search only works if the array is already sorted, which is the main reason we sort in the first place.

## Worked example

**Linear search.** Find the value 5 in the array, recording its position.

```pseudocode
arr <- [3, 8, 5, 9]
target <- 5
foundIndex <- -1
i <- 0
WHILE i <= 3 DO
    IF arr[i] = target THEN
        foundIndex <- i
    END IF
    i <- i + 1
END WHILE
OUTPUT foundIndex
```

Trace it: at `i = 0`, `arr[0] = 3` is not 5; at `i = 1`, `8` is not 5; at `i = 2`, `arr[2] = 5` matches, so `foundIndex` becomes 2; at `i = 3`, `9` is not 5. The loop ends and outputs 2, the position where 5 lives. Had the target been 6, no comparison would ever match and `foundIndex` would stay -1, the not-found marker.

**Selection sort.** Put `[29, 10, 14, 37]` in order, narrated pass by pass:

| Array now | Smallest in the unsorted part | After swapping it to the front |
|---|---|---|
| [29, 10, 14, 37] | 10 | [10, 29, 14, 37] |
| [10, 29, 14, 37] | 14 (of 29, 14, 37) | [10, 14, 29, 37] |
| [10, 14, 29, 37] | 29 (of 29, 37) | [10, 14, 29, 37] |

After three passes the array is fully sorted. Notice each pass only places one value; that is why sorting needs several passes, not one.

## Key ideas

- Searching finds whether and where a value sits in a collection; sorting arranges the collection into order.
- Linear search checks each element in turn until it finds the target or reaches the end, reporting the position or a not-found marker like -1.
- Selection sort repeatedly finds the smallest value in the unsorted part and swaps it to the front, taking several passes to finish.
- Binary search is far faster but only works on a sorted array, halving what is left each step, which is the main reason sorting is useful.

## Exercises

```yaml
- type: mcq
  difficulty: easy
  prompt: "What does linear search do?"
  options: ["Checks each element in turn until it finds the target or reaches the end", "Sorts the array into order", "Looks only at the middle element", "Adds up all the elements"]
  correct_answer: "Checks each element in turn until it finds the target or reaches the end"
  target_misconception: none
  explanation: "Linear search scans one element at a time from the start."
- type: mcq
  difficulty: easy
  prompt: "What does sorting an array do?"
  options: ["Arranges its values into order", "Finds a single value in it", "Counts how many values it has", "Removes duplicate values"]
  correct_answer: "Arranges its values into order"
  target_misconception: none
  explanation: "Sorting puts the values in order, for example smallest to largest."
- type: mcq
  difficulty: easy
  prompt: "When linear search finds the target, what does it report?"
  options: ["The position (index) where the target was found", "The value 1", "The number of elements", "The target value doubled"]
  correct_answer: "The position (index) where the target was found"
  target_misconception: array_index_value_confusion
  explanation: "It reports where the value is, its index, not the value itself."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\narr <- [3, 8, 5, 9]\ntarget <- 5\nfoundIndex <- -1\ni <- 0\nWHILE i <= 3 DO\n    IF arr[i] = target THEN\n        foundIndex <- i\n    END IF\n    i <- i + 1\nEND WHILE\nOUTPUT foundIndex"
  correct_answer: "2"
  target_misconception: array_index_value_confusion
  explanation: "5 sits at index 2, so foundIndex becomes 2; the output is the position, not the value."
- type: predict_output
  difficulty: medium
  prompt: "Trace this and state what it outputs.\n\narr <- [3, 8, 5, 9]\ntarget <- 6\nfoundIndex <- -1\ni <- 0\nWHILE i <= 3 DO\n    IF arr[i] = target THEN\n        foundIndex <- i\n    END IF\n    i <- i + 1\nEND WHILE\nOUTPUT foundIndex"
  correct_answer: "-1"
  target_misconception: loop_execution_model
  explanation: "No element equals 6, so foundIndex never changes and stays at the not-found marker -1."
- type: mcq
  difficulty: medium
  prompt: "In selection sort, what does each pass do?"
  options: ["Finds the smallest value in the unsorted part and moves it to the front", "Reverses the whole array", "Removes the largest value", "Doubles every value"]
  correct_answer: "Finds the smallest value in the unsorted part and moves it to the front"
  target_misconception: algorithm_sequencing_error
  explanation: "Selection sort selects the smallest remaining value each pass and swaps it into place."
- type: predict_output
  difficulty: medium
  prompt: "Selection sort is applied to [29, 10, 14, 37]. What is the array after the FIRST pass (the smallest value moved to the front)?"
  correct_answer: "[10, 29, 14, 37]"
  target_misconception: algorithm_sequencing_error
  explanation: "The smallest value, 10, is swapped to the front; the rest are not yet sorted."
- type: mcq
  difficulty: medium
  prompt: "Does one pass of selection sort fully sort the array?"
  options: ["No: each pass places one value, so it takes several passes", "Yes: one pass always sorts everything", "Only if the array has exactly two values", "No: selection sort never finishes"]
  correct_answer: "No: each pass places one value, so it takes several passes"
  target_misconception: algorithm_sequencing_error
  explanation: "Each pass fixes one position, so a full sort needs one pass per position."
- type: pseudocode_order
  difficulty: medium
  prompt: "Arrange these lines into a correct linear search that records the position of target in foundIndex."
  options: ["END WHILE", "foundIndex <- -1", "i <- 0", "IF arr[i] = target THEN foundIndex <- i END IF", "WHILE i <= n - 1 DO", "i <- i + 1", "OUTPUT foundIndex"]
  correct_answer: ["foundIndex <- -1", "i <- 0", "WHILE i <= n - 1 DO", "IF arr[i] = target THEN foundIndex <- i END IF", "i <- i + 1", "END WHILE", "OUTPUT foundIndex"]
  target_misconception: algorithm_sequencing_error
  explanation: "Set the marker and index before the loop, compare and advance inside it, then output after it ends."
- type: mcq
  difficulty: medium
  prompt: "Binary search is much faster than linear search, but what must be true of the array first?"
  options: ["It must already be sorted", "It must have an even number of values", "It must contain no zeros", "It must be very short"]
  correct_answer: "It must already be sorted"
  target_misconception: none
  explanation: "Binary search relies on order to decide which half to discard, so the array must be sorted."
- type: predict_output
  difficulty: hard
  prompt: "Selection sort is applied to [29, 10, 14, 37] until finished. What is the final sorted array?"
  correct_answer: "[10, 14, 29, 37]"
  target_misconception: algorithm_sequencing_error
  explanation: "Each pass places the next smallest value, giving 10, 14, 29, 37 in order."
- type: mcq
  difficulty: hard
  prompt: "Why is binary search so much faster than linear search on a large sorted array?"
  options: ["It throws away half of the remaining values at every step", "It checks two elements at once", "It never needs a loop", "It only works on small arrays"]
  correct_answer: "It throws away half of the remaining values at every step"
  target_misconception: none
  explanation: "Halving the search range each step means only a few steps are needed even for a huge array."
```
