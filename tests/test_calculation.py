import pytest
from datetime import datetime
from app.calculation import Calculation
from app.operations import OperationFactory
from app.exceptions import OperationError


class TestCalculation:
    def setup_method(self):
        self.add = OperationFactory.create("add")
        self.divide = OperationFactory.create("divide")

    def test_stores_operands_and_operation(self):
        calc = Calculation(self.add, 3, 5)
        assert calc.a == 3
        assert calc.b == 5
        assert calc.operation is self.add

    def test_result_is_computed_correctly(self):
        assert Calculation(self.add, 3, 5).result == 8

    def test_result_is_cached(self):
        calc = Calculation(self.add, 3, 5)
        r1 = calc.result
        r2 = calc.result
        assert r1 == r2

    def test_has_timestamp(self):
        calc = Calculation(self.add, 3, 5)
        assert isinstance(calc.timestamp, datetime)

    def test_str_contains_key_info(self):
        text = str(Calculation(self.add, 3, 5))
        assert "add" in text
        assert "3" in text
        assert "5" in text
        assert "8" in text

    def test_to_dict_has_all_keys(self):
        d = Calculation(self.add, 3, 5).to_dict()
        assert set(d.keys()) == {"operation", "a", "b", "result", "timestamp"}

    def test_to_dict_values_are_correct(self):
        d = Calculation(self.add, 3, 5).to_dict()
        assert d["operation"] == "add"
        assert d["a"] == 3
        assert d["b"] == 5
        assert d["result"] == 8

    def test_from_dict_round_trips(self):
        original = Calculation(self.add, 3, 5)
        restored = Calculation.from_dict(original.to_dict())
        assert restored.a == original.a
        assert restored.b == original.b
        assert restored.result == original.result

    def test_from_dict_restores_timestamp(self):
        original = Calculation(self.add, 3, 5)
        restored = Calculation.from_dict(original.to_dict())
        assert restored.timestamp == original.timestamp

    def test_operation_error_propagates(self):
        calc = Calculation(self.divide, 10, 0)
        with pytest.raises(OperationError):
            _ = calc.result