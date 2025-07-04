# monitoring/context_anomaly_logger.py
# Clasificación: Militar / Gubernamental / Ultra-secreto
# Propósito: Detección anticipada de anomalías estructurales en el contexto simbólico
# Norma: EVO-MON/CTX-VAL-4042
# Unidad Responsable: División de Monitoreo Cognitivo Preventivo (DMCP)

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ContextAnomalyLogger:
    """
    Sistema de validación militar para contextos simbólicos.
    Detecta y registra inconsistencias estructurales que puedan comprometer decisiones.
    """

    REQUIRED_KEYS = {
        "state": str,
        "observations": dict,
        "history": list,
        "rewards": list,
        "parameters": dict,
    }

    @classmethod
    def validate_and_log(cls, context: Dict[str, Any]) -> bool:
        """
        Valida profundamente el contexto simbólico y registra cualquier anomalía.

        Args:
            context (Dict[str, Any]): Diccionario de contexto simbólico.

        Returns:
            bool: True si el contexto es válido, False si se detectan anomalías.
        """
        if not isinstance(context, dict):
            logger.critical("[ContextAnomaly] ❌ El contexto no es un diccionario.")
            return False

        missing_keys: List[str] = []
        type_mismatches: List[str] = []

        for key, expected_type in cls.REQUIRED_KEYS.items():
            if key not in context:
                missing_keys.append(key)
            elif not isinstance(context[key], expected_type):
                type_mismatches.append(f"{key} (esperado: {expected_type.__name__}, recibido: {type(context[key]).__name__})")

        if missing_keys:
            logger.error(f"[ContextAnomaly] 🚨 Claves faltantes en el contexto: {missing_keys}")

        if type_mismatches:
            logger.error(f"[ContextAnomaly] ⚠️ Inconsistencias de tipo en el contexto: {type_mismatches}")

        if missing_keys or type_mismatches:
            logger.critical("[ContextAnomaly] ⛔ Contexto inválido detectado. Requiere intervención o rechazo preventivo.")
            logger.debug(f"[ContextAnomaly] Estado completo del contexto al fallar: {context}")
            return False

        logger.debug("[ContextAnomaly] ✅ Contexto validado correctamente.")
        return True
