import pytest
from core.tools import ToolManager


def test_initialize_marks_initialized_and_verbose_logs(caplog):
    manager = ToolManager()
    with caplog.at_level("INFO"):
        manager.initialize(verbose=True)
        assert manager.initialized is True
        assert "[ToolManager] Inicializando herramientas auxiliares..." in caplog.text
        assert "[ToolManager] Inicialización completada con éxito." in caplog.text


def test_initialize_is_idempotent(caplog):
    manager = ToolManager()
    manager.initialize(verbose=True)
    caplog.clear()
    with caplog.at_level("INFO"):
        manager.initialize(verbose=True)
        assert "[ToolManager] Ya fue inicializado. Ignorando segunda inicialización." in caplog.text


def test_get_tool_returns_none_if_not_registered():
    manager = ToolManager()
    assert manager.get_tool("unknown_tool") is None


def test_get_tool_returns_tool_if_registered():
    manager = ToolManager()
    mock_tool = object()
    manager.tools["analyzer"] = mock_tool
    assert manager.get_tool("analyzer") == mock_tool
