from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from app.operations import Operation, OperationFactory


@dataclass
class Calculation:
    operation: Operation
    a: float
    b: float
    timestamp: datetime = field(default_factory=datetime.now)
    _result: float | None = field(init=False, repr=False, default=None)

    @property
    def result(self) -> float:
        if self._result is None:
            self._result = self.operation.execute(self.a, self.b)
        return self._result

    def __str__(self) -> str:
        return (
            f"{self.operation.name}({self.a}, {self.b}) "
            f"= {self.result} "
            f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]"
        )

    def to_dict(self) -> dict:
        return {
            "operation": self.operation.name,
            "a": self.a,
            "b": self.b,
            "result": self.result,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Calculation:
        op = OperationFactory.create(data["operation"])
        calc = cls(
            operation=op,
            a=float(data["a"]),
            b=float(data["b"]),
            timestamp=datetime.fromisoformat(str(data["timestamp"])),
        )
        return calc