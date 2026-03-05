import pytest
import os
from unittest.mock import MagicMock
from app.observers import LoggingObserver, AutoSaveObserver
from app.calculation import Calculation
from app.operations import OperationFactory
from app.calculator_config import CalculatorConfig
from app.history import History


@pytest.fixture
def config():
    return CalculatorConfig.load()


@pytest.fixture
def calc():
    return Calculation(OperationFactory.create("add"), 3, 5)


@pytest.fixture
def history_with_calc(calc):
    h = History()
    h.add(calc)
    return h


class TestLoggingObserver:
    def test_update_calls_logger_info(self, calc):
        mock_logger = MagicMock()
        observer = LoggingObserver(mock_logger)
        observer.update(calc)
        mock_logger.info.assert_called_once()

    def test_log_message_contains_operation_name(self, calc):
        mock_logger = MagicMock()
        LoggingObserver(mock_logger).update(calc)
        call_args = str(mock_logger.info.call_args)
        assert "add" in call_args

    def test_log_message_contains_result(self, calc):
        mock_logger = MagicMock()
        LoggingObserver(mock_logger).update(calc)
        call_args = str(mock_logger.info.call_args)
        assert "8" in call_args

    def test_log_message_contains_operands(self, calc):
        mock_logger = MagicMock()
        LoggingObserver(mock_logger).update(calc)
        call_args = str(mock_logger.info.call_args)
        assert "3" in call_args
        assert "5" in call_args

    def test_different_operations_are_logged(self):
        mock_logger = MagicMock()
        observer = LoggingObserver(mock_logger)
        multiply_calc = Calculation(OperationFactory.create("multiply"), 4, 5)
        observer.update(multiply_calc)
        call_args = str(mock_logger.info.call_args)
        assert "multiply" in call_args


class TestAutoSaveObserver:
    def test_update_creates_csv_file(self, config, history_with_calc, calc):
        observer = AutoSaveObserver(config, history_with_calc)
        observer.update(calc)
        assert os.path.exists(config.history_file)

    def test_csv_contains_correct_columns(self, config, history_with_calc, calc):
        import pandas as pd
        AutoSaveObserver(config, history_with_calc).update(calc)
        df = pd.read_csv(config.history_file)
        assert "operation" in df.columns
        assert "result" in df.columns
        assert "a" in df.columns
        assert "b" in df.columns

    def test_csv_contains_correct_data(self, config, history_with_calc, calc):
        import pandas as pd
        AutoSaveObserver(config, history_with_calc).update(calc)
        df = pd.read_csv(config.history_file)
        assert df.iloc[0]["operation"] == "add"
        assert df.iloc[0]["result"] == 8

    def test_auto_save_false_skips_write(self, config, history_with_calc, calc):
        config.auto_save = False
        observer = AutoSaveObserver(config, history_with_calc)
        observer.update(calc)

    def test_multiple_entries_all_saved(self, config, calc):
        import pandas as pd
        h = History()
        h.add(calc)
        h.add(Calculation(OperationFactory.create("multiply"), 4, 5))
        observer = AutoSaveObserver(config, h)
        observer.update(calc)
        df = pd.read_csv(config.history_file)
        assert len(df) == 2

    def test_observer_called_multiple_times_overwrites(self, config, history_with_calc, calc):
        import pandas as pd
        observer = AutoSaveObserver(config, history_with_calc)
        observer.update(calc)
        observer.update(calc)
        df = pd.read_csv(config.history_file)
        assert len(df) == 1