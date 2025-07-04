# tests/test_targeted_mutation.py

import pytest
from metacognition.targeted_mutation import TargetedMutation
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine
from symbolic_ai.symbolic_rule import SymbolicRule


@pytest.fixture
def dummy_context():
    return {
        "entropy": 0.8,
        "error_rate": 0.6,
        "last_action": "explore",
        "mutation_budget": 3
    }


@pytest.fixture
def setup_rules():
    engine = SymbolicRuleEngine(auto_load=False)
    engine.clear_rules()
    rule = SymbolicRule("action", "explore", "move_forward", "entropy > 0.5")
    # Mock: se le añade un atributo 'reward'
    rule.reward = 0.3
    engine.add_rule(rule)
    return engine


def test_evaluate_context_entropy():
    tm = TargetedMutation()
    ctx = {"entropy": 0.9}
    assert tm.evaluate_context(ctx) == "refine_structure"


def test_evaluate_context_error_rate():
    tm = TargetedMutation()
    ctx = {"error_rate": 0.8}
    assert tm.evaluate_context(ctx) == "adjust_thresholds"


def test_evaluate_context_none():
    tm = TargetedMutation()
    ctx = {"error_rate": 0.2, "entropy": 0.3}
    assert tm.evaluate_context(ctx) is None


def test_select_rule_to_mutate_returns_lowest_reward(setup_rules):
    tm = TargetedMutation()
    tm.rule_engine = setup_rules
    rule = tm.select_rule_to_mutate()
    assert isinstance(rule, SymbolicRule)
    assert rule.reward == 0.3


def test_mutate_successful(monkeypatch, setup_rules, dummy_context):
    tm = TargetedMutation()
    tm.rule_engine = setup_rules

    # Parchear método mutate en la regla
    def dummy_mutate(self, mutation_type):
        self.accion = f"{self.accion}_{mutation_type}"
        return True

    monkeypatch.setattr(SymbolicRule, "mutate", dummy_mutate)

    success = tm.mutate(dummy_context)
    assert success is True

    mutated_rule = tm.select_rule_to_mutate()
    assert "refine_structure" in mutated_rule.accion or "adjust_thresholds" in mutated_rule.accion
