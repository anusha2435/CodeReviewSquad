# Debugging Method

A calm, step-by-step process beats random changes.

## Steps
1. Reproduce the problem. Find the smallest input that fails every time.
2. Read the error message and traceback carefully.
3. Locate the failing line, then work backwards to see where bad data came from.
4. Form a hypothesis: "I think `items` is empty here."
5. Test the hypothesis with a print statement, assert, or debugger.
6. Fix the root cause, not just the symptom.
7. Re-run the failing case and the other tests.
8. Add a test so the bug cannot return.

## Reading a traceback
- Read from the bottom up. The last line names the error type and message.
- The line just above it shows the exact failing code.
- Lines above that show the chain of calls that led there.

## Common exceptions and likely causes
| Exception | Usual cause |
|---|---|
| IndexError | Index past the end of a list, off-by-one, empty list |
| KeyError | Missing dictionary key |
| TypeError | Wrong type, such as adding a string and an int, or calling None |
| ValueError | Right type but invalid value, such as `int("abc")` or `max([])` |
| AttributeError | Object is None, or method name is misspelled |
| NameError | Variable not defined or misspelled |
| UnboundLocalError | Local variable used before it is assigned |
| ZeroDivisionError | Divisor is 0, often from empty input |
| RecursionError | Missing or unreachable base case |
| SyntaxError | Missing colon, bracket, or quote; bad indentation |
| IndentationError | Mixed tabs and spaces or wrong indentation level |

## Techniques
- Print the value and type of variables near the failure.
- Use `assert` to check assumptions.
- Use `python -m pdb script.py` or an IDE debugger to step through code.
- Simplify: remove code until the bug disappears, then add it back.
- Rubber duck: explain the code line by line out loud.
- Check recent changes first.

## Logic bugs (no error, wrong answer)
- Work through a small example by hand and compare with the program's output.
- Print intermediate values in loops.
- Check conditions: `<` vs `<=`, `and` vs `or`, missing `not`.
- Check initial values of counters, totals, and maximums.

## Habits that prevent bugs
- Write small functions that do one thing.
- Validate inputs early.
- Avoid global state.
- Run tests often.
