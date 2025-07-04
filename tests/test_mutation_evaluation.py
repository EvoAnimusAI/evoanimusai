import unittest
import ast
import os
import json
from unittest.mock import patch
from autoprogramming import mutation_evaluation as me

class MockSymbolicFunction:
    def __init__(self, code):
        self.code = code

    def to_dict(self):
        return {"code": self.code}

    @staticmethod
    def from_dict(data):
        return MockSymbolicFunction(data["code"])

class TestMutationEvaluation(unittest.TestCase):

    def setUp(self):
        # Limpia memoria antes de cada test
        me.memory = {"functions": []}

    def test_valid_code_improvement_true(self):
        func = MockSymbolicFunction("x = 1 + 2")
        with patch("random.choice", return_value=True):
            result = me.evaluate_mutation(func, {})
        self.assertTrue(result)
        self.assertEqual(len(me.memory["functions"]), 1)

    def test_valid_code_improvement_false(self):
        func = MockSymbolicFunction("x = 1 + 2")
        with patch("random.choice", return_value=False):
            result = me.evaluate_mutation(func, {})
        self.assertFalse(result)
        self.assertEqual(len(me.memory["functions"]), 0)

    def test_invalid_code(self):
        func = MockSymbolicFunction("x = (1 +")  # Sintaxis inválida
        result = me.evaluate_mutation(func, {})
        self.assertFalse(result)
        self.assertEqual(len(me.memory["functions"]), 0)

    def test_memory_persistence(self):
        func = MockSymbolicFunction("x = 42")
        me.memory["functions"].append(func)
        me.save_memory(output_dir="tests")
        with open("tests/symbolic_memory.json") as f:
            data = json.load(f)
        self.assertEqual(data["functions"][0]["code"], "x = 42")
        os.remove("tests/symbolic_memory.json")  # limpiar

if __name__ == '__main__':
    unittest.main()
