import pytest
import threading
from unittest.mock import patch

from daemon import evoai_shutdown_manager


def test_shutdown_all_once(monkeypatch):
    # Resetear el state del módulo antes de cada test
    evoai_shutdown_manager._shutdown_initiated = False

    # Mock de os._exit para evitar que termine el test
    with patch("os._exit") as mock_exit:
        evoai_shutdown_manager.shutdown_all()
        assert evoai_shutdown_manager._shutdown_initiated is True
        mock_exit.assert_called_once_with(0)


def test_shutdown_all_twice(monkeypatch):
    evoai_shutdown_manager._shutdown_initiated = False

    with patch("os._exit") as mock_exit, \
         patch.object(evoai_shutdown_manager.logger, "warning") as mock_warn:

        # Primera llamada: debe ejecutar apagado
        evoai_shutdown_manager.shutdown_all()
        assert mock_exit.call_count == 1

        # Segunda llamada: debe ignorar apagado duplicado
        evoai_shutdown_manager.shutdown_all()
        assert mock_warn.call_count == 1
        assert mock_exit.call_count == 1  # No se vuelve a ejecutar

