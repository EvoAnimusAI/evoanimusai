import pytest
from unittest.mock import patch, MagicMock
from daemon import evoai_visualization


@patch("daemon.evoai_visualization.show_symbolic_state")
def test_render_symbolic_state_success(mock_show):
    context = {"state": "active"}
    decision = {"action": "move"}
    observation = {"input": "external"}
    reward = 0.85

    evoai_visualization.render_symbolic_state(context, decision, observation, reward)

    mock_show.assert_called_once_with(context, decision, observation, reward)


@patch("daemon.evoai_visualization.show_symbolic_state", side_effect=Exception("RenderFail"))
@patch("daemon.evoai_visualization.logger")
def test_render_symbolic_state_failure(mock_logger, mock_show):
    evoai_visualization.render_symbolic_state({}, {}, {}, 0.0)

    mock_show.assert_called_once()
    mock_logger.warning.assert_called_once()
    assert "[Visualización] Falló renderización simbólica" in mock_logger.warning.call_args[0][0]
