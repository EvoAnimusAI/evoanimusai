# core/context_patch_handler.py
# Clasificación: Militar / Gubernamental / Ultra-secreto
# Propósito: Control seguro de modificaciones al contexto simbólico
# Norma: EVO-CTX/PATCH-GOV-2178
# Unidad Responsable: Centro de Integridad Contextual (CIC)

import logging
from typing import Dict, Any, Set

logger = logging.getLogger(__name__)

class ContextPatchHandler:
    """
    Sistema de gestión de parches al contexto simbólico.
    Supervisa, valida y autoriza escrituras sobre claves estructurales y extendidas.
    """

    # Claves permitidas explícitamente
    SAFE_KEYS: Set[str] = {
        "symbiotic_progress",
        "adaptive_entropy",
        "emergency_mode",
        "symbolic_latency",
        "last_mutation_result",
        "diagnostic_checksum"
    }

    @classmethod
    def safe_set(cls, context: Dict[str, Any], key: str, value: Any) -> None:
        """
        Intenta asignar un valor al contexto bajo reglas de seguridad estrictas.

        Args:
            context (Dict[str, Any]): Contexto simbólico operativo.
            key (str): Clave que se desea modificar o crear.
            value (Any): Valor a asignar.

        Raises:
            KeyError: Si la clave no está permitida ni registrada en el contexto.
        """
        if not isinstance(context, dict):
            logger.critical("[PatchHandler] ERROR: El contexto no es un diccionario.")
            raise TypeError("Contexto inválido: se esperaba un diccionario estructurado.")

        if key in cls.SAFE_KEYS or key in context:
            context[key] = value
            logger.info(f"[PatchHandler] ✅ Modificación permitida: '{key}' <- {repr(value)}")
        else:
            logger.critical(f"[PatchHandler] ❌ Modificación bloqueada: clave no autorizada '{key}'")
            raise KeyError(f"Context does not support setting key '{key}'")

    @classmethod
    def authorize_key(cls, key: str) -> None:
        """
        Agrega dinámicamente una clave a la lista segura de modificación.

        Args:
            key (str): Nombre de la clave a autorizar.
        """
        if key not in cls.SAFE_KEYS:
            cls.SAFE_KEYS.add(key)
            logger.warning(f"[PatchHandler] ⚠️ Clave '{key}' autorizada dinámicamente.")

    @classmethod
    def revoke_key(cls, key: str) -> None:
        """
        Elimina una clave de la lista segura.

        Args:
            key (str): Clave a revocar.
        """
        if key in cls.SAFE_KEYS:
            cls.SAFE_KEYS.remove(key)
            logger.warning(f"[PatchHandler] 🔒 Clave '{key}' revocada del contexto seguro.")

    @classmethod
    def list_safe_keys(cls) -> Set[str]:
        """
        Devuelve el conjunto actual de claves permitidas.

        Returns:
            Set[str]: Claves autorizadas para modificación directa.
        """
        return cls.SAFE_KEYS.copy()
