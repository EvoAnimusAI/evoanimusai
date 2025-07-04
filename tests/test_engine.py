import pytest
from unittest.mock import MagicMock, patch
from core.engine import EvoAIEngine, RuleEngineAdapter

@pytest.fixture
def sample_rules():
    return [
        {"action": "act1", "priority": 0.5},
        {"action": "act2", "priority": 0.7}
    ]

def test_rule_engine_adapter_evaluate(sample_rules):
    adapter = RuleEngineAdapter(sample_rules)
    context = {"some_key": "some_value"}
    results = adapter.evaluate(context)
    assert isinstance(results, list)
    assert all("action" in r and "priority" in r and "confidence" in r for r in results)

def test_rule_engine_adapter_add_remove_rule(sample_rules):
    adapter = RuleEngineAdapter(sample_rules.copy())
    new_rule = {"action": "act3", "priority": 0.9}
    adapter.add_rule(new_rule)
    assert any(r["action"] == "act3" for r in adapter.rules)
    adapter.remove_rule(new_rule)
    assert all(r["action"] != "act3" for r in adapter.rules)

def test_evoai_engine_init(sample_rules):
    engine = EvoAIEngine(sample_rules)
    assert engine.rules == sample_rules
    assert hasattr(engine, "learning_engine")
    assert hasattr(engine, "entropy_controller")

def test_heuristic_decide_returns_valid_action(sample_rules):
    engine = EvoAIEngine(sample_rules)
    context = {"entropy": 0.0}
    decision = engine.heuristic_decide(context)
    assert "action" in decision
    assert "priority" in decision
    assert "source" in decision

def test_heuristic_decide_raises_type_error_on_bad_context(sample_rules):
    engine = EvoAIEngine(sample_rules)
    with pytest.raises(TypeError):
        engine.heuristic_decide("not a dict")

def test_mutate_rules_changes_priority(sample_rules):
    engine = EvoAIEngine(sample_rules.copy())
    old_priorities = [r["priority"] for r in engine.rules]
    engine.mutate_rules()
    new_priorities = [r["priority"] for r in engine.rules]
    assert any(o != n for o, n in zip(old_priorities, new_priorities))

def test_learn_calls_subcomponents(sample_rules):
    engine = EvoAIEngine(sample_rules)
    engine.learning_engine.reinforce = MagicMock()
    engine.entropy_controller.update_entropy_change = MagicMock()
    engine.learn({"obs":1}, "act1", 0.8)
    engine.learning_engine.reinforce.assert_called_once_with("act1", 0.8)
    engine.entropy_controller.update_entropy_change.assert_called_once_with(0.8)

def test_get_rule_by_action(sample_rules):
    engine = EvoAIEngine(sample_rules)
    rule = engine.get_rule_by_action("act1")
    assert rule is not None
    assert rule["action"] == "act1"
    assert engine.get_rule_by_action("nonexistent") is None

def test_update_rule_priority_adjustment(sample_rules):
    engine = EvoAIEngine(sample_rules.copy())
    new_rule = {"action": "act1", "alpha": 0.2}
    old_priority = engine.rules[0]["priority"]
    engine.update_rule(new_rule, reward=0.8)
    updated_priority = engine.rules[0]["priority"]
    assert 0 <= updated_priority <= 1
    assert updated_priority != old_priority

def test_update_rule_raises_value_error_on_missing_action(sample_rules):
    engine = EvoAIEngine(sample_rules)
    with pytest.raises(ValueError):
        engine.update_rule({"priority": 0.5})

def test_prioritize_orders_rules_by_confidence():
    rules = [
        {"action": "a", "confidence": 0.3},
        {"action": "b", "confidence": 0.7},
        {"action": "c", "confidence": 0.5},
    ]
    engine = EvoAIEngine([])
    ordered = engine.prioritize(rules)
    assert ordered[0]["confidence"] == 0.7
    assert ordered[-1]["confidence"] == 0.3

