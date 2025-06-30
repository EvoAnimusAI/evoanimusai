# tests/test_evoai_mutation_handler.py
# -*- coding: utf-8 -*-
"""
Pruebas unitarias para evoai_mutation_handler.py
Estándares gubernamentales de confiabilidad y cobertura total.
"""

import json
import pytest
from unittest.mock import patch, mock_open, MagicMock
import daemon.evoai_mutation_handler as handler


# --- Test: Mutación dirigida aceptada ---
def test_perform_directed_mutation_accepts(monkeypatch):
    current_function = {"name": "test_func", "code": "print('original')"}

    monkeypatch.setattr("daemon.evoai_mutation_handler.get_symbolic_context", lambda: {"state": "active"})
    monkeypatch.setattr("daemon.evoai_mutation_handler.mutate_parent_function", lambda f, c, p: {"code": "new"})
    monkeypatch.setattr("daemon.evoai_mutation_handler.evaluate_mutation", lambda f, c: True)

    m_open = mock_open(read_data="[]")
    with patch("daemon.evoai_mutation_handler.open", m_open, create=True):
        handler.perform_directed_mutation(current_function, ["ai"], context={})
        assert m_open.call_count >= 1


# --- Test: Mutación dirigida rechazada ---
def test_perform_directed_mutation_rejects(monkeypatch):
    current_function = {"name": "test_func", "code": "print('original')"}

    monkeypatch.setattr("daemon.evoai_mutation_handler.get_symbolic_context", lambda: {"state": "active"})
    monkeypatch.setattr("daemon.evoai_mutation_handler.mutate_parent_function", lambda f, c, p: {"code": "new"})
    monkeypatch.setattr("daemon.evoai_mutation_handler.evaluate_mutation", lambda f, c: False)

    with patch("daemon.evoai_mutation_handler.open", mock_open(), create=True) as m:
        handler.perform_directed_mutation(current_function, ["ai"], context={})
        # No escritura si la mutación fue rechazada
        m.assert_not_called()


# --- Test: Mutación simbólica aceptada ---
def test_perform_symbolic_mutation_accepts(monkeypatch):
    filename = "mutation_test.py"
    code = "print('mutated')"

    monkeypatch.setattr("daemon.evoai_mutation_handler.generate_and_save_mutation", lambda: filename)
    monkeypatch.setattr("daemon.evoai_mutation_handler.evaluate_mutation", lambda c, ctx: True)
    monkeypatch.setattr("daemon.evoai_mutation_handler.os.path.exists", lambda x: True)

    m_open = mock_open(read_data="[]")
    with patch("daemon.evoai_mutation_handler.open", m_open, create=True):
        with patch("builtins.open", mock_open(read_data=code)):
            handler.perform_symbolic_mutation(10, 5, context={})
            assert m_open.call_count >= 1


# --- Test: Mutación simbólica rechazada (no guarda) ---
def test_perform_symbolic_mutation_skips(monkeypatch):
    filename = "mutation_test.py"
    code = "print('mutated')"

    monkeypatch.setattr("daemon.evoai_mutation_handler.generate_and_save_mutation", lambda: filename)
    monkeypatch.setattr("daemon.evoai_mutation_handler.evaluate_mutation", lambda c, ctx: False)
    monkeypatch.setattr("daemon.evoai_mutation_handler.os.path.exists", lambda x: True)

    with patch("daemon.evoai_mutation_handler.open", mock_open(read_data=code), create=True) as m:
        handler.perform_symbolic_mutation(10, 5, context={})
        # open solo para lectura; no escritura
        assert m.call_count == 1


# --- Test: Mutación sobre memoria interna del agente ---
def test_perform_internal_memory_mutation(monkeypatch):
    agent = MagicMock()
    agent.memory.retrieve_all.return_value = "internal_state"
    engine = MagicMock()

    monkeypatch.setattr("daemon.evoai_mutation_handler.mutate_function", lambda m, c: "mutated_code")

    handler.perform_internal_memory_mutation(agent, context={}, engine=engine)
    assert engine.last_mutated_function == "mutated_code"


# --- Test: Guardado de código en memoria simbólica ---
def test_save_to_symbolic_memory(monkeypatch):
    code = "print('mutated')"

    m_open = mock_open(read_data="[]")
    monkeypatch.setattr("daemon.evoai_mutation_handler.os.path.exists", lambda x: True)

    with patch("daemon.evoai_mutation_handler.open", m_open, create=True):
        handler.save_to_symbolic_memory(code)
        handle = m_open()
        handle.write.assert_called()
