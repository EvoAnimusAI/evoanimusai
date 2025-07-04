# core/state_persistence.py
import json
import os
import hashlib
import logging
import shutil
from datetime import datetime

from cryptography.fernet import Fernet, InvalidToken

logger = logging.getLogger("EvoAI.StatePersistence")

STATE_FILE = "data/evostate_checkpoint.json"
HASH_FILE = "data/evostate_checksum.sha256"
BACKUP_DIR = "data/backups/"
ENCRYPTION_KEY_ENV = "EVOAI_STATE_KEY"  # Base64-encoded key


# -------- UTILIDADES --------

def _compute_sha256(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def _backup_state_file():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    backup_path = os.path.join(BACKUP_DIR, f"evostate_{timestamp}.bak")
    shutil.copyfile(STATE_FILE, backup_path)
    print(f"[📁 BACKUP] Backup generado: {backup_path}")
    logger.info(f"[BACKUP] Estado respaldado: {backup_path}")

def _get_fernet():
    key = os.getenv(ENCRYPTION_KEY_ENV)
    if not key:
        raise EnvironmentError(f"[❌ CRYPTO] Falta variable {ENCRYPTION_KEY_ENV}")
    return Fernet(key)


# -------- FUNCIONES PRINCIPALES --------

def save_state(state: dict, encrypt: bool = False):
    try:
        content = json.dumps(state, indent=4, ensure_ascii=False).encode("utf-8")
        if encrypt:
            fernet = _get_fernet()
            content = fernet.encrypt(content)
            print("[🔐 ENCRYPT] Estado cifrado con AES-256.")
            logger.info("[SAVE] Estado cifrado antes de guardar.")
        else:
            print("[💾 SAVE] Estado sin cifrar.")

        with open(STATE_FILE, "wb") as f:
            f.write(content)
        _backup_state_file()

        hash_digest = _compute_sha256(STATE_FILE)
        with open(HASH_FILE, "w") as h:
            h.write(hash_digest)
        print(f"[✅ GUARDADO] Estado persistente escrito con hash: {hash_digest}")
        logger.info(f"[SAVE] Guardado y verificado con hash: {hash_digest}")

    except Exception as e:
        print(f"[❌ ERROR] Error al guardar estado: {e}")
        logger.error(f"[ERROR] Al guardar estado: {e}")
        raise

def load_state(decrypt: bool = False) -> dict:
    if not os.path.exists(STATE_FILE):
        print("[⚠️ LOAD] No existe archivo de estado.")
        return {}

    try:
        current_hash = _compute_sha256(STATE_FILE)
        with open(HASH_FILE, "r") as h:
            stored_hash = h.read().strip()

        if current_hash != stored_hash:
            print("[🛑 ALERTA] Integridad de estado comprometida. Abortando carga.")
            logger.critical("[HASH MISMATCH] El hash del estado no coincide.")
            raise ValueError("Integridad comprometida")

        with open(STATE_FILE, "rb") as f:
            content = f.read()

        if decrypt:
            fernet = _get_fernet()
            try:
                content = fernet.decrypt(content)
                print("[🔓 DECRYPT] Estado descifrado correctamente.")
                logger.info("[LOAD] Estado descifrado con éxito.")
            except InvalidToken:
                print("[❌ CRYPTO ERROR] Clave inválida al descifrar estado.")
                logger.critical("[ERROR] Descifrado fallido. Token inválido.")
                raise

        state = json.loads(content.decode("utf-8"))
        print("[📥 RESTORE] Estado restaurado correctamente.")
        logger.info("[LOAD OK] Estado cargado y verificado.")
        return state

    except Exception as e:
        print(f"[❌ ERROR] Fallo en carga de estado: {e}")
        logger.error(f"[LOAD ERROR] {e}")
        raise
