# Edge Case Checklist

Edge cases are unusual inputs where code often fails. Check each one against the function.

## Empty inputs
- Empty list `[]`, empty string `""`, empty dict `{}`, empty tuple.
- Typical failures: IndexError on `items[0]`, ZeroDivisionError on `sum(items) / len(items)`, `max([])` raising ValueError.

## None
- A parameter may be None when the caller passes nothing.
- Typical failures: `AttributeError: 'NoneType' object has no attribute ...`, TypeError on `len(None)`.

## Zero
- Division and modulo by zero.
- Logarithm or square root of zero or a negative number.
- Loops that run zero times: is the result variable still defined?

## Negative numbers
- Negative indexes silently count from the end.
- Floor division and modulo behave differently for negatives.
- Negative sizes, ages, or counts may be invalid.

## Single element
- A list with one item: does the loop or comparison still work?
- Sorting, min, max, and pairwise comparisons need at least 2 items.

## Duplicates
- Repeated values in lists. Does the function count them once or many times?
- Ties when finding the maximum or ranking.

## Boundaries
- First and last index, smallest and largest allowed value.
- Exactly equal to the threshold: is it `<` or `<=`?

## Large inputs
- Very large numbers or very long lists. Watch for slow nested loops and memory use.
- Deep recursion can raise RecursionError. Python's default limit is about 1000.

## Wrong types
- String where a number is expected, float where an int is expected.
- Mixed lists like `[1, "a", 2]`.
- Decide: should the function raise TypeError or convert the value?

## Special characters and text
- Spaces, tabs, newlines, Unicode characters, upper and lower case.
- Leading and trailing whitespace in user input.

## Floating point
- Rounding errors such as `0.1 + 0.2`.
- Comparing floats with `==`. Use `math.isclose`.

## Order and state
- Sorted vs unsorted input.
- Calling a function twice in a row. Does leftover state change the second result?
- Input that is modified by the function when the caller did not expect it.

## What to do when you find one
- Return a clear result such as None or 0, or raise a specific exception with a helpful message.
- Document the chosen behavior in the docstring.
