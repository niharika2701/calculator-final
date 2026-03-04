import pytest
from app.operations import OperationFactory, Operation
from app.exceptions import OperationError, ValidationError


class TestAddition:
    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 5), (-1, 1, 0), (0, 0, 0), (1.5, 2.5, 4.0), (-5, -3, -8),
    ])
    def test_add(self, a, b, expected):
        assert OperationFactory.create("add").execute(a, b) == expected


class TestSubtraction:
    @pytest.mark.parametrize("a, b, expected", [
        (5, 3, 2), (0, 5, -5), (-3, -3, 0), (1.5, 0.5, 1.0),
    ])
    def test_subtract(self, a, b, expected):
        assert OperationFactory.create("subtract").execute(a, b) == expected


class TestMultiplication:
    @pytest.mark.parametrize("a, b, expected", [
        (3, 4, 12), (-2, 5, -10), (0, 100, 0), (1.5, 2, 3.0),
    ])
    def test_multiply(self, a, b, expected):
        assert OperationFactory.create("multiply").execute(a, b) == expected


class TestDivision:
    @pytest.mark.parametrize("a, b, expected", [
        (10, 2, 5.0), (-6, 3, -2.0), (1, 4, 0.25),
    ])
    def test_divide(self, a, b, expected):
        assert OperationFactory.create("divide").execute(a, b) == expected

    def test_divide_by_zero_raises(self):
        with pytest.raises(OperationError, match="Cannot divide by zero"):
            OperationFactory.create("divide").execute(10, 0)


class TestPower:
    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 8), (5, 0, 1), (2, -1, 0.5), (9, 0.5, 3.0),
    ])
    def test_power(self, a, b, expected):
        assert OperationFactory.create("power").execute(a, b) == pytest.approx(expected)


class TestRoot:
    @pytest.mark.parametrize("a, b, expected", [
        (27, 3, 3.0), (16, 2, 4.0), (1, 5, 1.0),
    ])
    def test_root(self, a, b, expected):
        assert OperationFactory.create("root").execute(a, b) == pytest.approx(expected)

    def test_root_of_negative_raises(self):
        with pytest.raises(OperationError, match="Cannot take root of negative"):
            OperationFactory.create("root").execute(-8, 3)

    def test_root_zero_degree_raises(self):
        with pytest.raises(OperationError, match="Root degree cannot be zero"):
            OperationFactory.create("root").execute(8, 0)


class TestModulus:
    @pytest.mark.parametrize("a, b, expected", [
        (10, 3, 1), (15, 5, 0), (-7, 3, 2),
    ])
    def test_modulus(self, a, b, expected):
        assert OperationFactory.create("modulus").execute(a, b) == expected

    def test_modulus_by_zero_raises(self):
        with pytest.raises(OperationError, match="Cannot modulo by zero"):
            OperationFactory.create("modulus").execute(10, 0)


class TestIntDivide:
    @pytest.mark.parametrize("a, b, expected", [
        (10, 3, 3), (15, 5, 3), (-7, 2, -4),
    ])
    def test_int_divide(self, a, b, expected):
        assert OperationFactory.create("int_divide").execute(a, b) == expected

    def test_int_divide_by_zero_raises(self):
        with pytest.raises(OperationError, match="Cannot divide by zero"):
            OperationFactory.create("int_divide").execute(10, 0)


class TestPercent:
    @pytest.mark.parametrize("a, b, expected", [
        (50, 200, 25.0), (1, 4, 25.0), (0, 100, 0.0),
    ])
    def test_percent(self, a, b, expected):
        assert OperationFactory.create("percent").execute(a, b) == expected

    def test_percent_zero_denominator_raises(self):
        with pytest.raises(OperationError, match="Cannot divide by zero"):
            OperationFactory.create("percent").execute(50, 0)


class TestAbsDiff:
    @pytest.mark.parametrize("a, b, expected", [
        (5, 3, 2), (3, 5, 2), (-4, -1, 3), (0, 0, 0),
    ])
    def test_abs_diff(self, a, b, expected):
        assert OperationFactory.create("abs_diff").execute(a, b) == expected


class TestOperationFactory:
    def test_invalid_operation_raises(self):
        with pytest.raises(ValidationError, match="Unknown operation"):
            OperationFactory.create("teleport")

    def test_create_returns_operation_instance(self):
        op = OperationFactory.create("add")
        assert isinstance(op, Operation)

    def test_all_operations_registered(self):
        expected = {
            "add", "subtract", "multiply", "divide", "power",
            "root", "modulus", "int_divide", "percent", "abs_diff"
        }
        assert expected.issubset(set(OperationFactory.get_operations().keys()))

    def test_get_operations_returns_copy(self):
        ops = OperationFactory.get_operations()
        ops["hacked"] = None
        assert "hacked" not in OperationFactory.get_operations()

    def test_each_operation_has_name_and_description(self):
        for name, op_class in OperationFactory.get_operations().items():
            op = op_class()
            assert op.name == name
            assert isinstance(op.description, str)
            assert len(op.description) > 0