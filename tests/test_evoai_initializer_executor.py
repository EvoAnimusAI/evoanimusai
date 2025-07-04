import pytest
from unittest.mock import MagicMock, patch
from daemon import evoai_initializer_executor


def test_initialize_executor_success():
    mock_agent = MagicMock()
    mock_engine = MagicMock()
    mock_context = MagicMock()

    with patch("daemon.evoai_initializer_executor.EvoAIMonitor") as mock_monitor_class, \
         patch("daemon.evoai_initializer_executor.EvoAIExecutor") as mock_executor_class:

        mock_monitor = MagicMock()
        mock_executor = MagicMock()
        mock_monitor_class.return_value = mock_monitor
        mock_executor_class.return_value = mock_executor

        executor = evoai_initializer_executor.initialize_executor(mock_agent, mock_engine, mock_context)

        mock_monitor_class.assert_called_once()
        mock_executor_class.assert_called_once_with(
            agent=mock_agent, engine=mock_engine, monitor=mock_monitor, context=mock_context
        )
        assert executor is mock_executor


@pytest.mark.parametrize("agent,engine,context,expected_error", [
    (None, MagicMock(), MagicMock(), "agente.*obligatorio"),
    (MagicMock(), None, MagicMock(), "motor.*obligatorio"),
    (MagicMock(), MagicMock(), None, "contexto.*obligatorio"),
])
def test_initialize_executor_missing_parameters(agent, engine, context, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        evoai_initializer_executor.initialize_executor(agent, engine, context)


def test_initialize_executor_failure_on_internal_error():
    mock_agent = MagicMock()
    mock_engine = MagicMock()
    mock_context = MagicMock()

    with patch("daemon.evoai_initializer_executor.EvoAIMonitor"), \
         patch("daemon.evoai_initializer_executor.EvoAIExecutor", side_effect=RuntimeError("boom")):

        with pytest.raises(RuntimeError, match="boom"):
            evoai_initializer_executor.initialize_executor(mock_agent, mock_engine, mock_context)
