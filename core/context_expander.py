# core/context_expander.py
# -*- coding: utf-8 -*-
"""
Módulo de extensión de contexto para EvoAnimusAI.
Responsabilidad: manejar claves simbólicas extendidas como 'symbiotic_progress', 'cognitive_load', 'threat_index', etc.

Nivel: Militar / Gubernamental / Ultra-secreto
"""

import logging
from typing import Dict, Any

logger = logging.getLogger("EvoAI.ContextExpander")
logger.setLevel(logging.INFO)

class ContextExpander:
    """
    Expansor de contexto simbólico para claves extendidas.

    Uso:
        expander = ContextExpander(context_ref)
        expander.set("symbiotic_progress", 0.85)
    """

    def __init__(self, context_ref: Dict[str, Any]):
        self.context = context_ref
        logger.info("[Init] ContextExpander vinculado al contexto.")

    def set(self, key: str, value: Any) -> None:
        if not isinstance(key, str):
            raise ValueError("La clave debe ser un string.")
        logger.info(f"[Set] Clave extendida establecida: {key} = {value}")
        self.context[key] = value

    def get(self, key: str) -> Any:
        value = self.context.get(key)
        logger.info(f"[Get] Clave extendida consultada: {key} = {value}")
        return value

    def delete(self, key: str) -> None:
        if key in self.context:
            logger.info(f"[Delete] Clave extendida eliminada: {key}")
            del self.context[key]

    def export_all(self) -> Dict[str, Any]:
        logger.debug("[Export] Exportando state expandido.")
        return dict(self.context)
