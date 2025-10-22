"""Calculator app with exception handling examples."""

import attrs


class DivisionByZeroError(Exception):
    """Raised when attempting to divide by zero."""

    pass


@attrs.define
class Calculator:
    """A simple calculator class demonstrating exception handling."""

    precision: int = attrs.field(default=2)
    history: list = attrs.field(factory=list)

    def calculate(self, operation: str, a: float, b: float) -> float:
        """Runner function - main entry point for calculations."""
        result = self.perform_operation(operation, a, b)
        rounded_result = round(result, self.precision)

        self.history.append(f"{a} {operation} {b} = {rounded_result}")

        return rounded_result

    def perform_operation(self, operation: str, a: float, b: float) -> float:
        """Perform the requested operation with exception handling"""
        try:
            if operation == "add":
                return a + b
            elif operation == "subtract":
                return a - b
            elif operation == "multiply":
                return a * b
            elif operation == "divide":
                return self.divide(a, b)
        except DivisionByZeroError as e:
            print(f"Error: Attempted to divide {a} by zero: {e}")

    def divide(self, a: float, b: float) -> float:
        """Perform division with validation"""
        if b == 0:
            raise DivisionByZeroError(f"Cannot divide {a} by zero")
        return a / b
