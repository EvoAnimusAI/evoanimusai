import pytest
from unittest.mock import MagicMock, patch
import runtime.rule_adaptation as rule_adaptation


# ----------------------------------------------------------------------
# adapt_rules
# ----------------------------------------------------------------------
def test_adapt_rules_mutation_performed():
    engine = MagicMock()
    engine.mutate_rules = MagicMock()

    context = {"mutation_chance": 1.0}          # garantiza intento de mutación
    with patch("random.random", return_value=0.0), \
         patch("runtime.rule_adaptation.log_event"):          # silencia log
        result = rule_adaptation.adapt_rules(engine, context)

    engine.mutate_rules.assert_called_once()
    assert result is True


def test_adapt_rules_mutate_rules_raises():
    engine = MagicMock()
    engine.mutate_rules.side_effect = RuntimeError("fail")

    context = {"mutation_chance": 1.0}
    with patch("random.random", return_value=0.0), \
         patch("runtime.rule_adaptation.log_event"):
        result = rule_adaptation.adapt_rules(engine, context)

    engine.mutate_rules.assert_called_once()
    assert result is False


def test_adapt_rules_no_mutate_method():
    engine = MagicMock()
    # Elimina mutate_rules para simular motor sin soporte
    if hasattr(engine, "mutate_rules"):
        delattr(engine, "mutate_rules")

    context = {"mutation_chance": 1.0}
    with patch("random.random", return_value=0.0), \
         patch("runtime.rule_adaptation.log_event"):
        result = rule_adaptation.adapt_rules(engine, context)

    assert result is False


def test_adapt_rules_no_mutation_chance_met():
    engine = MagicMock()
    engine.mutate_rules = MagicMock()

    context = {"mutation_chance": 0.0}          # nunca mutará
    with patch("random.random", return_value=1.0), \
         patch("runtime.rule_adaptation.log_event"):
        result = rule_adaptation.adapt_rules(engine, context)

    engine.mutate_rules.assert_not_called()
    assert result is False


# ----------------------------------------------------------------------
# fallback_adapt_rules
# ----------------------------------------------------------------------
def test_fallback_adapt_rules_increments_counter():
    engine = MagicMock()
    context = {}

    with patch("runtime.rule_adaptation.log_event"):
        rule_adaptation.fallback_adapt_rules(engine, context)
        rule_adaptation.fallback_adapt_rules(engine, context)

    assert context["fallback_adapt_counter"] == 2
