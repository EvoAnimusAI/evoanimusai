# symbolic_ai/hypermutation.py

import ast
import random
import logging
from typing import Union
import astor  # Compatible con Python < 3.9

logger = logging.getLogger("evoai.hypermutation")
logger.setLevel(logging.INFO)


def hypermutation(expression: Union[str, ast.AST]) -> Union[str, None]:
    """
    Aplica una mutación segura a una expresión simbólica en forma de string o AST.

    La mutación reemplaza operadores binarios con otros al azar compatibles.

    Args:
        expression (Union[str, ast.AST]): Expresión simbólica a mutar.

    Returns:
        Union[str, None]: Expresión mutada como string, o None si falla.
    """
    try:
        # Convertir string a AST si es necesario
        if isinstance(expression, str):
            logger.info(f"[⚡ Hypermutation] Parsing expresión: {expression}")
            tree = ast.parse(expression, mode='eval')
        elif isinstance(expression, ast.AST):
            logger.info(f"[⚡ Hypermutation] Usando AST provisto directamente")
            tree = expression
        else:
            raise TypeError("La expresión debe ser str o ast.AST")

        class MutationTransformer(ast.NodeTransformer):
            def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
                self.generic_visit(node)
                original_op = type(node.op)
                available_ops = [ast.Add, ast.Sub, ast.Mult, ast.Div]
                if original_op in available_ops:
                    available_ops.remove(original_op)
                    new_op = random.choice(available_ops)()
                    logger.info(f"[🧬 Mutación] Reemplazando operador {original_op.__name__} -> {type(new_op).__name__}")
                    node.op = new_op
                return node

        mutated_tree = MutationTransformer().visit(tree)
        ast.fix_missing_locations(mutated_tree)

        mutated_code = astor.to_source(mutated_tree).strip()
        logger.info(f"[✅ Resultado] Expresión mutada: {mutated_code}")
        return mutated_code

    except Exception as e:
        logger.error(f"[❌ Error] Fallo en hypermutation: {e}")
        return None


class HypermutationEngine:
    """
    Clase envoltorio para la función de mutación hipermutativa,
    para facilitar integración y posible extensión futura.
    """

    @staticmethod
    def mutate(expression: Union[str, ast.AST]) -> Union[str, None]:
        return hypermutation(expression)
