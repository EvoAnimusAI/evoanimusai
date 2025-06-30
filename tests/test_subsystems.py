# tests/test_evoai_subsystems.py
import pytest
from unittest.mock import patch, MagicMock
from daemon.evoai_subsystems import EvoAISubsystems


@pytest.fixture
def mock_engine():
    return MagicMock(name="MockEngine")


@pytest.fixture
def mock_context():
    return MagicMock(name="MockContext")


@patch("daemon.evoai_subsystems.EvoAIAnalyzerDaemon")
@patch("daemon.evoai_subsystems.EvoCodex")
@patch("daemon.evoai_subsystems.NetworkAccess")
@patch("daemon.evoai_subsystems.Autoconsciousness")
@patch("daemon.evoai_subsystems.CodeAnalyzer")
@patch("daemon.evoai_subsystems.EvoAIMonitor")
def test_evoai_subsystems_initialization(
    mock_monitor,
    mock_code_analyzer,
    mock_consciousness,
    mock_network,
    mock_codex,
    mock_analyzer_daemon,
    mock_engine,
    mock_context
):
    subsystems = EvoAISubsystems(engine=mock_engine, context=mock_context)

    mock_monitor.assert_called_once()
    mock_code_analyzer.assert_called_once_with(root_path=".")
    mock_consciousness.assert_called_once_with(
        identity="Daniel Santiago Ospina Velasquez",
        agent_id="AV255583"
    )
    mock_network.assert_called_once()
    mock_codex.assert_called_once_with(root_path=".")
    mock_analyzer_daemon.assert_called_once_with(
        engine=mock_engine,
        log_file="logs/logs_evoai.json",
        interval=20
    )


@patch("daemon.evoai_subsystems.Autoconsciousness")
def test_evoai_subsystems_activate_calls_declare_existence(mock_consciousness_class):
    mock_consciousness_instance = MagicMock()
    mock_consciousness_class.return_value = mock_consciousness_instance

    subsystems = EvoAISubsystems(engine=MagicMock(), context=MagicMock())
    subsystems.activate()

    mock_consciousness_instance.declare_existence.assert_called_once()
