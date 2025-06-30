import pytest
from core.memory import AgentMemory

class TestAgentMemory:

    def setup_method(self):
        self.memory = AgentMemory()

    def test_initial_state(self):
        assert len(self.memory) == 0
        assert repr(self.memory) == "<AgentMemory: 0 items>"

    def test_store_and_recall(self):
        self.memory.store("test_data")
        assert len(self.memory) == 1
        recalled = self.memory.recall()
        assert recalled == "test_data"

    def test_store_none_is_ignored(self, caplog):
        with caplog.at_level("WARNING"):
            self.memory.store(None)
        assert len(self.memory) == 0
        assert "Attempted to store None data" in caplog.text

    def test_recall_with_invalid_index_returns_none(self, caplog):
        with caplog.at_level("WARNING"):
            result = self.memory.recall(10)  # Out of range
        assert result is None
        assert "Recall failed: index 10 out of range" in caplog.text

    def test_recall_with_valid_index(self):
        self.memory.store("a")
        self.memory.store("b")
        assert self.memory.recall(0) == "a"
        assert self.memory.recall(1) == "b"

    def test_clear_memory(self, caplog):
        self.memory.store("data")
        assert len(self.memory) == 1
        with caplog.at_level("INFO"):
            self.memory.clear()
        assert len(self.memory) == 0
        assert "AgentMemory cleared all stored data" in caplog.text

    def test_repr_and_len_consistency(self):
        self.memory.store(123)
        assert len(self.memory) == 1
        assert repr(self.memory) == "<AgentMemory: 1 items>"
