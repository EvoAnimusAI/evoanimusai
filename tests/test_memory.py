import logging
import pytest
from core.memory import AgentMemory

def test_memory_initialization():
    mem = AgentMemory()
    assert len(mem) == 0
    assert mem.summary() == {"items": 0}

def test_store_and_recall():
    mem = AgentMemory()
    mem.store("data1")
    mem.store({"key": "value"})
    assert len(mem) == 2
    assert mem.recall() == {"key": "value"}
    assert mem.recall(0) == "data1"

def test_recall_invalid_index(caplog):
    mem = AgentMemory()
    mem.store("data")
    with caplog.at_level(logging.WARNING):
        result = mem.recall(5)
    assert result is None
    warnings = [rec for rec in caplog.records if rec.levelname == "WARNING"]
    assert any("index 5 out of range" in w.message for w in warnings)

def test_store_none_ignored(caplog):
    mem = AgentMemory()
    with caplog.at_level(logging.WARNING):
        mem.store(None)
    assert len(mem) == 0
    warnings = [rec for rec in caplog.records if rec.levelname == "WARNING"]
    assert any("Attempted to store None data" in w.message for w in warnings)

def test_clear_memory():
    mem = AgentMemory()
    mem.store("data")
    mem.clear()
    assert len(mem) == 0
    assert mem.summary() == {"items": 0}

def test_repr_contains_item_count():
    mem = AgentMemory()
    mem.store("data")
    repr_str = repr(mem)
    assert "1 items" in repr_str or "1 item" in repr_str

