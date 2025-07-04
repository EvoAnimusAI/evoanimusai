# symbolic_ai/function_evaluator.py
# -*- coding: utf-8 -*-
"""
Evaluador de Funciones Mutadas — Nivel gubernamental, científico y militar.
-------------------------------------------------------------------------------
Evalúa funciones simbólicas mutadas dentro de un contexto controlado,
con validaciones estrictas, trazabilidad y tolerancia a fallos.

Autor: Daniel Santiago Ospina Vel
"""

import logging
from typing import Any, Optional, Callable

logger = logging.getLogger(__name__)

def evaluate_mutated_function(
    function: Any,
    context: Optional[dict] = None
) -> Any:
    """
    Evalúa una función mutada dentro de un contexto opcional.

    Args:
        function: Función o callable mutado a evaluar.
        context: Contexto opcional a pasar a la función.

    Returns:
        Resultado de la evaluación, o None si ocurre un error.

    Maneja errores, valida callability y registra trazabilidad detallada.
    """
    logger.info(f"[EVALUADOR] Iniciando evaluación de función mutada: {function}")

    # Validación estricta: callable o método __call__
    if not callable(function):
        if hasattr(function, '__call__') and callable(getattr(function, '__call__')):
            logger.warning(f"[EVALUADOR] Objeto no callable directo, pero posee __call__. Se utilizará.")
            function_callable: Callable = getattr(function, '__call__')
        else:
            logger.error(f"[EVALUADOR] El objeto NO es callable ni implementa __call__: {function}. Evaluación cancelada.")
            return None
    else:
        function_callable = function

    try:
        result = function_callable(context) if context is not None else function_callable()
        logger.info(f"[EVALUADOR] Evaluación exitosa. Resultado: {result}")
        return result

    except Exception as e:
        logger.error(f"[EVALUADOR] Error durante la evaluación: {e}", exc_info=True)
        return None
