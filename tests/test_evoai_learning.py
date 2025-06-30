# tests/test_evoai_learning.py
import pytest
from unittest.mock import MagicMock, patch
from daemon.evoai_network_learning import learn_from_web

@patch("daemon.evoai_network_learning.log_concept")
@patch("daemon.evoai_network_learning.log_synthesis")
def test_learn_from_web_success(mock_log_synthesis, mock_log_concept):
    mock_consciousness = MagicMock()
    mock_net = MagicMock()
    mock_context = MagicMock()

    # Configurar mocks
    mock_net.summarize_topic.return_value = "Este es un resumen simbólico relevante."
    mock_net.learn_from_url.return_value = None

    # Mock de extracción de conceptos
    with patch("daemon.evoai_network_learning.extract_symbolic_concepts") as mock_extract:
        mock_extract.return_value = ["inteligencia artificial", "aprendizaje autónomo"]

        result = learn_from_web(
            consciousness=mock_consciousness,
            net=mock_net,
            topic="IA",
            url="https://es.wikipedia.org/wiki/Inteligencia_artificial",
            context=mock_context,
            cycle=1
        )

        # Verificaciones
        mock_consciousness.evaluate_integrity.assert_called_once()
        mock_net.learn_from_url.assert_called_once_with("https://es.wikipedia.org/wiki/Inteligencia_artificial", "IA")
        mock_net.summarize_topic.assert_called_once_with("IA")
        mock_log_synthesis.assert_called_once()
        mock_log_concept.assert_called()
        mock_context.add_concept.assert_called()
        assert result == "Este es un resumen simbólico relevante."

@patch("daemon.evoai_network_learning.logger")
def test_learn_from_web_exception(mock_logger):
    mock_consciousness = MagicMock()
    mock_consciousness.evaluate_integrity.side_effect = Exception("Falla simulada")

    result = learn_from_web(
        consciousness=mock_consciousness,
        net=MagicMock(),
        topic="IA",
        url="http://ejemplo.com",
        context=MagicMock(),
        cycle=1
    )

    mock_logger.error.assert_called()
    assert result is None
