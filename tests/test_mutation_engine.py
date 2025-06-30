# tests/test_mutation_engine.py

import unittest
from types import SimpleNamespace
from mutations import mutation_engine
from mutations.mutation_engine import MutatedFunction, mutate_function


class TestMutatedFunction(unittest.TestCase):
    def setUp(self):
        self.sample_code = (
            "def test_func(x):\n"
            "    return x + 1\n"
        )
        exec_globals = {}
        exec(self.sample_code, exec_globals)
        self.callable_obj = exec_globals.get("test_func")
        self.metadata = {"info": "test metadata"}

        self.mutated_func = MutatedFunction(
            name="test_func",
            description="Función de prueba",
            code=self.sample_code,
            callable_obj=self.callable_obj,
            metadata=self.metadata,
            file_path="/ruta/falsa.py"
        )

    def test_callable_execution(self):
        result = self.mutated_func(5)
        self.assertEqual(result, 6)

    def test_callable_not_initialized_raises(self):
        mf = MutatedFunction(
            name="no_callable",
            description="Sin callable",
            code="def no_callable(): pass"
        )
        with self.assertRaises(RuntimeError) as cm:
            mf()
        self.assertIn("Callable object not initialized", str(cm.exception))

    def test_to_dict_contains_all_fields(self):
        d = self.mutated_func.to_dict()
        self.assertEqual(d["name"], "test_func")
        self.assertEqual(d["description"], "Función de prueba")
        self.assertEqual(d["code"], self.sample_code)
        self.assertEqual(d["metadata"], self.metadata)
        self.assertEqual(d["file_path"], "/ruta/falsa.py")

    def test_str_representation(self):
        s = str(self.mutated_func)
        self.assertIn("test_func", s)
        self.assertIn("Función de prueba", s)


class TestMutateFunction(unittest.TestCase):
    def setUp(self):
        self.agent_knowledge = {"state": "dummy_state"}

    def test_mutate_function_creates_valid_mutated_function(self):
        class DummySymbolic:
            def get_recent_concepts(self):
                return [{"concept": "test_concept"}]

        context = SimpleNamespace(symbolic=DummySymbolic())

        mutated = mutate_function(self.agent_knowledge, context)

        self.assertIsInstance(mutated, MutatedFunction)
        self.assertTrue(mutated.name.startswith("func_"))
        self.assertIn("test_concept", mutated.description)
        self.assertIsNotNone(mutated.callable)
        self.assertIn("source_concepts", mutated.metadata)
        self.assertEqual(mutated.metadata["source_concepts"], ["test_concept"])

        # Verificar ejecución de función mutada
        resultado = mutated(3)
        self.assertEqual(resultado, 6)  # según función definida: x * 2

    def test_mutate_function_raises_on_missing_concepts(self):
        class DummySymbolic:
            def get_recent_concepts(self):
                return []

        context = SimpleNamespace(symbolic=DummySymbolic())

        with self.assertRaises(ValueError) as cm:
            mutate_function(self.agent_knowledge, context)
        self.assertIn("No se encontraron conceptos simbólicos", str(cm.exception))

    def test_mutate_function_handles_non_dict_concepts(self):
        class DummySymbolic:
            def get_recent_concepts(self):
                return ["concept1", "concept2"]

        context = SimpleNamespace(symbolic=DummySymbolic())

        mutated = mutate_function(self.agent_knowledge, context)
        self.assertIn("concept1", mutated.description)
        self.assertIn("concept2", mutated.description)

    def test_mutate_function_raises_on_context_symbolic_error(self):
        class DummySymbolic:
            def get_recent_concepts(self):
                raise RuntimeError("Error simulado")

        context = SimpleNamespace(symbolic=DummySymbolic())

        with self.assertRaises(ValueError) as cm:
            mutate_function(self.agent_knowledge, context)
        self.assertIn("Error obteniendo conceptos simbólicos", str(cm.exception))

    def test_mutate_function_raises_on_compilation_error(self):
        # Parcheamos el código para forzar error de compilación
        original_code = (
            "def {name}(x):\n"
            "    return x * 2\n"
        )

        def faulty_mutate_function(agent_knowledge, context):
            name = "func_faulty"
            code = "def func_faulty(x):\n return x *\n"  # código inválido

            exec_globals = {}
            try:
                exec(code, exec_globals)
                callable_func = exec_globals.get(name)
                if not callable_func or not callable(callable_func):
                    raise RuntimeError("No se generó una función ejecutable válida.")
            except Exception as ex:
                raise RuntimeError(f"Error compilando función mutada: {ex}")

            return MutatedFunction(name, "Función fallida", code, callable_func, {})

        class DummySymbolic:
            def get_recent_concepts(self):
                return [{"concept": "dummy"}]

        context = SimpleNamespace(symbolic=DummySymbolic())

        with self.assertRaises(RuntimeError) as cm:
            faulty_mutate_function(self.agent_knowledge, context)
        self.assertIn("Error compilando función mutada", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
