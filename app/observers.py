from __future__ import annotations
from abc import ABC, abstractmethod
import logging
import pandas as pd
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig


class CalculationObserver(ABC):
    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        pass  # pragma: no cover


class LoggingObserver(CalculationObserver):
    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    def update(self, calculation: Calculation) -> None:
        self._logger.info(
            "CALCULATION | op=%s | a=%s | b=%s | result=%s",
            calculation.operation.name,
            calculation.a,
            calculation.b,
            calculation.result,
        )

class AutoSaveObserver(CalculationObserver):
    def __init__(self, config: CalculatorConfig, history) -> None:
        self._config = config
        self._history = history

    def update(self, calculation: Calculation) -> None:
        if not self._config.auto_save:
            return
        try:
            records = [c.to_dict() for c in self._history.entries]
            df = pd.DataFrame(records)
            df.to_csv(
                self._config.history_file,
                index=False,
                encoding=self._config.default_encoding,
            )
        except Exception as exc:  # pragma: no cover
            pass  # Silent fail on auto-save: don't crash the REPL