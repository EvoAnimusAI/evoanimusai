import ast
import astor
import random
import string
import logging
from typing import Optional

from autoprogramming.semantic_mutation import apply_semantic_mutation  # ✅ INTEGRACIÓN

logger = logging.getLogger(__name__)

def generate_function_name(rng: Optional[random.Random] = None) -> str:
    rng = rng or random
    return "func_" + ''.join(rng.choices(string.ascii_lowercase, k=6))

def generate_class_name(rng: Optional[random.Random] = None) -> str:
    rng = rng or random
    return "Class_" + ''.join(rng.choices(string.ascii_uppercase, k=4))

class MutationBlock(ast.NodeTransformer):
    def __init__(self, rng: Optional[random.Random] = None, force_all_mutations: bool = False):
        super().__init__()
        self.rng = rng or random
        self.force_all = force_all_mutations

    def _should_mutate(self) -> bool:
        return self.force_all or self.rng.random() < 0.5

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        if self._should_mutate():
            old_name = node.name
            node.name = generate_function_name(self.rng)
            logger.debug(f"[MUTATION] Function name changed from '{old_name}' to '{node.name}'")
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        if self._should_mutate():
            old_name = node.name
            node.name = generate_class_name(self.rng)
            logger.debug(f"[MUTATION] Class name changed from '{old_name}' to '{node.name}'")
        self.generic_visit(node)
        return node

    def visit_If(self, node: ast.If) -> ast.If:
        if self._should_mutate():
            node.test = ast.UnaryOp(op=ast.Not(), operand=node.test)
            logger.debug("[MUTATION] If condition negated")
        self.generic_visit(node)
        return node

    def visit_For(self, node: ast.For) -> ast.For:
        if self._should_mutate():
            if (
                isinstance(node.iter, ast.Call) and
                isinstance(node.iter.func, ast.Name) and
                node.iter.func.id == "range" and
                len(node.iter.args) > 0
            ):
                old_value = astor.to_source(node.iter.args[0]).strip()
                new_value = self.rng.randint(1, 5)
                node.iter.args[0] = ast.Constant(value=new_value)
                logger.debug(f"[MUTATION] For loop start changed from {old_value} to {new_value}")
        self.generic_visit(node)
        return node

    def visit_While(self, node: ast.While) -> ast.While:
        if self._should_mutate():
            node.test = ast.UnaryOp(op=ast.Not(), operand=node.test)
            logger.debug("[MUTATION] While condition negated")
        self.generic_visit(node)
        return node

    def visit_Try(self, node: ast.Try) -> ast.Try:
        if self._should_mutate():
            if node.body and node.orelse:
                node.body, node.orelse = node.orelse, node.body
                logger.debug("[MUTATION] Try body and else block swapped")
            for handler in node.handlers:
                if isinstance(handler.type, ast.Name):
                    old_type = handler.type.id
                    new_type = "Exception" + ''.join(self.rng.choices(string.ascii_uppercase, k=3))
                    handler.type.id = new_type
                    logger.debug(f"[MUTATION] Exception type changed from '{old_type}' to '{new_type}'")
        self.generic_visit(node)
        return node


def mutate_function(original_code: str, rng: Optional[random.Random] = None, force_all_mutations: bool = False) -> str:
    rng = rng or random
    try:
        tree = ast.parse(original_code)
        mutator = MutationBlock(rng=rng, force_all_mutations=force_all_mutations)
        mutated_tree = mutator.visit(tree)
        ast.fix_missing_locations(mutated_tree)
        syntactic_code = astor.to_source(mutated_tree)

        # 🔁 Aplicar mutación semántica como segunda fase
        semantically_mutated_code = apply_semantic_mutation(syntactic_code)
        return semantically_mutated_code

    except Exception as e:
        logger.error(f"[❌ MUTATION ERROR]: {e}", exc_info=True)
        return original_code
