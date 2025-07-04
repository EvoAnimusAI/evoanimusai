# utils/evo_logging.py
# -*- coding: utf-8 -*-

"""
🧭 Módulo de Logging Centralizado — EvoAI (con doble salida)
Versión: 1.1.0 | Seguridad: RESTRINGIDO
"""

import logging
import sys
from datetime import datetime

# ==========================
# ⚙️ Configuración del Logger
# ==========================

_logger = logging.getLogger("evoai.logger")
_logger.setLevel(logging.DEBUG)

_consola_handler = logging.StreamHandler(sys.stdout)
_consola_handler.setLevel(logging.DEBUG)

_formato = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s - [🧭 LOG] Evento: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ"
)
_consola_handler.setFormatter(_formato)

if not _logger.handlers:
    _logger.addHandler(_consola_handler)

# ==========================
# 🧪 Modo seguimiento interactivo
# ==========================

MODO_DEBUG = True  # Cambiar a False en producción

# ==========================
# 📣 Función pública de log seguro
# ==========================

def log(mensaje: str, level: str = "INFO", detalles: dict = None):
    """
    Publica un mensaje al logger centralizado con opción de print directo.
    :param mensaje: Texto del evento
    :param level: Nivel ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    :param detalles: Diccionario opcional con contexto adicional
    """
    detalles_str = f" | Detalles: {detalles}" if detalles else " | Detalles: {}"
    texto = f"{mensaje}{detalles_str}"

    # 🧭 Print visible para pruebas en modo interactivo
    if MODO_DEBUG:
        print(f"[🖨️ DEBUG PRINT] {texto}")

    if level == "DEBUG":
        _logger.debug(texto)
    elif level == "INFO":
        _logger.info(texto)
    elif level == "WARNING":
        _logger.warning(texto)
    elif level == "ERROR":
        _logger.error(texto)
    elif level == "CRITICAL":
        _logger.critical(texto)
    else:
        _logger.info(texto)
