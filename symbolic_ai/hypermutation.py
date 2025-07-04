# symbolic_ai/hypermutation.py
# -*- coding: utf-8 -*-

import ast
import random
import logging
import time
import hashlib
from typing import Union, Callable, Optional, Dict
import astor  # Compatible con Python < 3.9

logger = logging.getLogger("evoai.hypermutation")
logger.setLevel(logging.INFO)

# Constantes de control
MAX_MUTATIONS_PER_CYCLE = 10
MAX_REPEATED_MUTATIONS = 3
MUTATION_TIME_WINDOW = 60  # segundos

# Estado interno de control
_mutation_counter: Dict[str, int] = {}
_mutation_timestamps: Dict[str, list] = {}
_mutation_history: Dict[str, int] = {}

def _hash_expression(expr: Union[str, ast.AST]) -> str:
    if isinstance(expr, ast.AST):
        expr_str = astor.to_source(expr)
    else:
        expr_str = str(expr)
    return hashlib.sha256(expr_str.encode("utf-8")).hexdigest()

def _can_mutate(expr_hash: str) -> bool:
    now = time.time()

    timestamps = _mutation_timestamps.setdefault(expr_hash, [])
    timestamps = [ts for ts in timestamps if now - ts < MUTATION_TIME_WINDOW]
    _mutation_timestamps[expr_hash] = timestamps

    if len(timestamps) >= MAX_MUTATIONS_PER_CYCLE:
        logger.warning(f"[⛔ Límite] Exceso de mutaciones recientes para {expr_hash}")
        return False

    repeated_count = _mutation_history.get(expr_hash, 0)
    if repeated_count >= MAX_REPEATED_MUTATIONS:
        logger.warning(f"[🛑 Repetición] Mutación excesiva sobre la misma función ({expr_hash})")
        return False

    return True

def hypermutation(expression: Union[str, ast.AST]) -> Optional[str]:
    """
    Aplica una mutación segura a una expresión simbólica (str o AST).
    Reemplaza operadores binarios de forma aleatoria.

    Returns:
        str: Expresión mutada o None si no es posible.
    """
    expr_hash = _hash_expression(expression)
    if not _can_mutate(expr_hash):
        return None

    try:
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
                    logger.info(f"[🧬 Mutación] {original_op.__name__} -> {type(new_op).__name__}")
                    node.op = new_op
                return node

        mutated_tree = MutationTransformer().visit(tree)
        ast.fix_missing_locations(mutated_tree)
        mutated_code = astor.to_source(mutated_tree).strip()

        if not mutated_code:
            logger.warning("[⚠️ Resultado vacío] La mutación no produjo salida.")
            return None

        # Registro exitoso
        _mutation_history[expr_hash] = _mutation_history.get(expr_hash, 0) + 1
        _mutation_timestamps[expr_hash].append(time.time())
        logger.info(f"[✅ Mutación exitosa] Resultado: {mutated_code}")
        return mutated_code

    except Exception as e:
        logger.error(f"[❌ Error] Fallo en hypermutation: {e}")
        return None

class HypermutationEngine:
    """
    Motor envoltorio para mutaciones profundas con control de repetición, límite temporal
    y validación callable.
    """

    @staticmethod
    def mutate_expression(expression: Union[str, ast.AST]) -> Optional[str]:
        return hypermutation(expression)

    @staticmethod
    def mutate_function(func: Callable) -> Optional[Callable]:
        if not callable(func):
            logger.error("[❌ Error] Objeto recibido no es callable")
            return None

        try:
            source = astor.to_source(func)
            mutated_source = hypermutation(source)
            if mutated_source is None:
                return None

            # Compilar y retornar función mutada
            compiled = compile(mutated_source, "<mutated_func>", "eval")
            result = eval(compiled)
            if callable(result):
                logger.info("[✅ Callable mutado correctamente]")
                return result
            else:
                logger.warning("[⚠️ No callable] La mutación produjo un objeto no callable.")
                return None

        except Exception as e:
            logger.error(f"[❌ Error] Fallo al mutar función: {e}")
            return None
