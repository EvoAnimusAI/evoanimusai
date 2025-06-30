# core/context.py
# -*- coding: utf-8 -*-
"""
Contexto simbiótico-evolutivo de EvoAI.
Gestiona el estado interno del sistema, integra agente, entorno, motor simbólico
y ahora también la configuración validada (Config singleton).
"""

from symbolic_ai.symbolic_context import SymbolicContext
from typing import Any, Optional, Tuple, Dict
import copy
from core.config import Config  # Importación directa del singleton de configuración

class EvoContext(SymbolicContext):
    """
    Contexto de ejecución inteligente de EvoAI. Amplía el contexto simbólico
    para incluir agente, motor, entorno, estado y configuración validada.

    Attributes:
        agent: Objeto agente.
        engine: Motor simbólico.
        environment: Entorno físico o simulado.
        state: Estado operacional interno.
        config: Configuración validada cargada desde archivo JSON + entorno.
    """

    MAX_REWARDS_HISTORY = 20

    def __init__(
        self,
        agent: Optional[Any] = None,
        engine: Optional[Any] = None,
        environment: Optional[Any] = None,
    ) -> None:
        super().__init__()
        self.agent = agent
        self.environment = environment
        self.engine = engine  # Referencia opcional al motor simbólico
        self.config = Config.get_instance()  # Inyección automática de configuración

        self.state: Dict[str, Any] = {
            "observation": None,
            "last_action": None,
            "last_decision": None,
            "entropy": 0.0,
            "rewards": [],
        }

    def update(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(observation, dict):
            raise TypeError("La observación debe ser un diccionario.")
        self.state["observation"] = observation
        self.state["entropy"] = observation.get("entropía", 0.0)
        return self.state.copy()

    def decide(self) -> Tuple[Optional[Any], Optional[Any]]:
        observation = self.state.get("observation")
        if observation is None:
            return None, None

        try:
            agent_action = self.agent.decide(observation) if self.agent else None
        except Exception as e:
            print(f"[ERROR] Error en la decisión del agente: {e}")
            agent_action = None

        try:
            symbolic_decision = (
                self.engine.decide(observation)
                if self.engine and callable(getattr(self.engine, "decide", None))
                else None
            )
        except Exception as e:
            print(f"[ERROR] Error en la decisión del motor: {e}")
            symbolic_decision = None

        self.state["last_action"] = agent_action
        self.state["last_decision"] = symbolic_decision

        return agent_action, symbolic_decision

    def record_reward(self, reward: float) -> None:
        if not isinstance(reward, (int, float)):
            raise TypeError("La recompensa debe ser un número.")
        self.state["rewards"].append(reward)
        if len(self.state["rewards"]) > self.MAX_REWARDS_HISTORY:
            self.state["rewards"] = self.state["rewards"][-self.MAX_REWARDS_HISTORY :]

    def get_context(self) -> Dict[str, Any]:
        return copy.deepcopy(self.state)

    def assert_fact(self, key: str, value: Any) -> bool:
        if self.engine is None:
            print("[WARN] No hay motor simbólico para afirmar hechos.")
            return False
        if not callable(getattr(self.engine, "assert_fact", None)):
            print("[ERROR] El motor simbólico no tiene el método 'assert_fact'.")
            return False

        try:
            self.engine.assert_fact(key, value)
            print(f"[INFO] Hecho afirmado: {{{key}: {value}}}")
            return True
        except Exception as e:
            print(f"[ERROR] Fallo al afirmar hecho '{key}': {e}")
            return False

    @property
    def status(self) -> Dict[str, Any]:
        return copy.deepcopy(self.state)
