import unittest
from unittest.mock import MagicMock, patch

from runtime.executor import Executor, adapt_rules, fallback_adapt_rules


class TestExecutorAdvance(unittest.TestCase):
    def setUp(self):
        self.agent = MagicMock()
        self.agent.entropy = 0.5
        self.agent.rewards = []
        self.agent.states = []
        self.agent.rejected_mutations = 0
        self.agent.cycles_without_new_rule = 0

        self.context = {"symbiotic_progress": 9, "mutation_chance": 1.0}

        self.engine = MagicMock()
        self.executor = Executor(agent=self.agent, context=self.context, engine=self.engine)
        self.executor._symbolic_step = 0

        self.log_patch = patch('runtime.executor.log_event')
        self.mock_log_event = self.log_patch.start()

    def tearDown(self):
        self.log_patch.stop()

    @patch("runtime.executor.adapt_rules")
    def test_adapt_rules_called_and_progress_reset(self, mock_adapt_rules):
        mock_adapt_rules.return_value = True
        self.context["symbiotic_progress"] = 10

        self.executor._advance()

        mock_adapt_rules.assert_called_once_with(self.executor.engine, self.executor.context)
        self.assertEqual(self.context["symbiotic_progress"], 0)

        self.mock_log_event.assert_any_call("EXECUTOR", "Advancing symbiotically...", level="INFO")
        self.mock_log_event.assert_any_call("ENGINE", "Initiating symbolic rule adaptation...", level="INFO")
        self.mock_log_event.assert_any_call("ENGINE", "Symbolic engine adapted rules successfully.")

    @patch("runtime.executor.fallback_adapt_rules")
    @patch("runtime.executor.adapt_rules", side_effect=Exception("Adaptation failed"))
    def test_fallback_called_when_adapt_rules_raises(self, mock_adapt_rules, mock_fallback):
        self.context["symbiotic_progress"] = 10

        self.executor._advance()

        mock_adapt_rules.assert_called_once_with(self.executor.engine, self.executor.context)
        mock_fallback.assert_called_once_with(self.executor.engine, self.executor.context)
        self.assertEqual(self.context["symbiotic_progress"], 0)

    @patch("runtime.executor.fallback_adapt_rules")
    def test_fallback_called_when_adapt_rules_missing(self, mock_fallback):
        self.context["symbiotic_progress"] = 10

        self.executor.engine = MagicMock()
        delattr(self.executor.engine, "adapt_rules")

        with patch("runtime.executor.adapt_rules", new=None):
            self.executor._advance()
            mock_fallback.assert_called_once_with(self.executor.engine, self.executor.context)
            self.assertEqual(self.context["symbiotic_progress"], 0)

    def test_progress_increment_without_threshold(self):
        self.context["symbiotic_progress"] = 5
        self.executor._advance()

        self.assertEqual(self.context["symbiotic_progress"], 6)

    def test_adapt_rules_functionality(self):
        context = {"mutation_chance": 1.0}

        class DummyEngine:
            def __init__(self):
                self.mutate_rules_called = False

            def mutate_rules(self):
                self.mutate_rules_called = True

        dummy = DummyEngine()
        adapt_rules(dummy, context)

        self.assertTrue(dummy.mutate_rules_called)

    def test_adapt_rules_no_mutation(self):
        context = {"mutation_chance": 0.0}
        dummy = MagicMock()
        adapt_rules(dummy, context)
        dummy.mutate_rules.assert_not_called()

    def test_fallback_adapt_rules_increments_counter(self):
        context = {}
        dummy = MagicMock()
        fallback_adapt_rules(dummy, context)
        self.assertEqual(context["fallback_adapt_counter"], 1)

        fallback_adapt_rules(dummy, context)
        self.assertEqual(context["fallback_adapt_counter"], 2)

    @patch("runtime.executor.log_event")
    def test_execute_action_unknown(self, mock_log):
        result = self.executor._execute_action("acción_desconocida")
        self.assertFalse(result)
        mock_log.assert_any_call("EXECUTOR", "Action 'acción_desconocida' not implemented.", level="WARNING")

    @patch("runtime.executor.log_event")
    def test_execute_action_with_logging_force_exploration(self, mock_log):
        self.executor._previous_action = "mover"
        self.executor._action_repeats = self.executor.ACTION_REPEAT_LIMIT

        self.executor.action_registry.is_valid = MagicMock(return_value=True)
        self.executor.action_registry.get_description = MagicMock(return_value="Descripción")
        self.executor.action_registry.use_action = MagicMock()
        self.executor._execute_action = MagicMock(return_value=True)

        result = self.executor._execute_action_with_logging("mover")
        self.assertTrue(result)
        self.assertTrue(self.executor._force_explore)
        mock_log.assert_any_call("EXECUTOR", "Repeated action 'mover' — forcing exploration.", level="INFO")

    @patch("runtime.executor.log_event")
    def test_execute_action_with_logging_normal(self, mock_log):
        self.executor._previous_action = "mover"
        self.executor._action_repeats = 1

        self.executor.action_registry.is_valid = MagicMock(return_value=True)
        self.executor.action_registry.get_description = MagicMock(return_value="Desc")
        self.executor.action_registry.use_action = MagicMock()
        self.executor._execute_action = MagicMock(return_value=True)

        result = self.executor._execute_action_with_logging("mover")
        self.assertTrue(result)

    @patch("runtime.executor.log_event")
    def test_run_captures_exceptions(self, mock_log):
        self.executor.engine.decide.side_effect = Exception("Falló decisión")
        self.executor.run(steps=1)
        mock_log.assert_any_call("EXECUTOR", "Unexpected error: Falló decisión", level="ERROR")

    def test_run_explore_only(self):
        self.executor.explore_only = True
        self.executor._advance = MagicMock()
        self.executor._symbolic_step = 0
        self.executor.engine.decide = MagicMock(return_value="advance")
        self.executor._execute_action_with_logging = MagicMock(return_value=True)

        self.executor.run(steps=2)
        self.assertEqual(self.executor._execute_action_with_logging.call_count, 2)


if __name__ == "__main__":
    unittest.main()
