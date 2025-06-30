# tests/test_evoai_initializer_security.py
# -*- coding: utf-8 -*-
"""
Pruebas unitarias para evoai_initializer_security.py.
Cobertura completa de seguridad en lectura de claves desde entorno seguro.
"""

import os
import pytest
from daemon.evoai_initializer_security import load_secure_key

def test_load_secure_key_success(monkeypatch):
    valid_key = "A_SUPER_SECURE_DAEMON_KEY_12345"
    monkeypatch.setenv("EVOAI_DAEMON_KEY", valid_key)

    result = load_secure_key()
    assert result == valid_key


def test_load_secure_key_missing(monkeypatch):
    monkeypatch.delenv("EVOAI_DAEMON_KEY", raising=False)

    with pytest.raises(EnvironmentError) as exc_info:
        load_secure_key()
    assert "no configurada" in str(exc_info.value)


def test_load_secure_key_too_short(monkeypatch):
    monkeypatch.setenv("EVOAI_DAEMON_KEY", "short-key")

    with pytest.raises(ValueError) as exc_info:
        load_secure_key()
    assert "demasiado corta" in str(exc_info.value)
