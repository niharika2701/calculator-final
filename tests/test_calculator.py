import pytest
from unittest.mock import MagicMock
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError, HistoryError


@pytest.fixture
def config():
    return CalculatorConfig.load()


@pytest.fixture
def calculator(config):
    return Calculator(config)


class TestCalculatorBasicOps:
    @pytest.mark.parametrize("op, a, b, expected", [
        ("add", 3, 5, 8),
        ("subtract", 10, 4, 6),
        ("multiply", 3, 4, 12),
        ("divide", 10, 2, 5),
        ("power", 2, 3, 8),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 50, 200, 25.0),
        ("abs_diff", 5, 3, 2),
    ])
    def test_calculate(self, calculator, op, a, b, expected):
        result = calculator.calculate(op, a, b)
        assert result == expected

    def test_calculate_adds_to_history(self, calculator):
        calculator.calculate("add", 1, 2)
        assert len(calculator.history) == 1

    def test_divide_by_zero_raises(self, calculator):
        with pytest.raises(OperationError):
            calculator.calculate("divide", 10, 0)

    def test_invalid_operation_raises(self, calculator):
        with pytest.raises(ValidationError):
            calculator.calculate("teleport", 1, 2)


class TestCalculatorUndoRedo:
    def test_undo_removes_last(self, calculator):
        calculator.calculate("add", 1, 2)
        calculator.undo()
        assert len(calculator.history) == 0

    def test_redo_restores(self, calculator):
        calculator.calculate("add", 1, 2)
        calculator.undo()
        calculator.redo()
        assert len(calculator.history) == 1

    def test_undo_empty_raises(self, calculator):
        with pytest.raises(HistoryError):
            calculator.undo()

    def test_redo_empty_raises(self, calculator):
        with pytest.raises(HistoryError):
            calculator.redo()


class TestCalculatorObservers:
    def test_observer_is_notified(self, calculator):
        mock_observer = MagicMock()
        calculator.add_observer(mock_observer)
        calculator.calculate("add", 1, 2)
        mock_observer.update.assert_called_once()

    def test_multiple_observers_all_notified(self, calculator):
        obs1 = MagicMock()
        obs2 = MagicMock()
        calculator.add_observer(obs1)
        calculator.add_observer(obs2)
        calculator.calculate("add", 1, 2)
        obs1.update.assert_called_once()
        obs2.update.assert_called_once()

    def test_observer_not_notified_on_error(self, calculator):
        mock_observer = MagicMock()
        calculator.add_observer(mock_observer)
        with pytest.raises(OperationError):
            calculator.calculate("divide", 10, 0)
        mock_observer.update.assert_not_called()


class TestCalculatorHistory:
    def test_clear_history(self, calculator):
        calculator.calculate("add", 1, 2)
        calculator.clear_history()
        assert len(calculator.history) == 0

    def test_get_history_entries(self, calculator):
        calculator.calculate("add", 1, 2)
        calculator.calculate("multiply", 3, 4)
        assert len(calculator.history) == 2