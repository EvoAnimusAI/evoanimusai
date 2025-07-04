import unittest
from autoprogramming.directed_mutation import mutate_parent_function

class MockSymbolicFunction:
    def __init__(self, pasos):
        self.pasos = pasos

    def __deepcopy__(self, memo):
        # Simula un deepcopy manual
        return MockSymbolicFunction([p.copy() for p in self.pasos])

class TestDirectedMutation(unittest.TestCase):

    def test_mutation_with_preferred_topic(self):
        original = MockSymbolicFunction([{"accion": "mover", "param": 1.0}])
        mutated = mutate_parent_function(original, {}, temas_preferidos=["mover"])
        self.assertNotEqual(mutated.pasos[0]["param"], 1.0)

    def test_mutation_without_preferred_topic(self):
        original = MockSymbolicFunction([{"accion": "detener", "param": 2.0}])
        mutated = mutate_parent_function(original, {}, temas_preferidos=["avanzar"])
        self.assertNotEqual(mutated.pasos[0]["param"], 2.0)

    def test_mutation_without_preference(self):
        original = MockSymbolicFunction([{"accion": "girar", "param": 0.0}])
        mutated = mutate_parent_function(original, {}, temas_preferidos=None)
        self.assertNotEqual(mutated.pasos[0]["param"], 0.0)

    def test_no_steps(self):
        original = MockSymbolicFunction([])
        mutated = mutate_parent_function(original, {}, temas_preferidos=["cualquier"])
        self.assertEqual(mutated.pasos, [])

if __name__ == '__main__':
    unittest.main()
