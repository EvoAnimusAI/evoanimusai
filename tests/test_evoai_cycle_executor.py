import pytest
from unittest.mock import MagicMock, patch
from daemon import evoai_cycle_executor as executor


def test_initialize_context():
    with patch("daemon.evoai_cycle_executor.EvoAgent") as mock_agent_class, \
         patch("daemon.evoai_cycle_executor.Environment") as mock_env_class, \
         patch("daemon.evoai_cycle_executor.EvoAIEngine") as mock_engine_class, \
         patch("daemon.evoai_cycle_executor.EvoContext") as mock_context_class:

        mock_agent = MagicMock(name="EvoAgent")
        mock_env = MagicMock()
        mock_engine = MagicMock()
        mock_context = MagicMock()

        mock_agent_class.return_value = mock_agent
        mock_env_class.return_value = mock_env
        mock_engine_class.return_value = mock_engine
        mock_context_class.return_value = mock_context

        mock_context.assert_fact = MagicMock()

        context = executor.initialize_context()
        mock_context.assert_fact.assert_called_with("agent_identity", mock_agent.name)
        assert context is mock_context


def test_run_cycle_nominal_flow():
    mock_context = MagicMock()
    mock_context.decide.return_value = ({"action": "run"}, {"action": "run", "priority": 0.5})
    mock_context.environment.observe.return_value = {"input": "raw"}
    mock_context.as_dict.return_value = {"state": "ok"}

    mock_sanitizer = MagicMock()
    mock_sanitizer.sanitize.return_value = {"input": "clean"}

    result = executor.run_cycle(mock_context, 3, mock_sanitizer)

    mock_context.symbolic_engine = None  # just to be sure it doesn't interfere
    mock_context.decide.assert_called_once()
    mock_sanitizer.sanitize.assert_called_once()
    mock_context.update.assert_called_with({"input": "clean"})
    assert "state" in result


def test_run_cycle_with_priority_adjustment():
    mock_context = MagicMock()
    mock_context.decide.return_value = (None, {"action": "explore", "priority": 1.0})
    mock_context.environment.observe.return_value = {"foo": "bar"}
    mock_context.as_dict.return_value = {"result": "ok"}

    mock_sanitizer = MagicMock()
    mock_sanitizer.sanitize.return_value = {"foo": "bar"}

    result = executor.run_cycle(mock_context, 5, mock_sanitizer)

    assert result.get("result") == "ok"
    assert mock_context.update.called


def test_run_cycle_handles_exception_gracefully():
    mock_context = MagicMock()
    mock_context.decide.side_effect = RuntimeError("fail here")

    mock_sanitizer = MagicMock()

    result = executor.run_cycle(mock_context, 1, mock_sanitizer)
    assert result["error"] == "fail here"
    assert result["cycle"] == 1


def test_setup_signal_handlers(monkeypatch):
    handled_signals = {}

    def fake_signal(sig, handler):
        handled_signals[sig] = handler

    monkeypatch.setattr("signal.signal", fake_signal)
    executor.setup_signal_handlers()

    assert len(handled_signals) == 4
