# daemon/evoai_initializer_security.py
import os
import logging

logger = logging.getLogger("EvoAI.Security")

def load_secure_key() -> str:
    key = os.getenv("EVOAI_DAEMON_KEY")
    if not key:
        raise EnvironmentError("[CRITICAL] 🔐 Variable de entorno 'EVOAI_DAEMON_KEY' no configurada.")
    if len(key) < 20:
        raise ValueError("[CRITICAL] 🔐 DAEMON_KEY demasiado corta para estándares militares.")
    logger.info("[SECURITY] 🔐 Clave maestra cargada correctamente.")
    return key
