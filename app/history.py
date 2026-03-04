from __future__ import annotations
from app.calculation import Calculation
from app.calculator_memento import CalcMemento
from app.exceptions import HistoryError


class History:
    def __init__(self, max_size: int = 100) -> None:
        self._entries: list[Calculation] = []
        self._undo_stack: list[CalcMemento] = []
        self._redo_stack: list[CalcMemento] = []
        self._max_size = max_size

    @property
    def entries(self) -> list[Calculation]:
        return list(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    def add(self, calculation: Calculation) -> None:
        self._undo_stack.append(CalcMemento.from_list(self._entries))
        self._redo_stack.clear()
        self._entries.append(calculation)

        if len(self._entries) > self._max_size:
            self._entries = self._entries[-self._max_size:]

    def undo(self) -> None:
        if not self._undo_stack:
            raise HistoryError("Nothing to undo.")
        self._redo_stack.append(CalcMemento.from_list(self._entries))
        memento = self._undo_stack.pop()
        self._entries = memento.to_list()

    def redo(self) -> None:
        if not self._redo_stack:
            raise HistoryError("Nothing to redo.")
        self._undo_stack.append(CalcMemento.from_list(self._entries))
        memento = self._redo_stack.pop()
        self._entries = memento.to_list()

    def clear(self) -> None:
        self._entries.clear()
        self._undo_stack.clear()
        self._redo_stack.clear()

    def get_last(self) -> Calculation:
        if not self._entries:
            raise HistoryError("No calculations in history.")
        return self._entries[-1]

    def restore(self, entries: list[Calculation]) -> None:
        self._entries = list(entries)
        self._undo_stack.clear()
        self._redo_stack.clear()