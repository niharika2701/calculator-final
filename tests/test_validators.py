import pytest
from app.input_validators import validate_number, validate_operation
from app.exceptions import ValidationError
from app.calculator_config import CalculatorConfig


@pytest.fixture
def config():
    return CalculatorConfig.load()


class TestValidateNumber:
    def test_valid_integer(self, config):
        assert validate_number("42", config) == 42.0

    def test_valid_float(self, config):
        assert validate_number("3.14", config) == pytest.approx(3.14)

    def test_valid_negative(self, config):
        assert validate_number("-7", config) == -7.0

    def test_non_numeric_raises(self, config):
        with pytest.raises(ValidationError, match="not a valid number"):
            validate_number("abc", config)

    def test_empty_string_raises(self, config):
        with pytest.raises(ValidationError):
            validate_number("", config)

    def test_exceeds_max_raises(self, config):
        with pytest.raises(ValidationError, match="exceeds maximum"):
            validate_number("9e99", config)


class TestValidateOperation:
    def test_valid_name(self):
        assert validate_operation("add") == "add"

    def test_normalizes_uppercase(self):
        assert validate_operation("ADD") == "add"

    def test_strips_whitespace(self):
        assert validate_operation("  add  ") == "add"

    def test_empty_string_raises(self):
        with pytest.raises(ValidationError):
            validate_operation("")

    def test_non_string_raises(self):
        with pytest.raises(ValidationError):
            validate_operation(None)