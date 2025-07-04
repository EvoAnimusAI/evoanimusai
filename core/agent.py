# core/agent.py

import logging
import random
from math import log2
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from core.memory import AgentMemory  # ✅ CORREGIDO: usamos AgentMemory

logger = logging.getLogger(__name__)


@runtime_checkable
class ContextProtocol(Protocol):
    def assert_fact(self, key: str, value: Any) -> None: ...
    def update(self, data: Dict[str, Any]) -> None: ...


class EvoAgent:
    def __init__(self, context: Optional[ContextProtocol] = None, name: str = "EvoAgent") -> None:
        self.name = name
        self.context = context
        self.memory = AgentMemory()  # ✅ CORREGIDO: asignación explícita
        self.entropy: float = 0.0
        self.rewards: List[float] = []
        self.states: List[Dict[str, Any]] = []
        self.observation_history: List[Dict[str, Any]] = []
        self.rejected_mutations: int = 0
        self.cycles_without_new_rule: int = 0

        logger.info(f"[{self.name}] Inicializado. Contexto: {'asignado' if context else 'no asignado'}.")

        if self.context and not isinstance(self.context, ContextProtocol):
            logger.warning(f"[{self.name}] El contexto no cumple con el protocolo esperado.")

        if self.context:
            try:
                self.assert_fact("agent_name", self.name)
                logger.info(f"[{self.name}] Identidad simbólica registrada.")
            except Exception as e:
                logger.error(f"[{self.name}] Error registrando identidad simbólica: {e}")

    def assert_fact(self, key: str, value: Any) -> None:
        if not self.context:
            logger.error(f"[{self.name}] No hay contexto asignado para afirmar hecho: {key} = {value}")
            return
        if not hasattr(self.context, "assert_fact") or not callable(getattr(self.context, "assert_fact")):
            logger.error(f"[{self.name}] Contexto no implementa método 'assert_fact'. No se puede afirmar: {key} = {value}")
            return
        try:
            self.context.assert_fact(key, value)
            logger.info(f"[{self.name}] Hecho afirmado: {key} = {value}")
        except Exception as e:
            logger.error(f"[{self.name}] Error afirmando hecho '{key}': {e}")

    def perceive(self, observation: Dict[str, Any]) -> None:
        if not isinstance(observation, dict):
            raise TypeError("Observation must be a dictionary")

        sanitized = self._sanitize_observation(observation)

        if self.context:
            if "pos" in sanitized:
                self.assert_fact("position", sanitized["pos"])
            try:
                self.context.update(sanitized)
            except Exception as e:
                logger.error(f"[{self.name}] Error actualizando contexto: {e}")
        else:
            logger.warning(f"[{self.name}] No hay contexto asignado; la observación no se integra.")

        self.observation_history.append(sanitized)
        logger.info(f"[{self.name}] Contexto actualizado con: {sanitized}")

    def _sanitize_observation(self, observation: Dict[Any, Any]) -> Dict[str, Any]:
        sanitized = {}
        for key, value in observation.items():
            if not isinstance(key, str):
                logger.warning(f"[{self.name}] Clave inválida en observación (no str): {key}")
                continue
            if not isinstance(value, (int, float, str, bool, type(None))):
                logger.warning(f"[{self.name}] Valor inválido en observación para '{key}': {value}")
                continue
            sanitized[key] = value
        return sanitized

    def decide(self, observation: Dict[str, Any]) -> str:
        logger.info(f"[{self.name}] Observación recibida para decisión: {observation}")
        possible_actions = ["explore", "wait", "calm", "advance"]
        action = random.choice(possible_actions)
        logger.info(f"[{self.name}] Acción decidida: {action}")
        self.states.append(observation)
        return action

    def learn(self, observation: Dict[str, Any], action: str, reward: float) -> None:
        logger.info(f"[{self.name}] Aprendiendo -> Obs: {observation}, Acción: {action}, Recompensa: {reward}")
        self.rewards.append(reward)
        if len(self.rewards) > 1:
            self.entropy = self._calculate_entropy()
            logger.info(f"[{self.name}] Entropía actualizada: {self.entropy:.4f}")

    def _calculate_entropy(self) -> float:
        recent_rewards = self.rewards[-10:]
        freq = {}
        for r in recent_rewards:
            freq[r] = freq.get(r, 0) + 1
        total = len(recent_rewards)
        entropy = 0.0
        for count in freq.values():
            p = count / total
            entropy -= p * log2(p)
        return entropy
