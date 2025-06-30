# evoai_daemon.py
# -*- coding: utf-8 -*-
"""
EvoAI Daemon Principal — Nivel gubernamental
Punto de entrada del sistema simbólico-cognitivo EvoAI.
"""

import argparse
import logging

from daemon.evoai_initializer_core import initialize_core_components
from daemon.evoai_cycle_executor import run_cycle_loop

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

# Llave maestra (debe ser protegida y cargada desde entorno en producción)
DAEMON_KEY = "A591243133418571088300454z"


def main(daemon_key: str, test_mode: bool = False):
    if daemon_key != DAEMON_KEY:
        logger.critical("🔒 Clave inválida. Acceso denegado.")
        return

    logger.info("🔑 Clave aceptada. Iniciando EvoAI...")
    components = initialize_core_components()
    run_cycle_loop(components, test_mode=test_mode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EvoAI Super Symbolic Daemon")
    parser.add_argument("--key", required=True, help="Clave de acceso para el daemon")
    parser.add_argument("--test", action="store_true", help="Ejecutar un solo ciclo de prueba")
    args = parser.parse_args()

    main(args.key, test_mode=args.test)
