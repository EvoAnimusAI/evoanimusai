# core/context.py
# -*- coding: utf-8 -*-
"""
Contexto simbiótico-evolutivo de EvoAnimusAI.
Nivel: Militar / Gubernamental / Ultra-secreto
Gestiona el state interno del sistema, integrando:
- Agente autónomo
- Entorno físico/simulado
- Motor simbólico clásico
- Motor de decisión simbólica moderno (symbolic_engine)
- Configuración validada y extendida
"""

import copy
import logging
from typing import Any, Optional, Tuple, Dict
from core.config import Config
from core.context_expander import ContextExpander
from symbolic_ai.symbolic_context import SymbolicContext

logger = logging.getLogger(__name__)

class DummySymbolic:
    def get_recent_concepts(self):
        return []

class EvoContext(SymbolicContext):
    """
    Contexto operativo de EvoAnimusAI.
    """
    MAX_REWARDS_HISTORY = 20

    def __init__(
        self,
        agent: Optional[Any] = None,
        engine: Optional[Any] = None,
        environment: Optional[Any] = None,
        initial_state: Optional[Dict[str, Any]] = None
    ) -> None:
        print("[🧠 CONTEXT] Iniciando EvoContext...")
        super().__init__()
        self.agent = agent
        self.environment = environment
        self.engine = engine  # Motor simbólico clásico
        self.symbolic_engine = None  # Motor simbólico moderno
        self.symbolic = DummySymbolic()
        self.config = Config.get_instance()

        # Estado simbiótico-cognitivo inicial
        self.state: Dict[str, Any] = {
            "observation": None,
            "last_action": None,
            "last_decision": None,
            "entropy": 0.0,
            "rewards": [],
            "symbiotic_progress": None,
        }

        # Integrar initial_state si se pasa
        if initial_state:
            print(f"[🧠 CONTEXT] Cargando estado inicial: {initial_state}")
            self.state.update(initial_state)

        self.extended = ContextExpander(self.state)
        print("[🧠 CONTEXT] Inicialización completa.")

    def update(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(observation, dict):
            raise TypeError("La observación debe ser un diccionario.")
        self.state["observation"] = observation
        self.state["entropy"] = observation.get("entropy", 0.0)
        return self.state.copy()

    def decide(self) -> Tuple[Optional[Any], Optional[Any]]:
        observation = self.state.get("observation")
        if observation is None:
            logger.warning("[decide] Observación nula. Se omite ciclo.")
            return None, None

        try:
            agent_action = self.agent.decide(observation) if self.agent else None
        except Exception as e:
            logger.error(f"[Agent Decision Error] {e}")
            agent_action = None

        symbolic_decision = None
        symbolic_source = self.symbolic_engine or self.engine
        if symbolic_source and callable(getattr(symbolic_source, "decide", None)):
            try:
                symbolic_decision = symbolic_source.decide(observation)
            except Exception as e:
                logger.error(f"[Symbolic Decision Error] {e}")

        self.state["last_action"] = agent_action
        self.state["last_decision"] = symbolic_decision
        return agent_action, symbolic_decision

    def record_reward(self, reward: float) -> None:
        if not isinstance(reward, (int, float)):
            raise TypeError("La recompensa debe ser numérica.")
        self.state["rewards"].append(reward)
        if len(self.state["rewards"]) > self.MAX_REWARDS_HISTORY:
            self.state["rewards"] = self.state["rewards"][-self.MAX_REWARDS_HISTORY:]

    def update_context(self, key: str, value: Any) -> None:
        self.state[key] = value
        print(f"[🧠 CONTEXT] Update: {key} = {value}")

    def get_context(self) -> Dict[str, Any]:
        return copy.deepcopy(self.state)

    def assert_fact(self, key: str, value: Any) -> bool:
        primary = self.symbolic_engine
        fallback = self.engine if primary is not self.engine else None
        for target in (primary, fallback):
            if target is None:
                continue
            if not callable(getattr(target, "assert_fact", None)):
                logger.warning(f"[assert_fact] '{type(target).__name__}' no tiene 'assert_fact'.")
                continue
            try:
                target.assert_fact(key, value)
                logger.info(f"[assert_fact] Hecho afirmado correctamente con {type(target).__name__}: {key} = {value}")
                return True
            except Exception as e:
                logger.error(f"[assert_fact] Error al afirmar {key} con {type(target).__name__}: {e}")

        logger.critical(f"[assert_fact] No se pudo afirmar el hecho: {key} = {value}")
        return False

    @property
    def symbolic_decision_engine(self) -> Optional[Any]:
        return self.symbolic_engine

    @property
    def status(self) -> Dict[str, Any]:
        return copy.deepcopy(self.state)

    def as_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.state.items() if isinstance(k, str)}
