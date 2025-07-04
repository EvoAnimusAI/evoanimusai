import unittest
import ast
from autoprogramming.semantic_mutation import SemanticMutationBlock, apply_semantic_mutation


class TestSemanticMutation(unittest.TestCase):

    def setUp(self):
        self.mutator = SemanticMutationBlock()

    def _assert_code_equal(self, code1: str, code2: str):
        """
        Compara equivalencia AST entre dos fragmentos de código.
        """
        tree1 = ast.parse(code1, mode='eval')
        tree2 = ast.parse(code2, mode='eval')
        self.assertEqual(ast.dump(tree1), ast.dump(tree2))

    def _apply_mutation_to_expr(self, expr_code):
        tree = ast.parse(expr_code, mode='eval')
        mutated = self.mutator.visit(tree)
        ast.fix_missing_locations(mutated)
        return ast.unparse(mutated).strip()

    def test_add_zero_right(self):
        result = self._apply_mutation_to_expr("x + 0")
        self._assert_code_equal(result, "x")

    def test_add_zero_left(self):
        result = self._apply_mutation_to_expr("0 + x")
        self._assert_code_equal(result, "x")

    def test_mult_one_right(self):
        result = self._apply_mutation_to_expr("x * 1")
        self._assert_code_equal(result, "x")

    def test_mult_one_left(self):
        result = self._apply_mutation_to_expr("1 * x")
        self._assert_code_equal(result, "x")

    def test_add_non_zero(self):
        code = "x + 2"
        result = self._apply_mutation_to_expr(code)
        self._assert_code_equal(result, code)

    def test_mult_non_one(self):
        code = "x * 3"
        result = self._apply_mutation_to_expr(code)
        self._assert_code_equal(result, code)

    def _apply_mutation_to_compare(self, expr_code):
        tree = ast.parse(expr_code, mode='eval')
        mutated = self.mutator.visit(tree)
        ast.fix_missing_locations(mutated)
        return ast.unparse(mutated).strip()

    def test_eq_zero_to_not(self):
        result = self._apply_mutation_to_compare("x == 0")
        self._assert_code_equal(result, "not x")

    def test_noteq_zero_to_bool(self):
        result = self._apply_mutation_to_compare("x != 0")
        self._assert_code_equal(result, "bool(x)")

    def test_eq_non_zero_no_mutation(self):
        code = "x == 1"
        result = self._apply_mutation_to_compare(code)
        self._assert_code_equal(result, code)

    def test_noteq_non_zero_no_mutation(self):
        code = "x != 2"
        result = self._apply_mutation_to_compare(code)
        self._assert_code_equal(result, code)

    def test_non_eq_non_noteq_operator(self):
        code = "x < 0"
        result = self._apply_mutation_to_compare(code)
        self._assert_code_equal(result, code)

    def test_apply_semantic_mutation_code(self):
        code = """
def foo(x):
    return x + 0 == 0
"""
        mutated_code = apply_semantic_mutation(code)
        self.assertIn("return not x", mutated_code)

    def test_apply_semantic_mutation_invalid_code(self):
        invalid_code = "def foo(:"
        mutated = apply_semantic_mutation(invalid_code)
        self.assertEqual(mutated, invalid_code)


if __name__ == "__main__":
    unittest.main()
