# tests/test_evoai_visualization.py
import pytest
from unittest.mock import patch, MagicMock

from daemon import evoai_visualization


def test_render_symbolic_state_success():
    context = {"state": "alerta"}
    decision = "explore"
    observation = {"threat": False}
    reward = 0.85

    with patch("daemon.evoai_visualization.show_symbolic_state") as mock_render:
        evoai_visualization.render_symbolic_state(context, decision, observation, reward)
        mock_render.assert_called_once_with(context, decision, observation, reward)


def test_render_symbolic_state_exception(caplog):
    context = {}
    decision = "idle"
    observation = {}
    reward = 0.0

    with patch("daemon.evoai_visualization.show_symbolic_state", side_effect=RuntimeError("Render failed")):
        with caplog.at_level("WARNING"):
            evoai_visualization.render_symbolic_state(context, decision, observation, reward)
            assert any("Falló renderización simbólica" in message for message in caplog.messages)
