# daemon/evoai_initializer_decision.py
# -*- coding: utf-8 -*-
"""
Inicializador del módulo de decisión simbólica de EvoAnimusAI.
Estándar Militar / Gubernamental — con trazabilidad y redundancia estructural.
"""

import logging
from typing import Any

# Importación jerárquica oficial del motor simbólico
try:
    from core.symbolic_decision_engine import SymbolicDecisionEngine
except ImportError:
    try:
        from symbolic_ai.decision_module import SymbolicDecisionEngine
    except ImportError as e:
        raise ImportError(
            "[CRITICAL] No se pudo importar SymbolicDecisionEngine. "
            "Verifica core/symbolic_decision_engine.py o symbolic_ai/decision_module.py"
        ) from e

logger = logging.getLogger("EvoAI.Decision")

def debug_assert_fact_state(context: Any, key: str) -> None:
    logger.info(f"[DEBUG] Context symbolic_engine: {context.symbolic_engine}")
    logger.info(f"[DEBUG] Context engine: {context.engine}")
    symbolic_engine_has_method = callable(getattr(context.symbolic_engine, "assert_fact", None))
    engine_has_method = callable(getattr(context.engine, "assert_fact", None))
    logger.info(f"[DEBUG] symbolic_engine tiene assert_fact? {symbolic_engine_has_method}")
    logger.info(f"[DEBUG] engine tiene assert_fact? {engine_has_method}")

def initialize_decision(context: Any, agent: Any, engine: Any) -> Any:
    """
    Inicializa el módulo de decisión simbólica con configuración trazable.

    Args:
        context: Contexto operativo (EvoContext)
        agent: Agente simbiótico
        engine: Motor simbólico reglamental

    Returns:
        Instancia operativa de SymbolicDecisionEngine

    Raises:
        RuntimeError si la inicialización falla
    """
    logger.info("[Decision Init] Inicializando SymbolicDecisionEngine...")

    try:
        decision = SymbolicDecisionEngine(context=context, engine=engine)

        # Validación estructural de interfaz
        if not callable(getattr(decision, "decide", None)):
            raise TypeError("[Decision Init] La clase no implementa método 'decide(context)'.")

        if hasattr(decision, "prioritize") and not callable(decision.prioritize):
            logger.warning("[Decision Init] Método 'prioritize' no es invocable. Revisión sugerida.")

        # Registro estructural en el contexto, si es seguro hacerlo
        if hasattr(context, "symbolic_engine"):
            context.symbolic_engine = decision
            logger.info("[Decision Init] SymbolicDecisionEngine registrado en el contexto.")
        else:
            logger.warning("[Decision Init] El contexto no permite asignar symbolic_engine.")

        # Depuración antes de afirmar hechos simbólicos
        debug_assert_fact_state(context, "decision_engine_ready")

        # Registro simbólico opcional
        if hasattr(context, "assert_fact"):
            context.assert_fact("decision_engine_ready", True)
            context.assert_fact("decision_engine_class", decision.__class__.__name__)
            logger.info("[Decision Init] Hechos simbólicos de decisión afirmados.")

    except Exception as e:
        logger.critical(f"[Decision Init] Fallo crítico al inicializar decisión simbólica: {e}", exc_info=True)
        raise RuntimeError("Inicialización fallida del módulo de decisión.") from e

    logger.info("[Decision Init] Componente de decisión simbólica operativo.")
    return decision
