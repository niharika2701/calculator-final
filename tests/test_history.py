import pytest
from app.history import History
from app.operations import OperationFactory
from app.calculation import Calculation
from app.exceptions import HistoryError

@pytest.fixture
def history():
    return History(max_size=5)

@pytest.fixture
def calc():
    return Calculation(OperationFactory.create("add"), 3, 5)

class TestHistory:
    def test_starts_empty(self, history):
        assert history.entries == []
        assert len(history) == 0

    def test_add_entry(self, history, calc):
        history.add(calc)
        assert len(history) == 1
        assert history.entries[0] is calc

    def test_max_size_enforced(self):
        h = History(max_size=3)
        for i in range(5):
            h.add(Calculation(OperationFactory.create("add"), i, i))
        assert len(h) == 3

    def test_clear(self, history, calc):
        history.add(calc)
        history.clear()
        assert len(history) == 0

    def test_undo_removes_last(self, history, calc):
        history.add(calc)
        history.undo()
        assert len(history) == 0

    def test_undo_empty_raises(self, history):
        with pytest.raises(HistoryError, match="Nothing to undo"):
            history.undo()

    def test_redo_after_undo(self, history, calc):
        history.add(calc)
        history.undo()
        history.redo()
        assert len(history) == 1

    def test_redo_without_undo_raises(self, history):
        with pytest.raises(HistoryError, match="Nothing to redo"):
            history.redo()

    def test_new_add_clears_redo_stack(self, history, calc):
        history.add(calc)
        history.undo()
        history.add(calc)
        with pytest.raises(HistoryError, match="Nothing to redo"):
            history.redo()

    def test_get_last(self, history, calc):
        history.add(calc)
        assert history.get_last() is calc

    def test_get_last_empty_raises(self, history):
        with pytest.raises(HistoryError, match="No calculations"):
            history.get_last()