import pytest
from unittest.mock import patch, MagicMock

from daemon import evoai_initializer_tools


@pytest.fixture
def mock_engine():
    return MagicMock(name="MockSymbolicEngine")


@pytest.fixture
def mock_context():
    return MagicMock(name="MockContext")


@patch("daemon.evoai_initializer_tools.EvoAIMonitor")
@patch("daemon.evoai_initializer_tools.EvoCodex")
@patch("daemon.evoai_initializer_tools.Autoconsciousness")
@patch("daemon.evoai_initializer_tools.NetworkAccess")
@patch("daemon.evoai_initializer_tools.CodeAnalyzer")
def test_initialize_support_tools_success(
    mock_code_analyzer,
    mock_network,
    mock_consciousness,
    mock_codex,
    mock_monitor,
    mock_engine,
    mock_context
):
    mock_analyzer_instance = MagicMock()
    mock_code_analyzer.return_value = mock_analyzer_instance
    mock_monitor.return_value = MagicMock()
    mock_codex.return_value = MagicMock()
    mock_network.return_value = MagicMock()
    mock_consciousness.return_value = MagicMock()

    tools = evoai_initializer_tools.initialize_support_tools(
        engine=mock_engine,
        context=mock_context,
        daemon_key="SECURE_KEY_123"
    )

    assert isinstance(tools, dict)
    assert "monitor" in tools
    assert "code_analyzer" in tools
    assert "analyzer" in tools
    assert "consciousness" in tools
    assert "network" in tools
    assert "codex" in tools
    assert "decision_engine" in tools

    mock_code_analyzer.assert_called_once_with(root_path=".")
    mock_monitor.assert_called_once()
    mock_consciousness.assert_called_once_with("Daniel Santiago Ospina Velasquez", "AV255583")
    mock_network.assert_called_once_with(master_key="SECURE_KEY_123")
    mock_codex.assert_called_once_with(root_path=".")

    assert tools["decision_engine"] is mock_engine


@patch("daemon.evoai_initializer_tools.CodeAnalyzer", side_effect=Exception("Init failed"))
def test_initialize_support_tools_failure(mock_code_analyzer, mock_engine, mock_context):
    with pytest.raises(Exception) as exc_info:
        evoai_initializer_tools.initialize_support_tools(
            engine=mock_engine,
            context=mock_context,
            daemon_key="FAIL_KEY"
        )
    assert "Init failed" in str(exc_info.value)
