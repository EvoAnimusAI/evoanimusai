import unittest
import ast
from unittest.mock import patch
import autoprogramming.mutation_operator as mo


class TestMutationOperator(unittest.TestCase):
    """Pruebas unitarias para autoprogramming.mutation_operator"""

    # ---------- utilidades internas ----------
    def _mutate(self, code: str) -> str:
        """Ejecuta mutate_function con todas las mutaciones forzadas y
        parchea apply_semantic_mutation como identidad para aislar tests."""
        with patch.object(mo, "apply_semantic_mutation", lambda x: x):
            return mo.mutate_function(code, force_all_mutations=True)

    # ---------- tests de helpers -------------
    def test_generate_function_name_format(self):
        name = mo.generate_function_name()
        self.assertTrue(name.startswith("func_") and len(name) == 11)

    def test_generate_class_name_format(self):
        name = mo.generate_class_name()
        self.assertTrue(name.startswith("Class_") and len(name) == 10)

    # ---------- tests de mutación ------------
    def test_mutated_code_is_valid_python(self):
        original = """
def example(x):
    if x > 0:
        return x
    else:
        return -x
"""
        mutated = self._mutate(original)
        # Debe ser código válido
        try:
            ast.parse(mutated)
        except SyntaxError as e:
            self.fail(f"Código mutado inválido:\n{mutated}\nError: {e}")

    def test_function_name_changes(self):
        code = "def target():\n    return 42\n"
        mutated = self._mutate(code)
        self.assertIn("def ", mutated)
        self.assertNotIn("target", mutated)

    def test_class_name_changes(self):
        code = "class Target:\n    pass\n"
        mutated = self._mutate(code)
        self.assertIn("class ", mutated)
        self.assertNotIn("Target", mutated)

    def test_if_condition_negated(self):
        code = """
def foo(x):
    if x > 1:
        return True
    return False
"""
        mutated = self._mutate(code)
        self.assertIn("not", mutated)  # condición negada

    def test_try_except_swapped_and_exception_changed(self):
        code = """
try:
    x = 1 / 0
except ZeroDivisionError:
    x = 0
else:
    x = 1
"""
        mutated = self._mutate(code)
        # Debe contener una nueva Exception personalizada y el bloque else
        self.assertIn("Exception", mutated)
        self.assertIn("else", mutated)


if __name__ == "__main__":
    unittest.main()
