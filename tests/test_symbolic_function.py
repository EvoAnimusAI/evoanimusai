import unittest
from autoprogramming.symbolic_function import SymbolicFunction


class TestSymbolicFunction(unittest.TestCase):

    def test_to_dict(self):
        func = SymbolicFunction(
            name="test_func",
            code="def test_func(): pass",
            metadata={"author": "evo"}
        )
        expected = {
            "name": "test_func",
            "code": "def test_func(): pass",
            "metadata": {"author": "evo"}
        }
        self.assertEqual(func.to_dict(), expected)

    def test_from_dict(self):
        data = {
            "name": "init_func",
            "code": "def init_func(): return True",
            "metadata": {"role": "init"}
        }
        func = SymbolicFunction.from_dict(data)
        self.assertEqual(func.name, "init_func")
        self.assertEqual(func.code, "def init_func(): return True")
        self.assertEqual(func.metadata, {"role": "init"})

    def test_repr_format(self):
        func = SymbolicFunction("calc", "def calc(): pass", {"version": "1.0"})
        repr_str = repr(func)
        self.assertIn("SymbolicFunction", repr_str)
        self.assertIn("calc", repr_str)
        self.assertIn("version", repr_str)


if __name__ == "__main__":
    unittest.main()
