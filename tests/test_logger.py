# tests/test_logger.py

import os
import json
import logging
import pytest
from utils import logger

LOG_DIR = "logs"
MAIN_LOG = os.path.join(LOG_DIR, "evoai.log")


def setup_module(module):
    # Limpiar logs antes de cada módulo test
    if os.path.exists(MAIN_LOG):
        os.remove(MAIN_LOG)
    if os.path.exists(LOG_DIR):
        for f in os.listdir(LOG_DIR):
            path = os.path.join(LOG_DIR, f)
            if os.path.isfile(path):
                os.remove(path)


def test_initialize_logger_creates_dir_and_handlers():
    # Forzar re-inicialización
    for handler in logging.getLogger("evoai").handlers[:]:
        logging.getLogger("evoai").removeHandler(handler)

    logger.initialize_logger()

    # Verifica creación carpeta
    assert os.path.isdir(LOG_DIR)
    # Verifica que se haya agregado un handler rotativo y consola
    handlers = logging.getLogger("evoai").handlers
    assert any(isinstance(h, logging.handlers.RotatingFileHandler) for h in handlers)
    assert any(isinstance(h, logging.StreamHandler) for h in handlers)


def test_log_creates_main_log_file_and_writes_levels():
    logger.log("Mensaje DEBUG", level="DEBUG")
    logger.log("Mensaje INFO", level="INFO")
    logger.log("Mensaje WARNING", level="WARNING")
    logger.log("Mensaje ERROR", level="ERROR")
    logger.log("Mensaje CRITICAL", level="CRITICAL")

    assert os.path.exists(MAIN_LOG)
    with open(MAIN_LOG, "r", encoding="utf-8") as f:
        logs = f.read()
    assert "Mensaje DEBUG" in logs
    assert "Mensaje INFO" in logs
    assert "Mensaje WARNING" in logs
    assert "Mensaje ERROR" in logs
    assert "Mensaje CRITICAL" in logs


def test_log_unknown_level_logs_info_with_notice():
    logger.log("Mensaje nivel desconocido", level="NOEXISTE")

    assert os.path.exists(MAIN_LOG)
    with open(MAIN_LOG, "r", encoding="utf-8") as f:
        logs = f.read()
    assert "[Unknown level: NOEXISTE]" in logs
    assert "Mensaje nivel desconocido" in logs


def test_log_event_creates_json_log_file():
    tipo = "evento_test"
    data = {"clave": "valor", "numero": 123}

    # Elimina archivo previo si existe
    filepath = os.path.join(LOG_DIR, f"{tipo}.log")
    if os.path.exists(filepath):
        os.remove(filepath)

    logger.log_event(tipo, **data)

    assert os.path.exists(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        line = f.readline()
        record = json.loads(line)

    assert record["tipo"] == tipo
    assert record["clave"] == "valor"
    assert record["numero"] == 123
    assert "timestamp" in record


def test_initialize_logger_idempotency():
    logger.initialize_logger()
    initial_handlers = logging.getLogger("evoai").handlers.copy()

    # Llamar nuevamente no debe agregar handlers extras
    logger.initialize_logger()
    current_handlers = logging.getLogger("evoai").handlers

    assert len(initial_handlers) == len(current_handlers)


if __name__ == "__main__":
    pytest.main()
