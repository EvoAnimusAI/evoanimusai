import pytest
from unittest.mock import MagicMock, patch
from daemon import evoai_initializer_decision


def test_initialize_decision_success():
    mock_context = MagicMock()
    mock_context.symbolic_engine = None
    mock_context.assert_fact = MagicMock()

    mock_engine = MagicMock()
    mock_agent = MagicMock()

    with patch("daemon.evoai_initializer_decision.SymbolicDecisionEngine") as mock_decision_class:
        mock_decision = MagicMock()
        mock_decision.decide = MagicMock()
        mock_decision_class.return_value = mock_decision

        result = evoai_initializer_decision.initialize_decision(mock_context, mock_agent, mock_engine)

        assert result is mock_decision
        assert mock_context.symbolic_engine == mock_decision
        mock_context.assert_fact.assert_any_call("decision_engine_ready", True)
        mock_context.assert_fact.assert_any_call("decision_engine_class", mock_decision.__class__.__name__)


def test_initialize_decision_prioritize_not_callable():
    mock_context = MagicMock()
    mock_context.symbolic_engine = None
    mock_context.assert_fact = MagicMock()

    mock_engine = MagicMock()
    mock_agent = MagicMock()

    with patch("daemon.evoai_initializer_decision.SymbolicDecisionEngine") as mock_decision_class:
        mock_decision = MagicMock()
        mock_decision.decide = MagicMock()
        mock_decision.prioritize = "not_callable"
        mock_decision_class.return_value = mock_decision

        result = evoai_initializer_decision.initialize_decision(mock_context, mock_agent, mock_engine)

        assert result is mock_decision


def test_initialize_decision_fails_gracefully():
    mock_context = MagicMock()
    mock_engine = MagicMock()
    mock_agent = MagicMock()

    with patch("daemon.evoai_initializer_decision.SymbolicDecisionEngine", side_effect=Exception("boom")):
        with pytest.raises(RuntimeError, match="Inicialización fallida"):
            evoai_initializer_decision.initialize_decision(mock_context, mock_agent, mock_engine)
