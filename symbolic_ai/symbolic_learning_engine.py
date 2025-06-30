import logging
from typing import Dict, List, Optional, Any, Set, Tuple, Protocol

logger = logging.getLogger(__name__)


class RuleEngineInterface(Protocol):
    """
    Interfaz del motor de reglas simbólicas.
    Permite inyectar motores personalizados en entornos seguros o testeables.
    """

    def evaluate(self, context: Dict[str, Any]) -> List[Any]: ...
    def add_rule(self, rule: Any) -> None: ...
    def remove_rule(self, rule: Any) -> None: ...


class SymbolicLearningEngine:
    """
    Núcleo de Aprendizaje Simbólico de EvoAI.

    Este módulo es responsable de:
    - Analizar observaciones simbólicas.
    - Aprender reglas desde refuerzo o patrones.
    - Interactuar con un motor simbólico (inyectado) para evaluación y aplicación.
    """

    def __init__(self, rule_engine: Optional[RuleEngineInterface] = None):
        if rule_engine is None:
            raise ValueError("El parámetro 'rule_engine' es obligatorio para entornos de auditoría.")
        self.rule_engine = rule_engine

        self.reinforcement_history: Dict[Tuple[str, str], List[float]] = {}
        self.generated_rules: Set[Tuple[str, str]] = set()
        logger.debug("[Init] SymbolicLearningEngine inicializado con rule_engine: %s", type(rule_engine).__name__)

    def observe(self, observation: Dict[str, Any]) -> None:
        """
        Procesa una observación simbólica.
        """
        logger.info("[Observe] Observación recibida: %s", observation)
        # Lógica de observación futura aquí

    def register_concept(self, concept: str, source: str = "unknown") -> None:
        """
        Registra un concepto simbólico.
        """
        self.generated_rules.add((concept, source))
        logger.info("[RegisterConcept] Concepto registrado: %s (fuente: %s)", concept, source)

    def apply_rules(self, context: Dict[str, Any]) -> List[str]:
        """
        Aplica las reglas simbólicas usando el motor inyectado.

        Returns:
            List[str]: Resultados textuales de las acciones evaluadas.
        """
        logger.debug("[ApplyRules] Contexto de evaluación recibido: %s", context)
        resultado = self.rule_engine.evaluate(context)
        acciones = [r.texto for r in resultado if hasattr(r, "texto")]
        logger.info("[ApplyRules] Resultado: %s", acciones)
        return acciones

    def add_rule(self, rule: Any) -> None:
        """
        Añade una regla simbólica al motor.
        """
        logger.info("[AddRule] Agregando regla al motor: %s", rule)
        self.rule_engine.add_rule(rule)

    def export_state(self) -> Dict[str, Any]:
        """
        Exporta el estado interno para snapshot, trazabilidad o persistencia.

        Returns:
            Dict[str, Any]: Estado serializable.
        """
        state = {
            "reinforcement_history": dict(self.reinforcement_history),
            "generated_rules": list(self.generated_rules),
            "engine_type": type(self.rule_engine).__name__
        }
        logger.debug("[ExportState] Estado exportado: %s", state)
        return state
