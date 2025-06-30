"""tests/test_strategy_manager.py

Pruebas unitarias para StrategyManager.

Author: Daniel Santiago Ospina Velasquez
"""

import os
import unittest
from unittest.mock import patch, MagicMock, mock_open
from strategies.strategy_manager import StrategyManager

class TestStrategyManager(unittest.TestCase):
    def setUp(self):
        self.manager = StrategyManager(max_strategies=5)

    @patch("strategies.strategy_manager.log_event")
    def test_register_function_adds_strategy(self, mock_log):
        def dummy_func(x): return x
        self.manager.register_function(dummy_func, "dummy", 1.0)
        self.assertEqual(len(self.manager.strategies), 1)
        self.assertEqual(self.manager.strategies[0][0], "dummy")
        mock_log.assert_called_with("STRATEGY_REGISTERED", "dummy (manual)")

    @patch("strategies.strategy_manager.EvoAgent")
    @patch("strategies.strategy_manager.mutate_function")
    @patch("builtins.open", new_callable=mock_open)
    @patch("strategies.strategy_manager.register_mutated_function.register")
    @patch("strategies.strategy_manager.symbolic_context.add_concept")
    @patch("strategies.strategy_manager.log_event")
    def test_generate_new_strategy_success(self, mock_log, mock_add_concept, mock_register_mutated, mock_file, mock_mutate, mock_agent):
        mock_agent.return_value.memory.retrieve_all.return_value = "knowledge"
        mock_agent.return_value.context = "context"
        mutated = MagicMock()
        mutated.name = "mutated_func"
        mutated.description = "def mutated_func(x): return x"
        mock_mutate.return_value = mutated

        result = self.manager.generate_new_strategy()
        self.assertIsNotNone(result)
        name, path = result
        self.assertEqual(name, "mutated_func")
        mock_file.assert_called_once()
        mock_register_mutated.assert_called_once_with("mutated_func", mutated.description)
        mock_add_concept.assert_called_once()
        mock_log.assert_any_call("STRATEGY_CREATED", "mutated_func")

    @patch("strategies.strategy_manager.importlib.util.spec_from_file_location")
    @patch("strategies.strategy_manager.log_event")
    def test_load_strategy_success(self, mock_log, mock_spec):
        mock_loader = MagicMock()

        class DummyModule:
            @staticmethod
            def my_strategy(x): return x
        mock_module = DummyModule()

        mock_spec_obj = MagicMock()
        mock_spec_obj.loader = mock_loader
        mock_spec.return_value = mock_spec_obj

        with patch("strategies.strategy_manager.importlib.util.module_from_spec", return_value=mock_module):
            mock_loader.exec_module = lambda mod: None
            func = self.manager.load_strategy("strategies/my_strategy.py")
            self.assertTrue(callable(func))
            mock_log.assert_any_call("STRATEGY_LOADED", "my_strategy")

    @patch("strategies.strategy_manager.importlib.util.spec_from_file_location")
    def test_load_strategy_missing_function_returns_none(self, mock_spec):
        mock_loader = MagicMock()
        mock_module = MagicMock()

        # No contiene función llamada "unavailable"
        if hasattr(mock_module, "unavailable"):
            delattr(mock_module, "unavailable")

        mock_spec_obj = MagicMock()
        mock_spec_obj.loader = mock_loader
        mock_spec.return_value = mock_spec_obj

        with patch("strategies.strategy_manager.importlib.util.module_from_spec", return_value=mock_module):
            mock_loader.exec_module = lambda mod: None
            func = self.manager.load_strategy("strategies/unavailable.py")
            self.assertIsNone(func)

    def test_evaluate_strategy_returns_score(self):
        def good_func(data):
            return 42.0
        score = self.manager.evaluate_strategy(good_func)
        self.assertEqual(score, 42.0)

    def test_evaluate_strategy_handles_exception(self):
        def bad_func(data):
            raise RuntimeError("fail")
        score = self.manager.evaluate_strategy(bad_func)
        self.assertEqual(score, -10000.0)

    @patch("strategies.strategy_manager.log_event")
    @patch("os.remove")
    def test_prune_removes_low_score_files(self, mock_remove, mock_log):
        self.manager.strategies = [
            ("s1", 10.0, "path1.py"),
            ("s2", 20.0, "path2.py"),
            ("s3", 30.0, "path3.py"),
            ("s4", 40.0, "path4.py"),
            ("s5", 50.0, "path5.py"),
        ]
        with patch("os.path.exists", return_value=True):
            self.manager.prune()
        mock_remove.assert_any_call("path1.py")
        mock_remove.assert_any_call("path2.py")
        survivors = [s[0] for s in self.manager.strategies]
        self.assertIn("s3", survivors)
        self.assertIn("s4", survivors)
        self.assertIn("s5", survivors)
        self.assertNotIn("s1", survivors)
        self.assertNotIn("s2", survivors)
        mock_log.assert_any_call("STRATEGIES_PRUNED", "Supervivientes: 3")

    @patch("strategies.strategy_manager.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("strategies.strategy_manager.log_event")
    def test_save_symbolic_log_writes_file(self, mock_log, mock_file, mock_makedirs):
        self.manager.strategies = [
            ("s1", 10.0, "path1.py"),
            ("s2", 20.5, "path2.py"),
        ]
        self.manager.save_symbolic_log("dummy_log.txt")
        mock_makedirs.assert_called_once()
        mock_file.assert_called_once_with("dummy_log.txt", "w", encoding="utf-8")
        handle = mock_file()
        self.assertTrue(any("s1" in call.args[0] for call in handle.write.call_args_list))
        mock_log.assert_called_with("LOG_SAVED", "Log guardado en dummy_log.txt")

if __name__ == "__main__":
    unittest.main()
