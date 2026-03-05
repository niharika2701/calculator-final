from __future__ import annotations
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.history import History
from app.operations import OperationFactory
from app.observers import CalculationObserver
from app.logger import Logger
from app.exceptions import HistoryError


class Calculator:
    def __init__(self, config: CalculatorConfig | None = None) -> None:
        self._config = config or CalculatorConfig.load()
        self._history = History(max_size=self._config.max_history_size)
        self._observers: list[CalculationObserver] = []
        self._logger = Logger.get_logger(self._config)

    def calculate(self, operation_name: str, a: float, b: float) -> float:
        op = OperationFactory.create(operation_name)
        calc = Calculation(op, a, b)
        result = calc.result          
        self._history.add(calc)
        self._notify_observers(calc)
        return round(result, self._config.precision)

    def add_observer(self, observer: CalculationObserver) -> None:
        self._observers.append(observer)

    def _notify_observers(self, calculation: Calculation) -> None:
        for observer in self._observers:
            observer.update(calculation)

    def undo(self) -> None:
        self._history.undo()

    def redo(self) -> None:
        self._history.redo()

    def clear_history(self) -> None:
        self._history.clear()

    @property
    def history(self) -> list[Calculation]:
        return self._history.entries

    def get_history_object(self) -> History:
        return self._history