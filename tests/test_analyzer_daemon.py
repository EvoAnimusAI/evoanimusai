import pytest
from unittest.mock import MagicMock, patch, mock_open
from monitoring.analyzer_daemon import EvoAIAnalyzerDaemon

@pytest.fixture
def mock_engine():
    engine = MagicMock()
    engine.get_recent_events.return_value = [
        {"accion": "explore", "recompensa": 1.0, "regla_aplicada": "⟦mood:curious⟧ ⇒ explore :: True"},
        {"accion": "explore", "recompensa": 0.5, "regla_aplicada": "⟦mood:curious⟧ ⇒ explore :: True"},
        {"accion": "exploit", "recompensa": -1.0, "regla_aplicada": "⟦mood:focused⟧ ⇒ exploit :: True"},
    ]
    return engine

def test_run_cycle_not_triggered(mock_engine):
    daemon = EvoAIAnalyzerDaemon(engine=mock_engine, interval=5)
    daemon.counter = 3
    assert daemon.run_cycle() is None
    assert daemon.counter == 4

def test_run_cycle_empty_events(mock_engine):
    mock_engine.get_recent_events.return_value = []
    daemon = EvoAIAnalyzerDaemon(engine=mock_engine, interval=1)
    result = daemon.run_cycle()
    assert result is None
    assert daemon.counter == 0

def test_run_cycle_analysis_success(mock_engine):
    daemon = EvoAIAnalyzerDaemon(engine=mock_engine, interval=1, log_file="dummy.json")
    with patch("builtins.open", mock_open()) as mocked_file, \
         patch("json.dump") as mock_dump, \
         patch("logging.Logger.info"), \
         patch("logging.Logger.warning"):
        result = daemon.run_cycle()
        assert result is not None
        assert "actions" in result
        assert "rules" in result
        mock_dump.assert_called_once()

def test_analysis_malformed_event(mock_engine):
    mock_engine.get_recent_events.return_value.append({"accion": "unknown", "recompensa": "invalid"})
    daemon = EvoAIAnalyzerDaemon(engine=mock_engine, interval=1, log_file="dummy.json")
    with patch("builtins.open", mock_open()), \
         patch("json.dump"), \
         patch("logging.Logger.warning") as mock_warn:
        result = daemon.run_cycle()
        assert result is not None
        mock_warn.assert_called()
