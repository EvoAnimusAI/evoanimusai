# symbolic_ai/hypermutator.py
# -*- coding: utf-8 -*-
"""
Módulo de hipermutación simbólica de EvoAnimusAI.
Realiza mutaciones profundas de funciones, asegurando su validez y trazabilidad.

Nivel: Militar / Gubernamental / Ultra-secreto
"""

import logging
from typing import Callable, Optional

from symbolic_ai.mutation_validator import validate_and_prepare, log_invalid_mutation
from core.agent import EvoAgent  # 🔒 Protección explícita

logger = logging.getLogger("evoai.hypermutator")
logger.setLevel(logging.INFO)


def mutate_complete_function(function: Callable) -> Optional[Callable]:
    """
    Realiza una mutación simbólica de una función dada.
    La salida es siempre validada estructuralmente y preparada para ejecución segura.

    Args:
        function (Callable): Función a mutar.

    Returns:
        Optional[Callable]: Función mutada válida o None si la mutación falla.
    """
    if isinstance(function, EvoAgent):
        logger.warning(f"[⛔ Hypermutator] Objeto protegido detectado: {function}")
        log_invalid_mutation(function, reason="EvoAgent no debe ser tratado como función.")
        return None

    if not callable(function):
        logger.error(f"[❌ Hypermutator] El argumento no es callable: {repr(function)}")
        log_invalid_mutation(function)
        return None

    try:
        logger.info(f"[🧬 Hypermutator] Mutando función: {function.__name__}")

        # Simulación de mutación controlada — envuelve la función
        def mutated_function(*args, **kwargs):
            logger.info(f"[🧬 Hypermutator] Función mutada llamada: {function.__name__}")
            return function(*args, **kwargs)

        mutated_function.__name__ = f"mutated_{function.__name__}"
        mutated_function.__doc__ = f"Mutated version of {function.__name__}."
        mutated_function.__original_function__ = function

        # Validación estructural estricta
        safe_function = validate_and_prepare(mutated_function)

        if not callable(safe_function):
            logger.critical(f"[❌ Hypermutator] La función mutada NO es callable después de validación.")
            log_invalid_mutation(safe_function)
            return None

        logger.info(f"[✅ Hypermutator] Función mutada validada: {safe_function.__name__}")
        return safe_function

    except Exception as e:
        logger.exception(f"[❌ Hypermutator] Error durante mutación: {e}")
        return None
