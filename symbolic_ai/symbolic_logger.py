# symbolic_logger.py
# -*- coding: utf-8 -*-
"""
SecureSymbolicLogger: Logger simbólico de misión crítica para EvoAI.
Cumple estándares gubernamentales, científicos y corporativos internacionales.
Provee trazabilidad, integridad, sincronización y seguridad avanzada.
"""

import logging
from logging.handlers import RotatingFileHandler
import threading
import json
import socket
from datetime import datetime
import traceback
import hashlib
from typing import Optional, Dict, Any
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class SecureSymbolicLogger:
    def __init__(
        self,
        log_file: str = "symbolic_log.jsonl",
        max_bytes: int = 10 * 1024 * 1024,
        backup_count: int = 10,
        level: int = logging.INFO,
        encryption_key: Optional[bytes] = None,
    ):
        self.hostname = socket.gethostname()
        self.lock = threading.Lock()
        self.encryption_key = encryption_key
        self.aesgcm = AESGCM(encryption_key) if encryption_key else None

        self.logger = logging.getLogger(f"SecureSymbolicLogger_{id(self)}")
        self.logger.setLevel(level)
        self.logger.propagate = False

        for handler in list(self.logger.handlers):
            self.logger.removeHandler(handler)

        handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def _encrypt(self, plaintext: bytes) -> str:
        nonce = os.urandom(12)
        ct = self.aesgcm.encrypt(nonce, plaintext, None)
        return base64.b64encode(nonce + ct).decode("utf-8")

    def _decrypt(self, b64_ciphertext: str) -> bytes:
        data = base64.b64decode(b64_ciphertext)
        nonce = data[:12]
        ct = data[12:]
        plaintext = self.aesgcm.decrypt(nonce, ct, None)
        try:
            record = json.loads(plaintext.decode("utf-8"))
            msg = record.get("message", "")
            return msg.encode("utf-8")
        except Exception:
            return plaintext

    def _compute_file_checksum(self, filename: str) -> str:
        sha256 = hashlib.sha256()
        try:
            with open(filename, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            self._fallback_log(f"Checksum error: {e}")
            return ""

    def _fallback_log(self, msg: str) -> None:
        print(f"[SecureSymbolicLogger ERROR] {msg}")

    def _build_record(
        self,
        level: str,
        message: str,
        extra: Optional[Dict[str, Any]] = None
    ) -> str:
        base_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "message": message,
            "hostname": self.hostname,
            "thread": threading.current_thread().name,
        }
        if extra:
            base_record.update(extra)
        return json.dumps(base_record, ensure_ascii=False)

    def log(
        self,
        message: str,
        level: int = logging.INFO,
        extra: Optional[Dict[str, Any]] = None
    ) -> None:
        try:
            level_name = logging.getLevelName(level)
            with self.lock:
                record_str = self._build_record(level_name, message, extra)
                if self.aesgcm:
                    record_str = self._encrypt(record_str.encode("utf-8"))
                self.logger.log(level, record_str)
        except Exception as e:
            self._fallback_log(f"{e} — {traceback.format_exc()}")

    # =============================
    # Métodos especializados
    # =============================

    def log_entry(self, agent: Optional[str], environment: Optional[str], cycle: Optional[int]) -> None:
        self.log(
            f"Ciclo {cycle if cycle is not None else '?'} iniciado",
            logging.INFO,
            {
                "type": "cycle_entry",
                "agent": agent or "unknown",
                "environment": environment or "unknown",
                "cycle": cycle,
            }
        )

    def log_agent(self, agent_name: str) -> None:
        self.log(
            f"Agente activo: {agent_name}",
            logging.INFO,
            {"type": "agent_activation", "agent": agent_name}
        )

    def log_decision(self, agent: str, decision_type: str, content: str) -> None:
        self.log(
            f"Decisión [{decision_type}]: {content}",
            logging.INFO,
            {
                "type": "agent_decision",
                "agent": agent,
                "decision_type": decision_type,
                "content": content,
            }
        )

    def log_synthesis(self, summary: str) -> None:
        self.log(
            "Síntesis simbólica generada",
            logging.INFO,
            {"type": "symbolic_synthesis", "summary": summary}
        )

    def log_concept(self, concept: str, source: str) -> None:
        self.log(
            f"Nuevo concepto: {concept}",
            logging.INFO,
            {"type": "symbolic_concept", "concept": concept, "source": source}
        )

    def log_learning(self, source: str, insight: str) -> None:
        self.log(
            "Aprendizaje registrado",
            logging.INFO,
            {"type": "learning_event", "source": source, "insight": insight}
        )

    def log_rewrite(self, name: str, description: Optional[str] = None, file_path: Optional[str] = None) -> None:
        self.log(
            "Reescritura ejecutada",
            logging.INFO,
            {
                "type": "code_rewrite",
                "component": name,
                "description": description,
                "file_path": file_path,
            }
        )

    def log_event(self, event: Dict[str, Any]) -> None:
        """
        Logging genérico de eventos arbitrarios.
        """
        self.log(
            message=event.get("message", "Evento simbólico"),
            level=logging.INFO,
            extra=event
        )


# =============================
# Exportación explícita
# =============================

secure_symbolic_logger = SecureSymbolicLogger()

log_entry     = secure_symbolic_logger.log_entry
log_agent     = secure_symbolic_logger.log_agent
log_decision  = secure_symbolic_logger.log_decision
log_synthesis = secure_symbolic_logger.log_synthesis
log_concept   = secure_symbolic_logger.log_concept
log_learning  = secure_symbolic_logger.log_learning
log_rewrite   = secure_symbolic_logger.log_rewrite
log_event     = secure_symbolic_logger.log_event
