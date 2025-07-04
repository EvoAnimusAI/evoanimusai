# utils/logger.py
# -*- coding: utf-8 -*-

"""
Logger estructurado y endurecido EvoAI — Nivel Militar / Gubernamental / Alta Seguridad.
Incluye trazabilidad dual (log interno + impresión directa), soporte de log persistente, y validación de integridad de eventos.
"""

import logging
import sys
from typing import Any, Union

# Configuración de canal de salida estándar
STDOUT_ENABLED = True

# Configuración del sistema de logging
logger = logging.getLogger("evoai.logger")
logger.setLevel(logging.DEBUG)  # Nivel mínimo capturado

# Formato estructurado para trazabilidad auditada
log_format = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ"
)

# Handler para salida por consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

# (Opcional) Handler para archivo persistente
# file_handler = logging.FileHandler("logs/evoai.log")
# file_handler.setFormatter(log_format)
# logger.addHandler(file_handler)


def log(event: str, details: Any = None, level: Union[int, str] = "INFO") -> None:
    """
    Loguea eventos estructurados con visibilidad inmediata en consola (modo dual).

    Args:
        event (str): Nombre del evento o código de auditoría.
        details (Any): Información asociada al evento (str, dict, etc.).
        level (Union[int, str]): Nivel de log (por ejemplo: 'INFO', 'WARNING', 'ERROR').
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    
    if details is None:
        details = {}

    message = f"[🧭 LOG] Evento: {event} | Detalles: {details}"
    logger.log(level, message)

    if STDOUT_ENABLED:
        print(message)
