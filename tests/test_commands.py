import pytest
import os
from unittest.mock import MagicMock, patch
from app.commands import (
    CalculateCommand, HistoryCommand, ClearCommand,
    UndoCommand, RedoCommand, SaveCommand, LoadCommand,
    HelpCommand, build_command_registry,
)
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import CommandError, HistoryError, OperationError


@pytest.fixture
def config():
    return CalculatorConfig.load()


@pytest.fixture
def calculator(config):
    return Calculator(config)


@pytest.fixture
def registry():
    return build_command_registry()


class TestCalculateCommand:
    def test_basic_addition(self, calculator, config):
        cmd = CalculateCommand()
        result = cmd.execute(["add", "3", "5"], calculator, config)
        assert "8" in result

    def test_wrong_arg_count_raises(self, calculator, config):
        cmd = CalculateCommand()
        with pytest.raises(CommandError):
            cmd.execute(["add", "3"], calculator, config)

    def test_invalid_number_raises(self, calculator, config):
        cmd = CalculateCommand()
        with pytest.raises(Exception):
            cmd.execute(["add", "abc", "3"], calculator, config)

    def test_divide_by_zero_raises(self, calculator, config):
        cmd = CalculateCommand()
        with pytest.raises(OperationError):
            cmd.execute(["divide", "10", "0"], calculator, config)


class TestHistoryCommand:
    def test_empty_history_message(self, calculator, config):
        result = HistoryCommand().execute([], calculator, config)
        assert "No history" in result

    def test_shows_entries(self, calculator, config):
        calculator.calculate("add", 3, 5)
        result = HistoryCommand().execute([], calculator, config)
        assert "add" in result


class TestClearCommand:
    def test_clears_history(self, calculator, config):
        calculator.calculate("add", 1, 2)
        ClearCommand().execute([], calculator, config)
        assert len(calculator.history) == 0

    def test_returns_confirmation(self, calculator, config):
        result = ClearCommand().execute([], calculator, config)
        assert "cleared" in result.lower()


class TestUndoRedoCommands:
    def test_undo_removes_entry(self, calculator, config):
        calculator.calculate("add", 1, 2)
        UndoCommand().execute([], calculator, config)
        assert len(calculator.history) == 0

    def test_redo_restores_entry(self, calculator, config):
        calculator.calculate("add", 1, 2)
        UndoCommand().execute([], calculator, config)
        RedoCommand().execute([], calculator, config)
        assert len(calculator.history) == 1

    def test_undo_empty_raises(self, calculator, config):
        with pytest.raises(HistoryError):
            UndoCommand().execute([], calculator, config)

    def test_redo_empty_raises(self, calculator, config):
        with pytest.raises(HistoryError):
            RedoCommand().execute([], calculator, config)


class TestSaveLoadCommands:
    def test_save_empty_returns_message(self, calculator, config):
        result = SaveCommand().execute([], calculator, config)
        assert "Nothing" in result

    def test_save_creates_file(self, calculator, config):
        calculator.calculate("add", 1, 2)
        SaveCommand().execute([], calculator, config)
        assert os.path.exists(config.history_file)

    def test_load_no_file_raises(self, calculator, config):
        import tempfile, os
        with tempfile.TemporaryDirectory() as d:
            cfg = CalculatorConfig.load()
            cfg.history_file = os.path.join(d, "nonexistent.csv")  # type: ignore
            with pytest.raises(CommandError, match="No history file"):
                LoadCommand().execute([], calculator, cfg)

    def test_save_then_load_round_trips(self, calculator, config):
        calculator.calculate("add", 3, 5)
        SaveCommand().execute([], calculator, config)
        calculator.clear_history()
        LoadCommand().execute([], calculator, config)
        assert len(calculator.history) == 1


class TestHelpCommand:
    def test_help_contains_operations(self, registry, calculator, config):
        result = registry["help"].execute([], calculator, config)
        assert "add" in result
        assert "subtract" in result

    def test_help_contains_commands(self, registry, calculator, config):
        result = registry["help"].execute([], calculator, config)
        assert "history" in result
        assert "undo" in result
        assert "save" in result


class TestBuildCommandRegistry:
    def test_all_operations_in_registry(self, registry):
        from app.operations import OperationFactory
        for op in OperationFactory.get_operations():
            assert op in registry

    def test_utility_commands_in_registry(self, registry):
        for name in ["history", "clear", "undo", "redo", "save", "load", "help"]:
            assert name in registry
