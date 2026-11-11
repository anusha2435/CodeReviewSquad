# Docstrings and Type Hints

Docstrings explain what code does. Type hints say what types it expects.

## Docstring basics (PEP 257)
- Every public module, class, function, and method should have a docstring.
- Use triple double quotes: `"""Text."""`.
- The first line is a short summary in one sentence, ending with a period.
- Use the imperative mood: "Return the average", not "Returns the average".
- For longer docstrings, leave a blank line after the summary.

## One-line example
```python
def square(x):
    """Return x multiplied by itself."""
    return x * x
```

## Multi-line example
```python
def average(numbers):
    """Return the mean of a list of numbers.

    Args:
        numbers: A non-empty list of ints or floats.

    Returns:
        The arithmetic mean as a float.

    Raises:
        ValueError: If the list is empty.
    """
```

## What to document
- What the function does, not how it does it.
- Parameters, return value, and exceptions raised.
- Edge case behavior, such as what happens with empty input.

## Type hints
- Annotate parameters and return values: `def add(a: int, b: int) -> int:`.
- Common types: `int`, `float`, `str`, `bool`, `list[int]`, `dict[str, int]`.
- Optional value: `str | None` (Python 3.10+) or `Optional[str]`.
- A function that returns nothing: `-> None`.
- Type hints are not enforced at run time. Tools like mypy can check them.

## Common mistakes
- Docstring that repeats the function name: "Calculates average" for `calculate_average`.
- Out-of-date docstring after the code changed.
- Missing docstring on public functions.
- Type hint that disagrees with the real behavior.

## Comments vs docstrings
- Docstrings describe the interface for users of the function.
- Comments describe tricky internal logic for maintainers.
