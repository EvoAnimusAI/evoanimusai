import os
import pytest
from unittest.mock import MagicMock, patch
from core.self_diagnostics import SelfDiagnostics, run_integrity_diagnostics

class DummyContext:
    def __init__(self, state):
        self.state = state

@pytest.fixture
def valid_components(tmp_path):
    # Configuración de rutas temporales válidas simuladas
    with patch("core.self_diagnostics.Config.get_instance") as mock_config:
        mock_config.return_value.symbolic_memory_path = tmp_path / "memory"
        mock_config.return_value.mutated_functions_path = tmp_path / "mutated"
        mock_config.return_value.logs_path = tmp_path / "logs"

        # Crear las carpetas para evitar fallo de existencia
        os.makedirs(str(tmp_path / "memory"))
        os.makedirs(str(tmp_path / "mutated"))
        os.makedirs(str(tmp_path / "logs"))

        yield {
            "context": DummyContext(state={"key": "value"}),
            "agent": MagicMock(),
            "engine": MagicMock(),
            "decision": MagicMock(),
            "executor": MagicMock(),
        }

def test_run_preflight_check_success(valid_components):
    diag = SelfDiagnostics(components=valid_components)
    result = diag.run_preflight_check(daemon_key="validkeywithmore12")
    assert result is True

def test_run_preflight_check_missing_component(valid_components):
    components = valid_components.copy()
    del components["engine"]
    diag = SelfDiagnostics(components=components)
    result = diag.run_preflight_check(daemon_key="validkeywithmore12")
    assert result is False

def test_run_preflight_check_none_component(valid_components):
    components = valid_components.copy()
    components["agent"] = None
    diag = SelfDiagnostics(components=components)
    result = diag.run_preflight_check(daemon_key="validkeywithmore12")
    assert result is False

def test_run_preflight_check_invalid_context_state(valid_components):
    components = valid_components.copy()
    components["context"] = DummyContext(state=None)
    diag = SelfDiagnostics(components=components)
    result = diag.run_preflight_check(daemon_key="validkeywithmore12")
    assert result is False

def test_run_preflight_check_invalid_daemon_key(valid_components):
    diag = SelfDiagnostics(components=valid_components)
    result = diag.run_preflight_check(daemon_key="short")
    assert result is False

def test_run_preflight_check_missing_critical_paths(valid_components):
    # Patch os.path.exists para simular ruta no encontrada
    with patch("os.path.exists", return_value=False):
        diag = SelfDiagnostics(components=valid_components)
        result = diag.run_preflight_check(daemon_key="validkeywithmore12")
        assert result is False

def test_run_preflight_check_exception_handling(valid_components):
    with patch("core.self_diagnostics.Config.get_instance", side_effect=Exception("fail")):
        diag = SelfDiagnostics(components=valid_components)
        result = diag.run_preflight_check(daemon_key="validkeywithmore12")
        assert result is False

def test_run_integrity_diagnostics_success():
    ctx = DummyContext(state={"a": 1})
    assert run_integrity_diagnostics(ctx) is True

def test_run_integrity_diagnostics_none_context():
    assert run_integrity_diagnostics(None) is False

def test_run_integrity_diagnostics_invalid_state():
    ctx = DummyContext(state=None)
    assert run_integrity_diagnostics(ctx) is False

def test_run_integrity_diagnostics_exception():
    class BadContext:
        @property
        def state(self):
            raise Exception("error")

    ctx = BadContext()
    assert run_integrity_diagnostics(ctx) is False

