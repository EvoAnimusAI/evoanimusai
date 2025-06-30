# evoai_logger.py
# -*- coding: utf-8 -*-

"""
EvoAI Logger - Módulo de trazabilidad y registro centralizado a nivel gubernamental.
Responsable de garantizar el cumplimiento de estándares de auditoría, trazabilidad y supervisión continua.
"""

import os
import sys
import logging
from pathlib import Path
from daemon.evoai_config import LOG_DIR, LOG_FILE


# Asegurar estructura de directorio
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

# Configuración global del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] :: %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE), encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Logger de acceso global
logger = logging.getLogger("EvoAI.SuperDaemon")


def log_local(message: str):
    """Registra mensaje en archivo local adicional para trazabilidad independiente."""
    log_path = Path("evoai_log.txt")
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"{message}\n")
    logger.info(message)


__all__ = ["logger", "log_local"]
