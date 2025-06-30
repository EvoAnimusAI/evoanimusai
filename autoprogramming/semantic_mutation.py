import ast
import astor
import logging

logger = logging.getLogger(__name__)

class SemanticMutationBlock(ast.NodeTransformer):
    """
    Realiza mutaciones semánticas ligeras que preservan el comportamiento pero
    simplifican o transforman expresiones.
    """

    def visit_BinOp(self, node: ast.BinOp):
        self.generic_visit(node)

        # Simplifica x + 0 o 0 + x → x
        if isinstance(node.op, ast.Add):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                logger.debug("[SEMANTIC MUTATION] x + 0 → x")
                return node.left
            if isinstance(node.left, ast.Constant) and node.left.value == 0:
                logger.debug("[SEMANTIC MUTATION] 0 + x → x")
                return node.right

        # Simplifica x * 1 o 1 * x → x
        if isinstance(node.op, ast.Mult):
            if isinstance(node.right, ast.Constant) and node.right.value == 1:
                logger.debug("[SEMANTIC MUTATION] x * 1 → x")
                return node.left
            if isinstance(node.left, ast.Constant) and node.left.value == 1:
                logger.debug("[SEMANTIC MUTATION] 1 * x → x")
                return node.right

        return node

    def visit_Compare(self, node: ast.Compare):
        self.generic_visit(node)

        # Transforma x == 0 → not x
        if (
            isinstance(node.ops[0], ast.Eq) and
            isinstance(node.comparators[0], ast.Constant) and
            node.comparators[0].value == 0
        ):
            logger.debug("[SEMANTIC MUTATION] x == 0 → not x")
            return ast.UnaryOp(op=ast.Not(), operand=node.left)

        # Transforma x != 0 → bool(x)
        if (
            isinstance(node.ops[0], ast.NotEq) and
            isinstance(node.comparators[0], ast.Constant) and
            node.comparators[0].value == 0
        ):
            logger.debug("[SEMANTIC MUTATION] x != 0 → bool(x)")
            return ast.Call(func=ast.Name(id="bool", ctx=ast.Load()), args=[node.left], keywords=[])

        return node


def apply_semantic_mutation(code: str) -> str:
    """
    Aplica mutaciones semánticas al código dado.

    :param code: código Python en string
    :return: código modificado
    """
    try:
        tree = ast.parse(code)
        mutator = SemanticMutationBlock()
        mutated_tree = mutator.visit(tree)
        ast.fix_missing_locations(mutated_tree)
        return astor.to_source(mutated_tree)
    except Exception as e:
        logger.error(f"[❌ SEMANTIC MUTATION ERROR]: {e}", exc_info=True)
        return code
