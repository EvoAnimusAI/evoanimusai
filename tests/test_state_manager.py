import json
import os
import pytest
from core.state_manager import StateManager

def test_initial_state_empty():
    sm = StateManager()
    assert sm.get_state() == {}
    assert sm.status() == {"keys_count": 0, "has_data": False}

def test_set_and_get_value():
    sm = StateManager()
    sm.set("alpha", 42)
    assert sm.get("alpha") == 42
    # get_state devuelve copia (inmutabilidad externa)
    state_copy = sm.get_state()
    state_copy["alpha"] = 99
    assert sm.get("alpha") == 42  # original intacto

def test_update_with_valid_dict():
    sm = StateManager()
    sm.update({"a": 1, "b": 2})
    assert sm.get("a") == 1 and sm.get("b") == 2
    assert sm.status() == {"keys_count": 2, "has_data": True}

def test_update_with_invalid_type_raises():
    sm = StateManager()
    with pytest.raises(TypeError):
        sm.update(["not", "a", "dict"])

def test_save_and_load_state(tmp_path):
    sm = StateManager({"x": 10})
    file_path = tmp_path / "state.json"
    sm.save_to_file(str(file_path))
    # Asegurar que el archivo existe y contiene datos correctos
    assert file_path.exists()
    loaded_json = json.loads(file_path.read_text())
    assert loaded_json == {"x": 10}
    # Ahora limpiar y recargar
    sm.clear()
    assert sm.get_state() == {}
    sm.load_from_file(str(file_path))
    assert sm.get("x") == 10

def test_load_invalid_json_raises(tmp_path):
    file_path = tmp_path / "bad.json"
    file_path.write_text("{invalid json")
    sm = StateManager()
    with pytest.raises(Exception):
        sm.load_from_file(str(file_path))

def test_clear_resets_state():
    sm = StateManager({"k": "v"})
    sm.clear()
    assert sm.get_state() == {}
    assert sm.status() == {"keys_count": 0, "has_data": False}
