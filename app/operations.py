from abc import ABC, abstractmethod
from app.exceptions import OperationError, ValidationError

_operation_registry: dict[str, type] = {}

def register_operation(name: str, description: str):
    
    def decorator(cls):
        cls.name = name
        cls.description = description
        _operation_registry[name] = cls
        return cls
    return decorator

class Operation(ABC):
    name: str = ""
    description: str = ""

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        
        pass  # pragma: no cover


@register_operation("add", "Add two numbers:          add 3 5")
class Add(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b


@register_operation("subtract", "Subtract b from a:        subtract 10 3")
class Subtract(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b


@register_operation("multiply", "Multiply two numbers:     multiply 4 5")
class Multiply(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b


@register_operation("divide", "Divide a by b:            divide 10 2")
class Divide(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot divide by zero")
        return a / b


@register_operation("power", "Raise a to power of b:    power 2 8")
class Power(Operation):
    def execute(self, a: float, b: float) -> float:
        return a ** b


@register_operation("root", "b-th root of a:           root 27 3")
class Root(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Root degree cannot be zero")
        if a < 0:
            raise OperationError("Cannot take root of negative number")
        return a ** (1 / b)


@register_operation("modulus", "Remainder of a / b:       modulus 10 3")
class Modulus(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot modulo by zero")
        return a % b


@register_operation("int_divide", "Integer division a // b:  int_divide 10 3")
class IntDivide(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot divide by zero")
        return a // b


@register_operation("percent", "Percentage a of b:        percent 50 200")
class Percent(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise OperationError("Cannot divide by zero")
        return (a / b) * 100


@register_operation("abs_diff", "Absolute difference |a-b|: abs_diff 5 3")
class AbsDiff(Operation):
    def execute(self, a: float, b: float) -> float:
        return abs(a - b)

class OperationFactory:
    @classmethod
    def create(cls, operation_name: str) -> Operation:
        op_class = _operation_registry.get(operation_name.lower())
        if op_class is None:
            raise ValidationError(
                f"Unknown operation: '{operation_name}'. "
                f"Valid: {list(_operation_registry.keys())}"
            )
        return op_class()

    @classmethod
    def get_operations(cls) -> dict[str, type[Operation]]:
        return _operation_registry.copy()