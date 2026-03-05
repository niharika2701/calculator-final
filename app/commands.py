from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.input_validators import validate_number, validate_operation
from app.exceptions import (
    OperationError, ValidationError, HistoryError, CommandError
)

from app.calculation import Calculation
class ReplCommand(ABC):
    name: str = ""
    usage: str = ""
    description: str = ""

    @abstractmethod
    def execute(
        self,
        args: list[str],
        calculator: Calculator,
        config: CalculatorConfig,
    ) -> str:
        
        pass  # pragma: no cover


class CalculateCommand(ReplCommand):
    name = "calculate"
    usage = "<operation> <a> <b>"
    description = "Perform an arithmetic operation"

    def execute(
        self,
        args: list[str],
        calculator: Calculator,
        config: CalculatorConfig,
    ) -> str:
        if len(args) != 3:
            raise CommandError(
                f"Expected: <operation> <a> <b>. Got: {' '.join(args)}"
            )
        op_name = validate_operation(args[0])
        a = validate_number(args[1], config)
        b = validate_number(args[2], config)
        result = calculator.calculate(op_name, a, b)
        return f"{op_name}({a}, {b}) = {result}"


class HistoryCommand(ReplCommand):
    name = "history"
    usage = "history"
    description = "Display all calculation history"

    def execute(self, args, calculator, config) -> str:
        entries = calculator.history
        if not entries:
            return "No history yet."
        lines = [f"  {i+1:>3}. {calc}" for i, calc in enumerate(entries)]
        return "Calculation History:\n" + "\n".join(lines)


class ClearCommand(ReplCommand):
    name = "clear"
    usage = "clear"
    description = "Clear all calculation history"

    def execute(self, args, calculator, config) -> str:
        calculator.clear_history()
        return "History cleared."


class UndoCommand(ReplCommand):
    name = "undo"
    usage = "undo"
    description = "Undo the last calculation"

    def execute(self, args, calculator, config) -> str:
        calculator.undo()
        return "Last calculation undone."


class RedoCommand(ReplCommand):
    name = "redo"
    usage = "redo"
    description = "Redo the last undone calculation"

    def execute(self, args, calculator, config) -> str:
        calculator.redo()
        return "Last undo redone."


class SaveCommand(ReplCommand):
    name = "save"
    usage = "save"
    description = "Save calculation history to CSV file"

    def execute(self, args, calculator, config) -> str:
        entries = calculator.history
        if not entries:
            return "Nothing to save."
        try:
            records = [c.to_dict() for c in entries]
            df = pd.DataFrame(records)
            df.to_csv(config.history_file, index=False,
                      encoding=config.default_encoding)
            return f"History saved to {config.history_file} ({len(records)} entries)."
        except Exception as e:
            raise CommandError(f"Failed to save history: {e}") from e


class LoadCommand(ReplCommand):
    name = "load"
    usage = "load"
    description = "Load calculation history from CSV file"

    def execute(self, args, calculator, config) -> str:
        try:
            df = pd.read_csv(config.history_file,
                             encoding=config.default_encoding)
            entries = [
                Calculation.from_dict(row)
                for row in df.to_dict(orient="records")
            ]
            calculator.get_history_object().restore(entries)
            return f"Loaded {len(entries)} entries from {config.history_file}."
        except FileNotFoundError:
            raise CommandError(
                f"No history file found at {config.history_file}. "
                "Use 'save' first."
            )
        except Exception as e:
            raise CommandError(f"Failed to load history: {e}") from e


class HelpCommand(ReplCommand):
    name = "help"
    usage = "help"
    description = "Show this help message"

    def __init__(self, command_registry: dict[str, ReplCommand]) -> None:
        self._commands = command_registry

    def execute(self, args, calculator, config) -> str:
        from app.operations import OperationFactory

        lines = []
        lines.append("=" * 55)
        lines.append("  CALCULATOR — AVAILABLE COMMANDS")
        lines.append("=" * 55)

        lines.append("\n  ARITHMETIC OPERATIONS:")
        lines.append("  " + "-" * 40)
        for name, op_class in OperationFactory.get_operations().items():
            op = op_class()
            lines.append(f"  {name:<12} {op.description}")

        lines.append("\n  REPL COMMANDS:")
        lines.append("  " + "-" * 40)
        for cmd_name, cmd in self._commands.items():
            if cmd_name != "help":
                lines.append(f"  {cmd_name:<12} {cmd.description}")
        lines.append(f"  {'help':<12} {self.description}")
        lines.append(f"  {'exit':<12} Exit the application")
        lines.append("=" * 55)
        return "\n".join(lines)


def build_command_registry() -> dict[str, ReplCommand]:
    calculate_cmd = CalculateCommand()
    history_cmd   = HistoryCommand()
    clear_cmd     = ClearCommand()
    undo_cmd      = UndoCommand()
    redo_cmd      = RedoCommand()
    save_cmd      = SaveCommand()
    load_cmd      = LoadCommand()

    registry: dict[str, ReplCommand] = {}

    from app.operations import OperationFactory
    for op_name in OperationFactory.get_operations():
        registry[op_name] = calculate_cmd

    for cmd in [history_cmd, clear_cmd, undo_cmd, redo_cmd, save_cmd, load_cmd]:
        registry[cmd.name] = cmd

    registry["help"] = HelpCommand(registry)

    return registry