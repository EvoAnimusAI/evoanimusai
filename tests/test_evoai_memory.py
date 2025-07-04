import os
import json
from pathlib import Path
from daemon import evoai_memory


def test_ensure_memory_file_creates_file(tmp_path):
    file_path = tmp_path / "test_memory.json"
    evoai_memory.ensure_memory_file(str(file_path))
    assert file_path.exists()
    with file_path.open("r", encoding="utf-8") as f:
        assert json.load(f) == []


def test_load_symbolic_memory_returns_empty_if_not_exists(monkeypatch, tmp_path):
    monkeypatch.setattr(evoai_memory, "SYMBOLIC_MEMORY_FILE", str(tmp_path / "nonexistent.json"))
    data = evoai_memory.load_symbolic_memory()
    assert data == []


def test_append_to_symbolic_memory_creates_and_appends(monkeypatch, tmp_path):
    test_file = tmp_path / "symbolic.json"
    monkeypatch.setattr(evoai_memory, "SYMBOLIC_MEMORY_FILE", str(test_file))

    entry = {"origin": "test_case", "value": 42}
    evoai_memory.append_to_symbolic_memory(entry)

    with test_file.open("r", encoding="utf-8") as f:
        content = json.load(f)
    assert content == [entry]


def test_save_and_load_function_memory(monkeypatch, tmp_path):
    func_file = tmp_path / "function.json"
    monkeypatch.setattr(evoai_memory, "FUNCTION_MEMORY_FILE", str(func_file))

    data = {"name": "test_function", "steps": [{"action": "think", "param": 3.0}]}
    evoai_memory.save_function_memory(data)

    loaded = evoai_memory.load_function_memory()
    assert loaded == data


def test_load_function_memory_returns_default_if_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(evoai_memory, "FUNCTION_MEMORY_FILE", str(tmp_path / "missing.json"))
    result = evoai_memory.load_function_memory()
    assert isinstance(result, dict)
    assert "name" in result and "steps" in result
