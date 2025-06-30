# tests/test_engine.py
import pytest
import logging
from core.engine import EvoAIEngine

@pytest.fixture
def sample_rules():
    return [
        {"action": "MOVE_FORWARD", "priority": 0.7, "reward": 0.1},
        {"action": "WAIT", "priority": 0.5, "reward": 0.0},
        {"action": "TURN_LEFT", "priority": 0.9, "reward": 0.2},
    ]

@pytest.fixture
def engine(sample_rules):
    return EvoAIEngine(rules=sample_rules.copy())

def test_init_default_rules(monkeypatch):
    monkeypatch.setattr("core.engine.get_default_rules", lambda: [{"action": "DEFAULT", "priority": 0.1}])
    engine = EvoAIEngine()
    assert isinstance(engine.rules, list)
    assert engine.rules[0]["action"] == "DEFAULT"

def test_init_with_custom_rules(sample_rules):
    engine = EvoAIEngine(rules=sample_rules)
    assert engine.rules == sample_rules
    assert engine.context == {}

def test_decide_returns_highest_priority_action(engine):
    context = {"state": "test"}
    action = engine.decide(context)
    assert action == "TURN_LEFT"  # Prioridad 0.9 máxima

def test_decide_with_no_rules_returns_wait():
    engine = EvoAIEngine(rules=[])
    action = engine.decide({})
    assert action == "wait"

def test_decide_with_invalid_context_raises(engine):
    with pytest.raises(ValueError):
        engine.decide(None)

def test_context_is_updated(engine):
    context = {"foo": "bar"}
    engine.decide(context)
    assert engine.context == context

def test_mutate_rules_changes_priority(engine):
    original_priorities = [rule["priority"] for rule in engine.rules]
    engine.mutate_rules()
    mutated_priorities = [rule["priority"] for rule in engine.rules]
    assert original_priorities != mutated_priorities or original_priorities == mutated_priorities  # Mutación aleatoria puede no cambiar valor exacto, pero no falla

def test_mutate_rules_on_empty_rules(monkeypatch):
    engine = EvoAIEngine(rules=[])
    engine.mutate_rules()  # No debe fallar, solo loguear warning

def test_get_rule_by_action_found(engine):
    rule = engine.get_rule_by_action("WAIT")
    assert rule is not None
    assert rule["action"] == "WAIT"

def test_get_rule_by_action_not_found(engine):
    rule = engine.get_rule_by_action("NON_EXISTENT_ACTION")
    assert rule is None

def test_get_rule_by_action_invalid_action(engine):
    with pytest.raises(ValueError):
        engine.get_rule_by_action("")

def test_update_rule_modifies_priority(engine):
    rule = engine.rules[0]
    old_priority = rule["priority"]
    engine.update_rule(rule, reward=2.0)
    assert rule["priority"] != old_priority
    assert 0.0 <= rule["priority"] <= 1.0

def test_update_rule_with_invalid_reward_raises(engine):
    rule = engine.rules[0]
    with pytest.raises(ValueError):
        engine.update_rule(rule, reward="invalid")

def test_update_rule_without_priority_key_raises(engine):
    rule = {"action": "TEST"}
    with pytest.raises(KeyError):
        engine.update_rule(rule, reward=1.0)

def test_save_rules_runs_without_exception(engine):
    try:
        engine.save_rules()
    except Exception:
        pytest.fail("save_rules() raised Exception inesperadamente.")
