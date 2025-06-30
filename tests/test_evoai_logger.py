# tests/test_evoai_logger.py
# -*- coding: utf-8 -*-

"""
Test gubernamental para el módulo evoai_logger.py.
Verifica la correcta inicialización del logger central, la escritura de auditoría
en archivo local, y la trazabilidad dual a través de logger + archivo.
"""

import logging
import pytest
from pathlib import Path
from unittest import mock
from daemon import evoai_logger


@pytest.fixture(autouse=True)
def clean_logfile():
    """Limpieza automática de archivo local de auditoría antes y después de cada test."""
    log_file = Path("evoai_log.txt")
    if log_file.exists():
        log_file.unlink()
    yield
    if log_file.exists():
        log_file.unlink()


def test_logger_instance_type():
    """Verifica que el logger global esté correctamente instanciado y configurado."""
    assert isinstance(evoai_logger.logger, logging.Logger)
    assert evoai_logger.logger.name == "EvoAI.SuperDaemon"


@mock.patch("daemon.evoai_logger.logger")
def test_log_local_calls_logger(mock_logger):
    """Verifica que log_local escribe y llama correctamente a logger.info."""
    message = "Mensaje de prueba crítico"
    evoai_logger.log_local(message)

    # Verifica que logger.info fue llamado
    mock_logger.info.assert_called_once_with(message)

    # Verifica que el archivo fue creado y contiene el mensaje
    with open("evoai_log.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert any(message in line for line in lines)


@mock.patch("pathlib.Path.open", new_callable=mock.mock_open)
@mock.patch("daemon.evoai_logger.logger")
def test_log_local_uses_file_and_logger(mock_logger, mock_open):
    """Verifica uso conjunto de Path.open y logger.info sin escritura real."""
    test_msg = "Auditoría: entrada simulada"
    evoai_logger.log_local(test_msg)

    # Verifica que Path.open fue invocado correctamente
    mock_open.assert_called_once_with("a", encoding="utf-8")

    # Verifica que se escribió el mensaje
    handle = mock_open()
    handle.write.assert_called_once_with(f"{test_msg}\n")

    # Verifica que logger.info fue llamado
    mock_logger.info.assert_called_once_with(test_msg)
