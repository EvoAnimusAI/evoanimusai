# tests/test_evoai_initializer_engine.py
import pytest
import logging
from daemon.evoai_initializer_engine import initialize_engine

def test_initialize_engine_success(monkeypatch, caplog):
    class DummyEngine:
        def __init__(self):
            self.name = "MockEngine"

    monkeypatch.setattr("daemon.evoai_initializer_engine.EvoAIEngine", DummyEngine)

    caplog.set_level(logging.INFO)
    engine = initialize_engine()

    assert isinstance(engine, DummyEngine)
    assert "Motor inicializado correctamente." in caplog.text
    assert engine.name == "MockEngine"


def test_initialize_engine_failure(monkeypatch, caplog):
    def fail_engine():
        raise RuntimeError("Simulated Engine Error")

    monkeypatch.setattr("daemon.evoai_initializer_engine.EvoAIEngine", fail_engine)

    caplog.set_level(logging.ERROR)
    with pytest.raises(RuntimeError, match="Simulated Engine Error"):
        initialize_engine()

    assert "Error durante inicialización del motor" in caplog.text
