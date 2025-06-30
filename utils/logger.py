# utils/logger.py

import os
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

LOG_DIR = "logs"
MAIN_LOG = os.path.join(LOG_DIR, "evoai.log")


def initialize_logger():
    """
    Inicializa el sistema de logging.
    Asegura creación de carpeta y archivo de log.
    Configura handler rotativo con tamaño máximo y backups.
    Consola con formato homogéneo.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("evoai")
    logger.setLevel(logging.DEBUG)

    # Evitar duplicación de handlers si ya configurado
    if not logger.handlers:
        # Handler para archivo rotativo
        file_handler = RotatingFileHandler(
            MAIN_LOG, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


def log_event(tipo, **kwargs):
    """
    Registra evento estructurado (formato JSON) en archivo separado por tipo.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().isoformat()
    data = {
        "timestamp": timestamp,
        "tipo": tipo,
        **kwargs
    }

    filename = os.path.join(LOG_DIR, f"{tipo}.log")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def log(message: str, level: str = "INFO"):
    """
    Logger flexible con niveles.
    Imprime por consola y guarda en archivo principal.
    """
    logger = logging.getLogger("evoai")

    if not logger.handlers:
        initialize_logger()

    level = level.upper()
    if level == "DEBUG":
        logger.debug(message)
    elif level == "INFO":
        logger.info(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "CRITICAL":
        logger.critical(message)
    else:
        logger.info(f"[Unknown level: {level}] {message}")
