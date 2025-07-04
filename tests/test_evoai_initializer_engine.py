import pytest
from unittest.mock import patch, MagicMock
from daemon import evoai_initializer_engine


def test_initialize_engine_success():
    with patch("daemon.evoai_initializer_engine.EvoAIEngine") as mock_engine_class:
        mock_engine = MagicMock()
        mock_engine_class.return_value = mock_engine

        engine = evoai_initializer_engine.initialize_engine()

        mock_engine_class.assert_called_once()
        assert engine is mock_engine


def test_initialize_engine_failure():
    with patch("daemon.evoai_initializer_engine.EvoAIEngine", side_effect=RuntimeError("boom")):
        with pytest.raises(RuntimeError, match="boom"):
            evoai_initializer_engine.initialize_engine()
