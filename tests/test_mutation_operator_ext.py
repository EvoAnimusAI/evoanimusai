import random
import ast
import unittest
from unittest.mock import patch
from autoprogramming import mutation_operator as mo


class MutationOperatorExtendedTests(unittest.TestCase):
    """Cobertura avanzada para bucles for y bloques try/except en mutation_operator."""

    # ------------------------------------------------------------------ #
    # Utilidad interna                                                   #
    # ------------------------------------------------------------------ #
    def _mutate(self, code: str) -> ast.Module:
        """Aplica mutate_function con todas las mutaciones forzadas y
        parchea apply_semantic_mutation como identidad para aislar la prueba."""
        with patch.object(mo, "apply_semantic_mutation", lambda x: x):
            mutated_src = mo.mutate_function(
                code, force_all_mutations=True, rng=random.Random(42)
            )
        return ast.parse(mutated_src)

    # ------------------------------------------------------------------ #
    # Prueba 1: Mutación de bucle for                                    #
    # ------------------------------------------------------------------ #
    def test_for_loop_range_start_changes(self):
        original = """
def loop():
    for i in range(10):
        print(i)
"""
        tree = self._mutate(original)
        # Busca el nodo For
        for_node = next(node for node in ast.walk(tree) if isinstance(node, ast.For))
        self.assertIsInstance(for_node.iter, ast.Call)
        # Extrae valor actual del primer argumento de range()
        new_start = for_node.iter.args[0]
        self.assertIsInstance(new_start, ast.Constant)
        # El valor original era 10; ahora debe estar entre 1 y 5 inclusive
        self.assertNotEqual(new_start.value, 10)
        self.assertIn(new_start.value, range(1, 6))

    # ------------------------------------------------------------------ #
    # Prueba 2: Mutación en bloque try/except/else                       #
    # ------------------------------------------------------------------ #
    def test_try_block_swapped_and_exception_renamed(self):
        original = """
def foo():
    try:
        result = 1 / 0
    except ValueError:
        result = 0
    else:
        result = 1
    return result
"""
        tree = self._mutate(original)
        try_node = next(node for node in ast.walk(tree) if isinstance(node, ast.Try))

        # 1) Verifica que el cuerpo y el else hayan sido intercambiados
        first_body_stmt = try_node.body[0]
        self.assertIsInstance(first_body_stmt, ast.Assign)
        self.assertEqual(ast.unparse(first_body_stmt.targets[0]), "result")
        # El código original tenía result = 1 / 0 en body y result = 1 en else.
        # Tras swap, el body debería contener 'result = 1'
        self.assertEqual(ast.unparse(first_body_stmt.value), "1")

        # 2) Comprueba que el tipo de excepción haya cambiado
        handler = try_node.handlers[0]
        self.assertIsInstance(handler.type, ast.Name)
        self.assertNotEqual(handler.type.id, "ValueError")
        self.assertTrue(handler.type.id.startswith("Exception"))

if __name__ == "__main__":
    import random
    unittest.main()
