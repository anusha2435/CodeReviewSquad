# Python Naming Conventions

Good names make code readable without needing comments.

## Standard patterns
| Item | Style | Example |
|---|---|---|
| Variables | snake_case | `total_price` |
| Functions | snake_case | `calculate_average` |
| Methods | snake_case | `get_name` |
| Classes | CapWords (PascalCase) | `ShoppingCart` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES` |
| Modules/files | short snake_case | `data_utils.py` |
| Private by convention | leading underscore | `_internal_helper` |

## Rules of thumb
- Names should describe purpose: `user_count` is better than `n` or `x1`.
- Functions are actions, so use verbs: `parse_input`, `send_email`.
- Booleans read like questions: `is_valid`, `has_items`.
- Collections use plural names: `users`, `order_ids`.

## Names to avoid
- Single letters like `l`, `O`, `I`. They look like digits 1 and 0.
- Vague names such as `data`, `temp`, `stuff`, `foo` unless truly temporary.
- Names that shadow built-ins: `list`, `dict`, `str`, `id`, `max`, `min`, `sum`, `input`, `type`, `len`.
  - Example: `list = [1, 2]` breaks later calls to `list(...)`.
  - Use `items`, `values`, `max_value` instead.
- CamelCase function names such as `GetMax`. Use `get_max`.
- Misleading names, such as `user_list` that is actually a dictionary.

## Loop variables
- Short names are fine for tiny loops: `for i in range(n)`.
- Prefer meaningful names when the body is longer: `for student in students`.
- Use `_` for a value you intentionally ignore.

## Class naming
- Class names are nouns: `Invoice`, `Parser`.
- Exception classes end with `Error`: `ValidationError`.

## Consistency
- Pick one style and keep it across the whole file.
- Do not rename public functions without updating all callers.
