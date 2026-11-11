# Python Basics for Explaining Code

Use these notes when describing what a piece of code does.

## Variables and types
- A variable is a name that refers to a value: `count = 0`.
- Common types: int, float, str, bool, list, tuple, dict, set, None.
- Lists are ordered and changeable. Tuples are ordered and fixed. Dicts map keys to values. Sets hold unique items.

## Functions
- Defined with `def name(parameters):`.
- `return` sends a value back. Without it the function returns None.
- Default parameters: `def greet(name="friend")`.
- A function runs only when it is called.

## Conditions
- `if`, `elif`, `else` choose between paths.
- Comparison operators: `==`, `!=`, `<`, `<=`, `>`, `>=`.
- Combine with `and`, `or`, `not`.
- Empty values (0, "", [], None) count as False.

## Loops
- `for item in collection:` repeats once per item.
- `for i in range(n):` runs with i from 0 to n-1.
- `while condition:` repeats while the condition stays true.
- `break` leaves a loop. `continue` skips to the next round.
- `enumerate(items)` gives index and item together.

## Collections
- Index starts at 0. Negative index counts from the end: `items[-1]` is the last item.
- Slice: `items[1:3]` gives index 1 and 2.
- `append` adds to a list. `len` gives the size.
- Dictionary access: `d["key"]` or `d.get("key")`.

## Comprehensions
- `[x * 2 for x in nums]` builds a new list.
- `[x for x in nums if x > 0]` filters while building.
- Also available for dicts and sets.

## Classes
- A class bundles data and behavior: `class Dog:`.
- `__init__` sets up a new object. `self` refers to that object.
- Methods are functions defined inside a class.
- Objects are created by calling the class: `d = Dog("Rex")`.

## Errors and exceptions
- `try` runs code that might fail. `except` handles a specific error. `finally` always runs.
- `raise ValueError("message")` signals a problem on purpose.

## Files and resources
- `with open("file.txt") as f:` opens a file and closes it automatically.

## Modules
- `import math` loads a module. `from math import sqrt` loads one name.
- Code under `if __name__ == "__main__":` runs only when the file is run directly.

## How to explain code well
1. Say what the whole function is for in one sentence.
2. Walk through the code in order, describing each part in plain words.
3. Mention the inputs and what is returned.
4. Point out any assumptions, such as "assumes the list is not empty".
5. Finish with the result for a small example.
