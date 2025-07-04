import pytest
from unittest.mock import patch, MagicMock
from daemon.evoai_subsystems import EvoAISubsystems


@pytest.fixture
def mock_dependencies():
    with patch("daemon.evoai_subsystems.EvoAIMonitor") as mock_monitor, \
         patch("daemon.evoai_subsystems.CodeAnalyzer") as mock_analyzer, \
         patch("daemon.evoai_subsystems.Autoconsciousness") as mock_conscious, \
         patch("daemon.evoai_subsystems.NetworkAccess") as mock_net, \
         patch("daemon.evoai_subsystems.EvoCodex") as mock_codex, \
         patch("daemon.evoai_subsystems.EvoAIAnalyzerDaemon") as mock_daemon:
        yield {
            "monitor": mock_monitor,
            "analyzer": mock_analyzer,
            "conscious": mock_conscious,
            "net": mock_net,
            "codex": mock_codex,
            "daemon": mock_daemon,
        }


def test_subsystem_initialization(mock_dependencies):
    engine = MagicMock()
    context = MagicMock()

    subsystems = EvoAISubsystems(engine, context)

    assert hasattr(subsystems, "monitor")
    assert hasattr(subsystems, "code_analyzer")
    assert hasattr(subsystems, "consciousness")
    assert hasattr(subsystems, "network")
    assert hasattr(subsystems, "codex")
    assert hasattr(subsystems, "analyzer_daemon")

    mock_dependencies["monitor"].assert_called_once()
    mock_dependencies["analyzer"].assert_called_once_with(root_path=".")
    mock_dependencies["conscious"].assert_called_once_with(
        identity="Daniel Santiago Ospina Velasquez",
        agent_id="AV255583"
    )
    mock_dependencies["net"].assert_called_once()
    mock_dependencies["codex"].assert_called_once_with(root_path=".")
    mock_dependencies["daemon"].assert_called_once_with(
        engine=engine,
        log_file="logs/logs_evoai.json",
        interval=20
    )


def test_activate_declares_existence(mock_dependencies):
    engine = MagicMock()
    context = MagicMock()

    subsystems = EvoAISubsystems(engine, context)
    subsystems.consciousness = MagicMock()

    subsystems.activate()

    subsystems.consciousness.declare_existence.assert_called_once()
