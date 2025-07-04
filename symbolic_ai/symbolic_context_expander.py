# symbolic_ai/symbolic_context_expander.py
# Clasificación: Militar / Gubernamental / Ultra-secreto
# Propósito: Expansión segura y validada del contexto simbólico
# Responsable: Unidad de Expansión Cognitiva (UEC)
# Cumple con norma: EVO-SYM/CONTEXT-SEC/STD-2099

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class SymbolicContextExpander:
    """
    Módulo de expansión de contexto simbólico.
    Refuerza la estructura mínima del contexto, asegurando integridad operativa.
    """

    REQUIRED_FIELDS = {
        "state": "initialized",
        "observations": {},
        "parameters": {},
        "rewards": [],
        "history": [],
    }

    @classmethod
    def expand(cls, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expande el contexto simbólico insertando campos obligatorios
        si no existen, con valores seguros por defecto.

        Args:
            context (Dict[str, Any]): Contexto simbólico en crudo.

        Returns:
            Dict[str, Any]: Contexto expandido, estructurado y trazable.
        """
        if not isinstance(context, dict):
            logger.critical("[Expander] ERROR: El contexto no es un diccionario.")
            raise TypeError("El contexto simbólico debe ser un diccionario estructurado.")

        for key, default in cls.REQUIRED_FIELDS.items():
            if key not in context:
                logger.warning(f"[Expander] Campo faltante '{key}' insertado con valor por defecto.")
                context[key] = default
            else:
                # Validación tipo estricta (nivel militar)
                if type(context[key]) != type(default):
                    logger.error(f"[Expander] Tipo inválido para '{key}': esperado {type(default)}, recibido {type(context[key])}")
                    raise ValueError(f"Tipo inválido para campo '{key}' en el contexto simbólico.")

        logger.debug(f"[Expander] Contexto simbólico expandido y validado: {context}")
        return context
