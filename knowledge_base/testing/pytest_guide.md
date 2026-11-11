# pytest Guide

pytest is the most common Python testing tool.

## Basics
- Test files are named `test_*.py` or `*_test.py`.
- Test functions start with `test_`.
- Use plain `assert` statements.
- Run all tests with `pytest`. Run quietly with `pytest -q`.
- Stop at the first failure with `pytest -x`.

## Simple example
```python
from solution import add

def test_add_positive_numbers():
    assert add(2, 3) == 5
```

## Arrange, Act, Assert
1. Arrange: set up inputs.
2. Act: call the function.
3. Assert: check the result.

## Testing exceptions
```python
import pytest
from solution import average

def test_average_empty_list_raises():
    with pytest.raises(ValueError):
        average([])
```
- Use `pytest.raises(SomeError)` when the function should fail on bad input.
- Add `match="text"` to check part of the error message.

## Testing floats
```python
import pytest

def test_float_result():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

## parametrize: many cases, one test
```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

## Fixtures: shared setup
```python
import pytest

@pytest.fixture
def sample_list():
    return [3, 1, 2]

def test_sorted(sample_list):
    assert sorted(sample_list) == [1, 2, 3]
```

## Importing the code under test
- Put the code in `solution.py` and use `from solution import *` or `from solution import function_name`.
- Do not copy the function into the test file.

## Useful options
- `pytest -v` shows each test name.
- `pytest -k name` runs tests matching a name.
- `pytest --tb=short` gives shorter tracebacks.

## Reading failures
- pytest shows the failing assert, the values on each side, and the line number.
- "assert 3 == 4" means actual was 3 and expected was 4.
