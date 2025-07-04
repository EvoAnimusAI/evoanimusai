# symbolic_ai/decision_module.py
# -*- coding: utf-8 -*-
"""
Módulo de decisión simbólica de EvoAnimusAI.
Clasificación: Militar / Gubernamental / Ultra-secreto

Responsabilidad:
Toma decisiones simbólicas basadas en el contexto, agente y motor lógico simbólico.
Incluye validación de entrada, trazabilidad de decisiones y preparación para refuerzo simbiótico.
"""

import logging
from typing import Any, Optional, Dict

logger = logging.getLogger("EvoAI.SymbolicDecision")


class SymbolicDecisionEngine:
    """
    Componente simbólico responsable de tomar decisiones informadas por contexto y reglas.

    Args:
        context (Any): Contexto simbiótico expandido.
        agent (Any): Instancia del agente EvoAnimusAI.
        engine (Any): Motor simbólico (debe implementar 'decide' y 'prioritize').
    """

    def __init__(self, context: Any, agent: Any, engine: Any) -> None:
        if context is None or agent is None or engine is None:
            raise ValueError("[SymbolicDecisionEngine] Contexto, agente y motor no pueden ser None.")

        required_methods = ["decide", "prioritize"]
        for method in required_methods:
            if not callable(getattr(engine, method, None)):
                raise TypeError(f"[SymbolicDecisionEngine] El motor simbólico debe implementar '{method}'.")

        self.context = context
        self.agent = agent
        self.engine = engine

        logger.info("[✅ SymbolicDecisionEngine] Instanciado con validación completa.")

    def decide(self, observation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Ejecuta lógica simbólica para determinar la mejor action a tomar.

        Args:
            observation (dict): Observaciones del entorno, integradas al contexto si están presentes.

        Returns:
            dict: Estructura de decisión con action propuesta y metadatos de evaluación.
        """
        logger.debug("[🧠 SymbolicDecisionEngine] Iniciando proceso de decisión...")

        try:
            if observation:
                self.context.update_observation(observation)

            # Uso correcto del motor simbólico moderno (decide + prioritize)
            candidate_actions = self.engine.decide(self.context)
            prioritized = self.engine.prioritize(candidate_actions)

            selected = prioritized[0] if prioritized else {"action": "noop", "reason": "no valid options"}

            logger.info(f"[🧠 SymbolicDecisionEngine] Acción seleccionada: {selected}")
            return selected

        except Exception as e:
            logger.error(f"[❌ SymbolicDecisionEngine] Error durante decisión simbólica: {e}")
            return {"decision": "error", "reason": str(e)}
