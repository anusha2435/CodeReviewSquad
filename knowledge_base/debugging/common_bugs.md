# Common Python Bugs

## Mutable default argument
`def add(item, items=[])` creates the list once and shares it across all calls.
Fix: use `items=None`, then `if items is None: items = []` inside the function.

## Off-by-one errors
- `range(len(a) + 1)` goes one index past the end and causes IndexError.
- `range(1, n)` excludes `n`. Use `range(1, n + 1)` to include it.
- Slices exclude the end index: `a[0:3]` gives 3 items.
- Check the first and last iteration by hand.

## Division by zero
- `total / len(items)` fails when `items` is empty.
- Check for an empty list or zero denominator first, or raise a clear ValueError.

## Comparing to None with ==
Use `is None` or `is not None`. Using `==` can behave wrongly with custom objects.

## Bare except
`except:` also catches KeyboardInterrupt and hides real errors.
Catch specific exceptions like `except ValueError:` and handle or re-raise them.

## Modifying a list while iterating over it
Removing items from a list inside `for x in items:` skips elements.
Fix: iterate over a copy `for x in items[:]`, or build a new list with a comprehension.

## Integer vs float division
- `/` always returns a float in Python 3.
- `//` is floor division and rounds toward negative infinity: `-7 // 2` is `-4`.
- Use `%` carefully with negative numbers.

## Shadowing built-ins
Naming a variable `list`, `max`, `sum`, `id` or `input` breaks later use of the built-in.

## Late-binding closures
Lambdas created in a loop all use the final loop value.
Fix: bind the value as a default argument: `lambda x, i=i: x + i`.

## Unclosed files and resources
Use `with open(path) as f:` so the file closes even if an error occurs.

## String and type mix-ups
- `input()` always returns a string. Convert with `int()` or `float()`.
- `"5" + 5` raises TypeError.
- Comparing `"10" < "9"` compares text, not numbers.

## Variable scope
- Assigning to a global name inside a function creates a new local variable.
- Use `global` only when truly needed, or pass values and return results instead.
- Using a variable before assignment raises UnboundLocalError.

## Equality vs identity
- Use `==` to compare values and `is` only for None, True, False.
- Floating point: `0.1 + 0.2 == 0.3` is False. Use `math.isclose`.

## Infinite loops
Check that the loop condition changes inside the loop body, and that `break` conditions are reachable.

## Missing return
A function without `return` gives back None, which causes errors later.
Check every code path returns a value.

## Dictionary access
`d[key]` raises KeyError when the key is missing. Use `d.get(key, default)` or check `key in d`.
