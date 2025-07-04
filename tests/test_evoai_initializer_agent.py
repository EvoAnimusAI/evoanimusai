import pytest
from unittest.mock import MagicMock, patch
from daemon import evoai_initializer_agent


def test_initialize_agent_success():
    mock_context = MagicMock()

    with patch("daemon.evoai_initializer_agent.EvoAgent") as mock_agent_class:
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent

        agent = evoai_initializer_agent.initialize_agent(name="TestAgent", context=mock_context)

        mock_agent_class.assert_called_once_with(name="TestAgent", context=mock_context)
        assert agent is mock_agent


def test_initialize_agent_without_context_raises():
    with pytest.raises(ValueError, match="contexto operativo.*obligatorio"):
        evoai_initializer_agent.initialize_agent(name="NoContext")


def test_initialize_agent_exception_logged_and_raised():
    mock_context = MagicMock()

    with patch("daemon.evoai_initializer_agent.EvoAgent", side_effect=RuntimeError("explota")):
        with pytest.raises(RuntimeError, match="explota"):
            evoai_initializer_agent.initialize_agent(name="ErrorAgent", context=mock_context)
