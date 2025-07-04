import os
import pytest
from daemon import evoai_initializer_security


def test_load_secure_key_success(monkeypatch):
    monkeypatch.setenv("EVOAI_DAEMON_KEY", "A591243133418571088300454z")
    key = evoai_initializer_security.load_secure_key()
    assert key == "A591243133418571088300454z"


def test_load_secure_key_missing(monkeypatch):
    monkeypatch.delenv("EVOAI_DAEMON_KEY", raising=False)
    with pytest.raises(EnvironmentError, match="no configurada"):
        evoai_initializer_security.load_secure_key()


def test_load_secure_key_too_short(monkeypatch):
    monkeypatch.setenv("EVOAI_DAEMON_KEY", "short-key")
    with pytest.raises(ValueError, match="demasiado corta"):
        evoai_initializer_security.load_secure_key()
