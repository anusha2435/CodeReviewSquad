# Writing Good Tests

## What a good test is
- Small: checks one behavior.
- Independent: does not rely on another test running first.
- Repeatable: same result every run, no randomness or network.
- Readable: the name says what is tested and what should happen.

## Naming
- Pattern: `test_<function>_<situation>_<expected>`.
- Examples: `test_average_empty_list_raises`, `test_get_max_single_item_returns_item`.

## What to cover
1. Normal cases: typical valid inputs.
2. Edge cases: empty, None, zero, negative, single element, duplicates, boundaries.
3. Error cases: invalid input that should raise an exception.
4. Regression cases: the exact input that caused a past bug.

## How many tests
- For a small function, 5 to 8 focused tests are usually enough.
- Add more only when the logic has many branches.

## Example set for `average(numbers)`
- `[1, 2, 3]` returns 2.0.
- `[5]` returns 5.0.
- `[-1, 1]` returns 0.0.
- `[0.1, 0.2]` returns about 0.15 (use approx).
- `[]` raises ValueError.

## Good practices
- Write the expected value by hand from the requirement, not by running the code and copying the output.
- Test behavior, not internal steps.
- Keep test data small and obvious.
- One logical assertion per test where possible.
- Do not print in tests. Use assertions.
- Avoid testing the same thing many times.

## Mistakes to avoid
- Tests with no assert.
- Tests that always pass, such as `assert True`.
- Expected values computed with the same buggy logic as the code.
- Huge inputs that make tests slow.
- Reading files, using the network, or relying on the current time.
- Tests that change shared state and break other tests.

## If a test fails
- Decide first: is the code wrong or is the test wrong?
- Compare with the requirement or docstring.
- Fix the real cause. Do not weaken the test just to make it pass.

## Mutable default check
A good test calls a function twice in a row to confirm results do not leak between calls.
