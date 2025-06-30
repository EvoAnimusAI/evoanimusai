# tests/test_rule_adaptation.py

import unittest
from unittest.mock import MagicMock, patch
from runtime import rule_adaptation


class TestRuleAdaptation(unittest.TestCase):

    @patch("runtime.rule_adaptation.random.random")
    def test_adapt_rules_with_mutation(self, mock_random):
        engine = MagicMock()
        engine.mutate_rules = MagicMock()
        context = {"mutation_chance": 1.0}  # fuerza la mutación
        mock_random.return_value = 0.0

        result = rule_adaptation.adapt_rules(engine, context)

        self.assertTrue(result)
        engine.mutate_rules.assert_called_once()

    @patch("runtime.rule_adaptation.random.random")
    def test_adapt_rules_no_mutation_due_to_chance(self, mock_random):
        engine = MagicMock()
        engine.mutate_rules = MagicMock()
        context = {"mutation_chance": 0.0}  # evita mutación
        mock_random.return_value = 1.0

        result = rule_adaptation.adapt_rules(engine, context)

        self.assertFalse(result)
        engine.mutate_rules.assert_not_called()

    @patch("runtime.rule_adaptation.random.random")
    def test_adapt_rules_mutation_fails_gracefully(self, mock_random):
        engine = MagicMock()
        engine.mutate_rules.side_effect = Exception("Boom")
        context = {"mutation_chance": 1.0}
        mock_random.return_value = 0.0

        result = rule_adaptation.adapt_rules(engine, context)

        self.assertFalse(result)
        engine.mutate_rules.assert_called_once()

    @patch("runtime.rule_adaptation.random.random")
    def test_adapt_rules_without_mutate_rules_method(self, mock_random):
        engine = object()  # sin mutate_rules
        context = {"mutation_chance": 1.0}
        mock_random.return_value = 0.0

        result = rule_adaptation.adapt_rules(engine, context)

        self.assertFalse(result)

    def test_fallback_adapt_rules_increments_counter(self):
        engine = MagicMock()
        context = {}

        rule_adaptation.fallback_adapt_rules(engine, context)
        self.assertEqual(context.get("fallback_adapt_counter"), 1)

        rule_adaptation.fallback_adapt_rules(engine, context)
        self.assertEqual(context.get("fallback_adapt_counter"), 2)
