import unittest
from autoprogramming.base_symbols import basic_advance

class TestBasicAdvance(unittest.TestCase):

    def test_advance(self):
        obs = {'entropy': 0.3, 'energy': 80}
        self.assertEqual(basic_advance(obs), 'advance')

    def test_wait_high_entropy(self):
        obs = {'entropy': 0.6, 'energy': 80}
        self.assertEqual(basic_advance(obs), 'wait')

    def test_wait_low_energy(self):
        obs = {'entropy': 0.3, 'energy': 40}
        self.assertEqual(basic_advance(obs), 'wait')

    def test_wait_edge_cases(self):
        obs = {'entropy': 0.5, 'energy': 50}
        self.assertEqual(basic_advance(obs), 'wait')

if __name__ == '__main__':
    unittest.main()
