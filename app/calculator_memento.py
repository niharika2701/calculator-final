from __future__ import annotations
from dataclasses import dataclass, field
from app.calculation import Calculation


@dataclass(frozen=True)
class CalcMemento:
    history_snapshot: tuple[Calculation, ...]

    @classmethod
    def from_list(cls, history: list[Calculation]) -> CalcMemento:
        return cls(history_snapshot=tuple(history))

    def to_list(self) -> list[Calculation]:
        return list(self.history_snapshot)