import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class SymbolicEvaluator:
    """
    Clase para evaluar reglas simbólicas expresadas en texto.
    
    Las reglas deben tener el formato:
        "⟦rol:valor⟧ ⇒ action :: condición"
    
    Donde 'condición' es una expresión lógica evaluable sobre el contexto dado.
    """
    def __init__(self, rule_text: str):
        if not isinstance(rule_text, str) or not rule_text.strip():
            raise ValueError("rule_text debe ser un string no vacío.")
        self.rule_text = rule_text.strip()

    def evaluate(self, context: Dict[str, Any]) -> bool:
        """
        Evalúa la condición de la regla en el contexto proporcionado.

        Args:
            context (Dict[str, Any]): Diccionario con variables disponibles para la evaluación.

        Returns:
            bool: Resultado de la evaluación.
        """
        condition = self.extract_condition()
        if not condition:
            logger.warning("No se encontró condición en la regla, devolviendo False.")
            return False

        try:
            # Evaluación segura: Aquí se puede reemplazar por motor simbólico/AST
            # Actualmente evalúa solo expresiones lógicas básicas.
            # Usar eval con precaución: el contexto debe estar controlado.
            result = eval(condition, {"__builtins__": None}, context)
            if not isinstance(result, bool):
                logger.warning(f"Evaluación no retornó bool, retornando False. Resultado: {result}")
                return False
            return result
        except Exception as e:
            logger.error(f"Error evaluando condición '{condition}': {e}")
            return False

    def extract_condition(self) -> str:
        """
        Extrae la condición lógica desde el texto de la regla.

        Returns:
            str: La condición como string o cadena vacía si no existe.
        """
        parts = self.rule_text.split("::")
        if len(parts) == 2:
            return parts[1].strip()
        logger.debug(f"Regla sin condición válida: '{self.rule_text}'")
        return ""
