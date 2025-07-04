# daemon/evoai_shutdown_manager.py
# -*- coding: utf-8 -*-
"""
Módulo de manejo seguro de apagado para EvoAI.
Intercepta señales del sistema y asegura cierre ordenado.
Compatible con Ctrl+C, kill, cierre de terminal, etc.
"""

import os
import sys
import signal
import threading
import logging
import time

logger = logging.getLogger("EvoAI.Shutdown")
logger.setLevel(logging.INFO)

# Lock de sincronización para evitar apagados duplicados
_shutdown_lock = threading.Lock()
_shutdown_initiated = False

def shutdown_all():
    """
    Ejecuta el apagado ordenado de todos los subsistemas.
    """
    global _shutdown_initiated

    with _shutdown_lock:
        if _shutdown_initiated:
            logger.warning("🔁 Apagado ya en curso. Ignorando nueva solicitud.")
            return
        _shutdown_initiated = True

        logger.info("🔒 Iniciando apagado seguro de EvoAI...")
        print("[🛑] Apagando subsistemas de EvoAI...")

        try:
            # ⛔ Cierre de hilos, subprocesos o tareas activas
            # Añadir llamadas de cierre aquí (según subsistemas utilizados)
            # Por ejemplo: executor.stop_all(), engine.shutdown(), etc.

            # 🧠 Persistir state crítico si aplica
            # memory.save(), context.dump(), etc.

            # 🔐 Cierre de recursos de seguridad
            # network_access.close_connections(), etc.

            # Espera de sincronización
            time.sleep(0.2)

            logger.info("✅ Apagado completo. Recursos liberados.")
            print("[✔️] EvoAI detenido correctamente.")
        except Exception as e:
            logger.exception(f"⚠️ Error durante apagado: {e}")
            print(f"[❌] Falla en apagado: {e}")
        finally:
            os._exit(0)  # Fuerza cierre sin excepciones colgantes

def _signal_handler(sig, frame):
    """
    Manejador universal de señales OS.
    """
    signal_name = signal.Signals(sig).name
    logger.info(f"📡 Señal recibida: {signal_name}")
    print(f"\n[🔴] Señal recibida: {signal_name}. Iniciando apagado...")
    shutdown_all()

def setup_signal_handlers():
    """
    Registra los manejadores de señal OS para apagado limpio.
    """
    logger.info("⚙️ Configurando manejadores de señal para apagado...")

    signal.signal(signal.SIGINT, _signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, _signal_handler)  # kill
    signal.signal(signal.SIGHUP, _signal_handler)   # terminal cerrada
    signal.signal(signal.SIGQUIT, _signal_handler)  # Ctrl+\

    logger.info("🧬 Señales capturadas: SIGINT, SIGTERM, SIGHUP, SIGQUIT")
