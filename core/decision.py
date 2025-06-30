import logging
from typing import Optional, Any

from core.engine import SymbolicEngine

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class DecisionEngine:
    """
    Motor de decisiones que actúa como interfaz entre el sistema EvoAI y el motor simbólico.
    Evalúa el contexto y decide qué acción seguir.

    Attributes:
        engine (SymbolicEngine): Motor simbólico para razonamiento y manipulación de reglas.
    """

    def __init__(self, symbolic_context: Optional[SymbolicEngine] = None) -> None:
        """
        Inicializa el motor de decisiones con un contexto simbólico.
        Si no se proporciona, crea una instancia por defecto de SymbolicEngine.

        Args:
            symbolic_context (Optional[SymbolicEngine]): Contexto simbólico para razonamiento.
        """
        if symbolic_context is not None:
            # Verificar interfaz básica requerida en vez de instancia estricta
            required_methods = ['decide', 'get_rule_by_action', 'update_rule', 'mutate_rules', 'save_rules']
            if not all(callable(getattr(symbolic_context, method, None)) for method in required_methods):
                raise TypeError("symbolic_context debe implementar la interfaz requerida de SymbolicEngine o ser None.")
        self.engine = symbolic_context or SymbolicEngine()
        logger.info("[🧠 DecisionEngine] Inicializado con contexto simbólico.")

    def decide(self, context: Any) -> Any:
        if context is None:
            raise ValueError("El contexto para decidir no puede ser None.")
        logger.debug("[🧠 DecisionEngine] Analizando contexto para tomar decisión...")
        try:
            action = self.engine.decide(context)
            logger.info(f"[🧠 DecisionEngine] Acción decidida: {action}")
            return action
        except Exception as e:
            logger.error(f"[ERROR] Fallo en DecisionEngine.decide: {e}")
            raise RuntimeError(f"Fallo en DecisionEngine.decide: {e}")

    def update(self, action: Any, reward: float) -> None:
        if not isinstance(reward, (int, float)):
            raise ValueError("La recompensa debe ser un número.")
        logger.debug(f"[🧠 DecisionEngine] Actualizando motor con acción {action} y recompensa {reward}")
        try:
            rule = self.engine.get_rule_by_action(action)
            if rule:
                self.engine.update_rule(rule, reward)
                logger.info(f"[🧠 DecisionEngine] Regla actualizada con recompensa {reward}")
            else:
                logger.warning("[🧠 DecisionEngine] No se encontró regla para la acción proporcionada.")
        except Exception as e:
            logger.error(f"[ERROR] Fallo en DecisionEngine.update: {e}")
            raise RuntimeError(f"Fallo en DecisionEngine.update: {e}")

    def mutate(self) -> None:
        logger.debug("[🧠 DecisionEngine] Ejecutando mutación de reglas.")
        try:
            self.engine.mutate_rules()
            logger.info("[🧠 DecisionEngine] Mutación ejecutada exitosamente.")
        except Exception as e:
            logger.error(f"[ERROR] Fallo en DecisionEngine.mutate: {e}")
            raise RuntimeError(f"Fallo en DecisionEngine.mutate: {e}")

    def save(self) -> None:
        logger.debug("[🧠 DecisionEngine] Guardando reglas simbólicas.")
        try:
            self.engine.save_rules()
            logger.info("[🧠 DecisionEngine] Reglas guardadas exitosamente.")
        except Exception as e:
            logger.error(f"[ERROR] Fallo en DecisionEngine.save: {e}")
            raise RuntimeError(f"Fallo en DecisionEngine.save: {e}")
