# symbolic_expression.py

from typing import Any, Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)

class SymbolicExpression:
    """
    Representa una expresión simbólica evaluable, con soporte para estructuras
    tipo árbol (dict) o expresiones textuales tipo regla simbólica.

    Métodos:
        evaluate(context): Evalúa la expresión simbólica en un contexto dado.
        head(): Devuelve el operador principal si es una estructura compuesta.
        body(): Extrae la acción de una expresión textual simbólica.
    """

    def __init__(self, expression: Union[str, int, float, dict]):
        if not isinstance(expression, (str, int, float, dict)):
            raise TypeError("SymbolicExpression must be str, int, float, or dict.")
        self.expression = expression

    def evaluate(self, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Evalúa la expresión simbólica según su estructura.

        - Primitivos: se retornan tal cual.
        - Diccionarios: se asume estructura {'op': str, 'args': list}.
        """
        if isinstance(self.expression, (int, float, str)):
            return self.expression

        if isinstance(self.expression, dict):
            op = self.expression.get("op")
            args = self.expression.get("args", [])

            if not isinstance(args, list):
                logger.warning("Expected 'args' to be a list.")
                return None

            eval_args = [SymbolicExpression(arg).evaluate(context) for arg in args]

            try:
                if op == "add":
                    return sum(eval_args)
                elif op == "mul":
                    result = 1
                    for a in eval_args:
                        result *= a
                    return result
                else:
                    logger.warning(f"Unknown operation '{op}' in symbolic expression.")
            except Exception as e:
                logger.error(f"Evaluation error in symbolic operation '{op}': {e}")
                return None

        logger.warning("Expression structure not recognized.")
        return None

    def head(self) -> Optional[str]:
        """
        Retorna el operador principal de una expresión estructurada.
        """
        if isinstance(self.expression, dict):
            return self.expression.get("op")
        return None

    def body(self) -> Optional[str]:
        """
        Extrae la parte 'acción' de una expresión textual simbólica:
        Ejemplo: ⟦rol:valor⟧ ⇒ acción :: condición
        """
        if isinstance(self.expression, str):
            try:
                parts = self.expression.split('⇒')
                if len(parts) > 1:
                    right = parts[1].strip()
                    action = right.split('::')[0].strip()
                    return action
            except Exception as e:
                logger.error(f"Error parsing body from symbolic text: {e}")
        return None

    def __repr__(self) -> str:
        return f"<SymbolicExpression: {self.expression!r}>"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SymbolicExpression":
        if not isinstance(data, dict):
            raise ValueError("Expected dictionary to create SymbolicExpression.")
        return cls(data)

    @classmethod
    def from_string(cls, expression_str: str) -> "SymbolicExpression":
        if not isinstance(expression_str, str):
            raise ValueError("Expected string to create SymbolicExpression.")
        return cls(expression_str)
