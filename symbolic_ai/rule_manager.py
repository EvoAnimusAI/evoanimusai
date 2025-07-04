# -*- coding: utf-8 -*-
"""
Módulo de gestión avanzada de reglas simbólicas para EvoAnimusAI.
Incluye control de versiones, persistencia extendida, auditoría y recuperación segura.
"""

import json
import hashlib
import os
import shutil
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class RuleManager:
    def __init__(self, storage_path: str = "data/rules", versioning_enabled: bool = True):
        self.storage_path = storage_path
        self.versioning_enabled = versioning_enabled
        os.makedirs(self.storage_path, exist_ok=True)
        logger.debug(f"[RuleManager] Inicializado con path: {self.storage_path}")

    def _compute_checksum(self, rule: Dict[str, Any]) -> str:
        rule_str = json.dumps(rule, sort_keys=True)
        checksum = hashlib.sha256(rule_str.encode("utf-8")).hexdigest()
        logger.debug(f"[RuleManager] Checksum generado: {checksum}")
        return checksum

    def version_rule(self, rule: Dict[str, Any]) -> Dict[str, Any]:
        versioned = rule.copy()
        versioned["version"] = datetime.utcnow().isoformat()
        versioned["checksum"] = self._compute_checksum(rule)
        logger.info(f"[RuleManager] Regla versionada: {versioned['version']}")
        return versioned

    def save_rules(self, rules: List[Dict[str, Any]], filename: str = "rules.json") -> None:
        path = os.path.join(self.storage_path, filename)
        backup_path = os.path.join(self.storage_path, f"backup_{datetime.utcnow().isoformat()}.json")

        # Crear backup
        if os.path.exists(path):
            shutil.copy(path, backup_path)
            logger.info(f"[RuleManager] Backup creado en: {backup_path}")

        # Versionar reglas si está habilitado
        versioned_rules = [self.version_rule(rule) for rule in rules] if self.versioning_enabled else rules

        # Guardar reglas
        with open(path, "w", encoding="utf-8") as f:
            json.dump(versioned_rules, f, indent=4)
        logger.info(f"[RuleManager] Reglas guardadas en: {path}")

    def load_rules(self, filename: str = "rules.json") -> List[Dict[str, Any]]:
        path = os.path.join(self.storage_path, filename)
        if not os.path.exists(path):
            logger.warning(f"[RuleManager] Archivo no encontrado: {path}")
            return []

        with open(path, "r", encoding="utf-8") as f:
            rules = json.load(f)
        logger.info(f"[RuleManager] {len(rules)} reglas cargadas desde: {path}")
        return rules

    def diff_rules(self, old_rules: List[Dict[str, Any]], new_rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        old_checksums = {self._compute_checksum(rule): rule for rule in old_rules}
        new_checksums = {self._compute_checksum(rule): rule for rule in new_rules}

        diffs = []
        for checksum, rule in new_checksums.items():
            if checksum not in old_checksums:
                diffs.append(rule)
        logger.info(f"[RuleManager] Diferencias encontradas: {len(diffs)}")
        return diffs

    def rollback_rule(self, rule_id: str, backup_filename: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Restaura una regla desde un archivo de backup según su ID (asume que las reglas tienen 'id').
        """
        backups = sorted([
            f for f in os.listdir(self.storage_path)
            if f.startswith("backup_") and f.endswith(".json")
        ], reverse=True)

        for backup in backups:
            path = os.path.join(self.storage_path, backup)
            with open(path, "r", encoding="utf-8") as f:
                try:
                    rules = json.load(f)
                    for rule in rules:
                        if rule.get("id") == rule_id:
                            logger.warning(f"[RuleManager] Regla {rule_id} recuperada desde: {path}")
                            return rule
                except Exception as e:
                    logger.error(f"[RuleManager] Error procesando backup {path}: {e}")
                    continue

        logger.error(f"[RuleManager] No se encontró regla con ID: {rule_id} en backups")
        return None
# === Interfaces externas seguras ===

_default_manager = RuleManager()

def version_rule(rule: Dict[str, Any]) -> Dict[str, Any]:
    return _default_manager.version_rule(rule)

def diff_rules(old_rules: List[Dict[str, Any]], new_rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return _default_manager.diff_rules(old_rules, new_rules)
