import os
import json
import pytest
from core.state_manager import StateManager
from unittest.mock import mock_open, patch

@pytest.fixture
def sample_state():
    return {"key1": "value1", "key2": 2, "nested": {"a": 1}}

def test_initialization_and_get_set(sample_state):
    sm = StateManager(initial_state=sample_state)
    # Initial state deep copy equality
    assert sm.get_state() == sample_state
    # Get existing key
    assert sm.get("key1") == "value1"
    # Get non-existing key returns None or default
    assert sm.get("nonexistent") is None
    assert sm.get("nonexistent", default=42) == 42

    # Set updates state
    sm.set("key3", 3)
    assert sm.get("key3") == 3

def test_update_merges_state(sample_state):
    sm = StateManager(initial_state=sample_state)
    sm.update({"key2": 20, "key4": "new"})
    updated = sm.get_state()
    assert updated["key2"] == 20
    assert updated["key4"] == "new"

    # Passing non-dict raises TypeError
    with pytest.raises(TypeError):
        sm.update("not a dict")

def test_save_to_file_and_load_from_file(tmp_path, sample_state):
    sm = StateManager(initial_state=sample_state)
    file_path = tmp_path / "state.json"

    # Save state to file
    sm.save_to_file(str(file_path))
    assert file_path.exists()

    # Load state back
    sm2 = StateManager()
    sm2.load_from_file(str(file_path))
    assert sm2.get_state() == sample_state

def test_load_from_file_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text("not a json", encoding="utf-8")

    sm = StateManager()
    with pytest.raises(json.JSONDecodeError):
        sm.load_from_file(str(file_path))

def test_load_from_file_non_dict_json(tmp_path):
    file_path = tmp_path / "list.json"
    file_path.write_text(json.dumps([1, 2, 3]), encoding="utf-8")

    sm = StateManager()
    with pytest.raises(ValueError):
        sm.load_from_file(str(file_path))

def test_save_to_file_ioerror():
    sm = StateManager({"k": "v"})
    with patch("builtins.open", mock_open()) as mocked_open:
        mocked_open.side_effect = IOError("disk full")
        with pytest.raises(IOError):
            sm.save_to_file("/fake/path/state.json")

def test_clear_method(sample_state):
    sm = StateManager(initial_state=sample_state)
    sm.clear()
    assert sm.get_state() == {}
