# PEP 8 Summary

PEP 8 is the standard style guide for Python code. Following it makes code easier to read and review.

## Indentation
- Use 4 spaces per indentation level.
- Never mix tabs and spaces.
- Continuation lines should align with the opening bracket or use a hanging indent.

## Line length
- PEP 8 recommends a maximum of 79 characters per line.
- Many teams accept 88 to 100. Be consistent within a project.
- Break long lines inside brackets instead of using backslashes.
- flake8 code: E501 (line too long).

## Blank lines
- Two blank lines between top-level functions and classes.
- One blank line between methods inside a class.
- Use single blank lines inside functions to separate logical steps.
- flake8 codes: E302 (expected 2 blank lines), E303 (too many blank lines).

## Imports
- Put imports at the top of the file.
- One import per line: `import os` and `import sys`, not `import os, sys`.
- Group in this order, with a blank line between groups: standard library, third-party, local modules.
- Avoid wildcard imports like `from module import *`.
- Remove unused imports. flake8 code: F401.

## Whitespace
- One space around operators and after commas: `x = a + b`, `f(a, b)`.
- No space before a comma, colon, or opening bracket: `f(x)`, not `f (x)`.
- No spaces around `=` for keyword arguments: `f(x=1)`.
- No trailing whitespace at the end of lines. flake8 code: W291.
- End the file with exactly one newline. flake8 code: W292.
- flake8 code: E225 (missing whitespace around operator).

## Comparisons
- Compare to None with `is` or `is not`, never `==`. flake8 code: E711.
- Use `if flag:` instead of `if flag == True:`. flake8 code: E712.
- Use `isinstance(x, int)` instead of `type(x) == int`.
- Use `if not items:` to test for an empty list.

## Exceptions
- Never use a bare `except:`. Catch specific exceptions. flake8 code: E722.
- Keep the `try` block as small as possible.

## Comments
- Write comments that explain why, not what.
- Keep comments up to date. A wrong comment is worse than none.
- Start block comments with `# ` (hash and one space).

## Unused code
- Remove variables that are assigned but never used. flake8 code: F841.
- Remove commented-out code. Version control keeps history.
