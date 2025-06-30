# evoai_daemon.py
# -*- coding: utf-8 -*-
"""
EvoAI Daemon Principal — Nivel gubernamental
Punto de entrada del sistema simbólico-cognitivo EvoAI.
"""

import argparse
import logging
import os

from daemon.evoai_initializer_core import initialize_core_components
from daemon.evoai_cycle_executor import run_cycle_loop
from daemon.evoai_initializer_security import load_secure_key

# Configuración del logger raíz
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] :: %(message)s",
    handlers=[
        logging.FileHandler("logs/evoai_super_daemon.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("EvoAI.Daemon")

# Llave maestra por defecto (usada solo si no hay variable de entorno y no se pasa --key)
DAEMON_KEY_FALLBACK = "A591243133418571088300454z"


def main(daemon_key: str, test_mode: bool = False):
    # Comparación estricta de clave para acceso
    if daemon_key != DAEMON_KEY_FALLBACK and daemon_key != load_secure_key():
        logger.critical("🔒 Clave inválida. Acceso denegado.")
        return

    logger.info("🔑 Clave aceptada. Iniciando EvoAI...")
    components = initialize_core_components()
    run_cycle_loop(components, test_mode=test_mode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EvoAI Super Symbolic Daemon")
    parser.add_argument("--key", required=False, help="Clave de acceso para el daemon")
    parser.add_argument("--test", action="store_true", help="Ejecutar un solo ciclo de prueba")
    args = parser.parse_args()

    # Prioriza el argumento --key, si no se pasa, intenta cargar desde variable segura
    daemon_key = args.key if args.key else load_secure_key()

    main(daemon_key, test_mode=args.test)
