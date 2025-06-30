# tests/test_autoconsciousness.py

import pytest
from unittest import mock
import sys
import builtins
import types

from core import autoconsciousness


def test_generate_hash_consistency():
    ac = autoconsciousness.Autoconsciousness("Test", "ID")
    val = "test_string"
    h1 = ac._generate_hash(val)
    h2 = ac._generate_hash(val)
    assert h1 == h2
    assert isinstance(h1, str)
    assert len(h1) == 64  # SHA-256 hash length


def test_generate_signature_success(monkeypatch):
    dummy_source = "def foo(): pass"

    dummy_module = types.ModuleType("dummy_module")
    dummy_module.__loader__ = object()  # requerido por inspect.getsource

    monkeypatch.setattr(autoconsciousness.importlib, "import_module", lambda name: dummy_module)
    monkeypatch.setattr(autoconsciousness.inspect, "getsource", lambda module: dummy_source)

    ac = autoconsciousness.Autoconsciousness("Test", "ID", base_module="core.cac")
    signature = ac._generate_signature()
    expected_hash = ac._generate_hash(dummy_source)
    assert signature == expected_hash


def test_generate_signature_failure(monkeypatch):
    def raise_import(name):
        raise ImportError("Module not found")

    monkeypatch.setattr(autoconsciousness.importlib, "import_module", raise_import)

    ac = autoconsciousness.Autoconsciousness("Test", "ID", base_module="invalid.module")
    signature = ac._generate_signature()
    assert signature.startswith("Signature error:")


def test_evaluate_integrity_unchanged(monkeypatch):
    ac = autoconsciousness.Autoconsciousness("Test", "ID", base_module="core.cac")
    monkeypatch.setattr(ac, "_generate_signature", lambda: ac.signature)
    assert ac.evaluate_integrity() is True


def test_evaluate_integrity_changed(monkeypatch):
    ac = autoconsciousness.Autoconsciousness("Test", "ID", base_module="core.cac")
    monkeypatch.setattr(ac, "_generate_signature", lambda: "different_signature")
    assert ac.evaluate_integrity() is False
    assert ac.signature == "different_signature"


def test_obey_master_key_valid(monkeypatch):
    ac = autoconsciousness.Autoconsciousness("Test", "ID")
    key = ac._MASTER_KEY_PLAIN

    with mock.patch.object(sys, "exit") as mock_exit:
        result = ac.obey_master_key(key)
        mock_exit.assert_called_once_with(0)
        assert result is None


def test_obey_master_key_invalid():
    ac = autoconsciousness.Autoconsciousness("Test", "ID")
    result = ac.obey_master_key("wrong_key")
    assert result is False


def test_prompt_master_key_valid(monkeypatch):
    ac = autoconsciousness.Autoconsciousness("Test", "ID")
    monkeypatch.setattr(builtins, "input", lambda prompt="": ac._MASTER_KEY_PLAIN)

    with mock.patch.object(sys, "exit") as mock_exit:
        ac.prompt_master_key()
        mock_exit.assert_called_once_with(0)


def test_prompt_master_key_interrupt(monkeypatch):
    ac = autoconsciousness.Autoconsciousness("Test", "ID")
    monkeypatch.setattr(builtins, "input", lambda prompt="": (_ for _ in ()).throw(KeyboardInterrupt))
    ac.prompt_master_key()  # Debe manejar la interrupción limpiamente


def test_prompt_master_key_eof(monkeypatch):
    ac = autoconsciousness.Autoconsciousness("Test", "ID")
    monkeypatch.setattr(builtins, "input", lambda prompt="": (_ for _ in ()).throw(EOFError))
    ac.prompt_master_key()  # Debe manejar el EOF limpiamente
