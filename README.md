# Exception Handling Testing Examples

This project demonstrates testing patterns for exception handling in Python, designed for an intermediate testing course!

## Project Overview

This project contains a simple calculator application with deliberate exception handling patterns, along with comprehensive tests that demonstrate how to test exception handling using pytest and pytest-mock.

## Project Structure

```
exception_handling/
  src/
    exception_handling/
      __init__.py
      calculator_app.py      # Calculator with exception handling
  tests/
    test_calculator_app.py   # Test suite demonstrating exception testing patterns
  pyproject.toml
  README.md
```

## Calculator Application

The calculator (`src/exception_handling/calculator_app.py`) demonstrates three function types with different exception handling patterns:

### 1. `calculate()` - Runner Function

- **Purpose**: Main entry point that delegates to `perform_operation()`
- **Exception Handling**: None (delegates responsibility)
- **Testing Focus**: Mocking dependencies and verifying delegation

### 2. `perform_operation()` - Function with try/except

- **Purpose**: Executes arithmetic operations and handles exceptions
- **Exception Handling**: Has try/except blocks that catch `DivisionByZeroError`
- **Testing Focus**: Testing exception handling in try/except blocks using `side_effect`

### 3. `divide()` - Function with conditional raise

- **Purpose**: Performs division with validation
- **Exception Handling**: Raises `DivisionByZeroError` if divisor is zero (no try/except)
- **Testing Focus**: Testing direct exception raising using `pytest.raises`

### Custom Exception

- **`DivisionByZeroError`**: Custom exception raised when attempting to divide by zero

## Testing Patterns

The test suite (`tests/test_calculator_app.py`) demonstrates several key testing concepts:

### 1. Fixture with autospec

```python
@pytest.fixture
def mock_calculator(mocker):
    """Create a mocked Calculator instance with autospec."""
    return mocker.create_autospec(Calculator, instance=True)
```

- Uses `mocker.create_autospec()` to create a properly spec'd mock
- Ensures mocks match the actual class interface

### 2. Parametrized Tests with pytest.param

```python
@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        pytest.param("add", 10, 5, 15, id="add_positive_numbers"),
        pytest.param("subtract", 10, 5, 5, id="subtract_positive_numbers"),
        # ...
    ],
)
def test_calculate(mock_calculator, mocker, operation, a, b, expected):
    # ...
```

- Uses `pytest.param()` with descriptive IDs for clear test output
- Single test function handles multiple test cases

### 3. Class.method(self=mock, args) Pattern

```python
result = Calculator.calculate(self=mock_calculator, operation=operation, a=a, b=b)
```

- Calls class methods directly with mocked `self` parameter
- Allows testing methods in isolation without instantiating the class

### 4. Testing Exceptions with pytest.raises

```python
if error_found:
    with pytest.raises(DivisionByZeroError) as exc_info:
        Calculator.divide(self=mock_calculator, a=a, b=b)

    assert f"Cannot divide {a} by zero" in str(exc_info.value)
```

- Used for testing functions that raise exceptions directly
- Captures exception information for assertion

### 5. Testing Exception Handling with side_effect

```python
if error_found:
    mocker.patch.object(
        mock_calculator,
        "divide",
        side_effect=DivisionByZeroError(f"Cannot divide {a} by zero"),
    )
```

- Makes mocked methods raise exceptions
- Used to test try/except blocks by simulating error conditions
- Verifies that exceptions are caught and handled correctly

### 6. Conditional Test Logic with error_found Parameter

```python
@pytest.mark.parametrize(
    "a,b,expected,error_found",
    [
        pytest.param(10, 5, 2.0, False, id="divide_even_numbers"),
        pytest.param(10, 0, None, True, id="division_by_zero_raises_error"),
    ],
)
def test_divide(mock_calculator, a, b, expected, error_found):
    if error_found:
        # Test exception path
        with pytest.raises(DivisionByZeroError):
            Calculator.divide(self=mock_calculator, a=a, b=b)
    else:
        # Test success path
        result = Calculator.divide(self=mock_calculator, a=a, b=b)
        assert result == expected
```

- Uses `error_found` boolean parameter to control test behavior
- Single test function handles both success and exception cases
- Conditional setup of mocks based on test case

## Key Testing Concepts Demonstrated

### 1. Testing Functions WITHOUT try/except (divide)

- Use `pytest.raises` to verify exceptions are raised
- Test both successful cases and exception cases in one parametrized test

### 2. Testing Functions WITH try/except (perform_operation)

- Use `side_effect` to make mocked dependencies raise exceptions
- Verify exception handling behavior (e.g., print was called)
- Verify the exception is caught and handled appropriately

### 3. Testing Runner Functions (calculate)

- Mock internal dependencies
- Verify delegation to other functions
- Test data transformation (rounding, history tracking)

## Running the Tests

### Install Dependencies

```bash
# Sync all dependencies using uv
uv sync --all-extras
```

### Activate Virtual Environment

```bash
source .venv/bin/activate
```

### Run Tests

```bash
# Run all tests with verbose output
pytest tests/test_calculator_app.py -v

# Run specific test
pytest tests/test_calculator_app.py::test_divide -v

# Run with coverage
pytest tests/test_calculator_app.py --cov=exception_handling
```

## Running the Calculator Demo

```bash
python src/exception_handling/calculator_app.py
```

This will demonstrate:

- Successful arithmetic operations
- Division by zero exception handling
- Calculation history tracking

## Learning Objectives

After studying this project, you should understand:

1. How to use `mocker.create_autospec()` to create properly spec'd mocks
2. How to use `mocker.patch.object()` to mock methods
3. How to use `side_effect` to make mocks raise exceptions
4. How to use `pytest.raises` to test direct exception raising
5. How to test try/except blocks by verifying exception handling behavior
6. How to use parametrized tests with conditional logic for both success and error cases
7. How to test functions in isolation using the `Class.method(self=mock)` pattern

## Dependencies

- **attrs**: Class decorators for cleaner class definitions
- **pytest**: Testing framework
- **pytest-mock**: pytest plugin for mocking (provides `mocker` fixture)
- **mock**: Additional mocking utilities

## Course Notes

This example is intentionally simplified to focus on exception handling testing patterns. In production code, you might:

- Have more complex exception hierarchies
- Use different exception handling strategies (logging, retries, etc.)
- Test edge cases more thoroughly
- Use integration tests alongside unit tests
