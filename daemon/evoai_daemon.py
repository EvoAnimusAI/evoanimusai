# daemon/evoai_daemon.py
# -*- coding: utf-8 -*-
"""
EvoAI Daemon Principal — Nivel gubernamental
Punto de entrada del sistema simbólico-cognitivo EvoAI.
"""

import argparse
import logging
import os
import atexit
from dotenv import load_dotenv
load_dotenv()

from daemon.evoai_initializer_core import initialize_core_components
from daemon.evoai_cycle_executor import run_cycle_loop
from daemon.evoai_initializer_security import load_secure_key
from daemon.evoai_shutdown_manager import setup_signal_handlers
from core.self_diagnostics import SelfDiagnostics
from core.state_persistence import load_state, save_state

# Logger raíz
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] :: %(message)s",
    handlers=[
        logging.FileHandler("logs/evoai_super_daemon.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("EvoAI.Daemon")

DAEMON_KEY_FALLBACK = "A591243133418571088300454z"

# 🔒 Componente compartido para persistencia
components = None

def persist_final_state():
    global components
    if components is None:
        return
    try:
        # Se espera que components incluya una clave 'context' con el estado actual
        context = components.get("context", None)
        if context is not None and hasattr(context, "state"):
            save_state(context.state, encrypt=True)
            print("[💾 SAVE] Estado final guardado exitosamente (atexit).")
            logger.info("[SAVE] Estado guardado exitosamente al finalizar daemon (atexit).")
    except Exception as e:
        print(f"[❌ SAVE ERROR] Fallo al guardar estado (atexit): {e}")
        logger.error(f"[SAVE ERROR] {e}")

# Registrar hook de salida segura
atexit.register(persist_final_state)

def main(daemon_key: str, test_mode: bool = False, resume: bool = False):
    global components
    setup_signal_handlers()

    if daemon_key != DAEMON_KEY_FALLBACK and daemon_key != load_secure_key():
        logger.critical("🔒 Clave inválida. Acceso denegado.")
        return

    logger.info("🔑 Clave aceptada. Iniciando EvoAI...")

    # Intentar restaurar estado persistente si se indica
    initial_state = {}
    if resume:
        try:
            initial_state = load_state(decrypt=True)
            logger.info("[🔁 RESUME] Estado cargado correctamente desde disco.")
            print("[🔁 RESUME] Estado restaurado desde archivo persistente.")
        except Exception as e:
            logger.warning(f"[⚠️ RESUME ERROR] No se pudo cargar estado previo: {e}")
            print(f"[⚠️ RESUME ERROR] Fallo al cargar estado anterior: {e}")

    components = initialize_core_components(initial_state=initial_state)

    diagnostics = SelfDiagnostics(components)
    if not diagnostics.run_preflight_check(daemon_key):
        logger.critical("🚨 Diagnóstico fallido. Abortando daemon.")
        return

    try:
        run_cycle_loop(test_mode=test_mode)  # ❗️NO pasamos 'components' si no lo acepta
    finally:
        persist_final_state()  # Llamada explícita además del atexit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EvoAI Super Symbolic Daemon")
    parser.add_argument("--key", required=False, help="Clave de acceso para el daemon")
    parser.add_argument("--test", action="store_true", help="Ejecutar en modo prueba (test_mode)")
    parser.add_argument("--resume", action="store_true", help="Reanudar estado desde disco (state resume)")

    args = parser.parse_args()
    daemon_key = args.key if args.key else load_secure_key()

    main(daemon_key, test_mode=args.test, resume=args.resume)
