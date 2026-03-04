from app.exceptions import ValidationError
from app.calculator_config import CalculatorConfig


def validate_number(value: str, config: CalculatorConfig) -> float:
    try:
        number = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f"'{value}' is not a valid number.")

    if abs(number) > config.max_input_value:
        raise ValidationError(
            f"Value {number} exceeds maximum allowed input "
            f"({config.max_input_value})."
        )
    return number

def validate_operation(name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Operation name must be a non-empty string.")
    return name.strip().lower()