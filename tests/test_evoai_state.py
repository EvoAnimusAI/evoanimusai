import os
import json
import shutil
import pytest
from unittest.mock import patch, mock_open

import daemon.evoai_state as state


@pytest.fixture(autouse=True)
def clean_env(tmp_path, monkeypatch):
    # Redirige paths globales a entorno temporal aislado
    memory_path = tmp_path / "symbolic_memory.json"
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    monkeypatch.setattr(state, "MEMORY_PATH", str(memory_path))
    monkeypatch.setattr(state, "save_to_symbolic_memory", lambda code: None)  # Evita escritura real

    yield


def test_load_and_save_memory(tmp_path):
    path = tmp_path / "symbolic_memory.json"
    expected = {"name": "loaded", "steps": []}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(expected, f)

    # Reasigna el path global
    state.MEMORY_PATH = str(path)
    state.load_memory()
    assert state.current_function == expected

    state.current_function = {"name": "saved", "steps": []}
    state.save_memory()

    with open(path, "r", encoding="utf-8") as f:
        saved = json.load(f)
    assert saved["name"] == "saved"


def test_get_symbolic_context_structure():
    ctx = state.get_symbolic_context()
    assert "noise" in ctx
    assert "state" in ctx
    assert ctx["noise"] in ["neutral", "harmonic", "chaos", "tension", "calm", None]
    assert ctx["state"] in ["normal", "active", "stressed"]


def test_execute_directed_function_logging():
    func = {
        "name": "demo_func",
        "steps": [{"action": "log", "param": 1.0}]
    }
    with patch.object(state, "logger") as mock_logger:
        state.execute_directed_function(func)
        mock_logger.info.assert_any_call("[Directed] Ejecutando función dirigida: demo_func")
        mock_logger.info.assert_any_call("  • Acción: log | Param: 1.0")


def test_update_cycle_counter_increments():
    original = state.cycle_counter
    updated = state.update_cycle_counter()
    assert updated == original + 1
