# tests/test_evoai_initializer_core.py
import pytest
from unittest.mock import patch, MagicMock

from daemon import evoai_initializer_core


@patch("daemon.evoai_initializer_core.load_secure_key")
@patch("daemon.evoai_initializer_core.initialize_agent")
@patch("daemon.evoai_initializer_core.initialize_engine")
@patch("daemon.evoai_initializer_core.initialize_executor")
@patch("daemon.evoai_initializer_core.initialize_support_tools")
@patch("daemon.evoai_initializer_core.EvoContext")
def test_initialize_core_components_success(
    mock_context_cls,
    mock_initialize_support_tools,
    mock_initialize_executor,
    mock_initialize_engine,
    mock_initialize_agent,
    mock_load_secure_key,
):
    # Preparar mocks
    mock_context = MagicMock(name="EvoContext")
    mock_agent = MagicMock(name="Agent")
    mock_engine = MagicMock(name="Engine")
    mock_executor = MagicMock(name="Executor")
    mock_tools = {
        "monitor": MagicMock(),
        "code_analyzer": MagicMock(),
        "analyzer": MagicMock(),
        "consciousness": MagicMock(),
        "network": MagicMock(),
        "codex": MagicMock(),
        "decision_engine": mock_engine,
    }

    mock_context_cls.return_value = mock_context
    mock_load_secure_key.return_value = "secure_key_ABC123456789012345"
    mock_initialize_agent.return_value = mock_agent
    mock_initialize_engine.return_value = mock_engine
    mock_initialize_executor.return_value = mock_executor
    mock_initialize_support_tools.return_value = mock_tools

    result = evoai_initializer_core.initialize_core_components()

    # Validaciones
    assert result["context"] == mock_context
    assert result["agent"] == mock_agent
    assert result["engine"] == mock_engine
    assert result["executor"] == mock_executor
    for key in mock_tools:
        assert key in result
        assert result[key] == mock_tools[key]
