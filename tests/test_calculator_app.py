"""Tests for calculator_app module demonstrating exception handling testing patterns."""

import pytest

from exception_handling.calculator_app import (
    Calculator,
    DivisionByZeroError,
)


@pytest.fixture
def mock_calculator(mocker):
    """Create a mocked Calculator instance with autospec."""
    return mocker.create_autospec(Calculator, instance=True)


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        pytest.param("add", 10, 5, 15, id="add_positive_numbers"),
        pytest.param("subtract", 10, 5, 5, id="subtract_positive_numbers"),
        pytest.param("multiply", 10, 5, 50, id="multiply_positive_numbers"),
        pytest.param("divide", 10, 5, 2.0, id="divide_positive_numbers"),
    ],
)
def test_calculate(mock_calculator, mocker, operation, a, b, expected):
    """Test calculate() delegates to perform_operation and handles results correctly."""
    mocker.patch.object(mock_calculator, "perform_operation", return_value=expected)

    mock_history = mocker.MagicMock()
    mocker.patch.object(mock_calculator, "history", mock_history)
    mocker.patch.object(mock_calculator, "precision", 2)

    result = Calculator.calculate(self=mock_calculator, operation=operation, a=a, b=b)

    mock_calculator.perform_operation.assert_called_once_with(operation, a, b)

    assert result == round(expected, 2)

    mock_history.append.assert_called_once()


@pytest.mark.parametrize(
    "operation,a,b,expected,error_found,error_type",
    [
        pytest.param("add", 10, 5, 15, False, None, id="add_operation"),
        pytest.param("subtract", 10, 5, 5, False, None, id="subtract_operation"),
        pytest.param("multiply", 10, 5, 50, False, None, id="multiply_operation"),
        pytest.param("divide", 10, 5, 2.0, False, None, id="divide_operation"),
        pytest.param(
            "divide",
            10,
            0,
            None,
            True,
            DivisionByZeroError,
            id="division_by_zero_error",
        ),
    ],
)
def test_perform_operation(
    mock_calculator, mocker, operation, a, b, expected, error_found, error_type
):
    """Test perform_operation() for both successful operations and exception handling"""
    mock_print = mocker.patch("builtins.print")
    caught_error = None

    if error_found:
        mock_calculator.divide.side_effect = lambda *args, **kwargs: (
            _ for _ in ()
        ).throw(DivisionByZeroError(f"Cannot divide {a} by zero"))
    else:
        if operation == "divide":
            mocker.patch.object(mock_calculator, "divide", return_value=expected)

    try:
        result = Calculator.perform_operation(
            self=mock_calculator, operation=operation, a=a, b=b
        )
    except DivisionByZeroError as error:
        caught_error = error
        assert error_found, "Error should only be raised if error_found is True"

    if error_found:
        assert (
            caught_error is None
        ), "Exception should be caught by perform_operation, not escape"

        mock_print.assert_called_once()

        assert result is None
    else:
        assert result == expected

    if operation == "divide":
        mock_calculator.divide.assert_called_once_with(a, b)


@pytest.mark.parametrize(
    "a,b,expected,error_found",
    [
        pytest.param(10, 5, 2.0, False, id="divide_even_numbers"),
        pytest.param(10, 3, 10 / 3, False, id="divide_with_remainder"),
        pytest.param(0, 5, 0.0, False, id="divide_zero_numerator"),
        pytest.param(-10, 5, -2.0, False, id="divide_negative_numerator"),
        pytest.param(10, -5, -2.0, False, id="divide_negative_denominator"),
        pytest.param(10, 0, None, True, id="division_by_zero_raises_error"),
        pytest.param(-10, 0, None, True, id="negative_divided_by_zero"),
    ],
)
def test_divide(mock_calculator, a, b, expected, error_found):
    """Test divide() for both successful divisions and exception raising."""
    if error_found:
        with pytest.raises(DivisionByZeroError) as exc_info:
            Calculator.divide(self=mock_calculator, a=a, b=b)

        assert f"Cannot divide {a} by zero" in str(exc_info.value)
    else:
        result = Calculator.divide(self=mock_calculator, a=a, b=b)
        assert result == expected
