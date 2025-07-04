import pytest
from unittest.mock import MagicMock
from core.decision import DecisionEngine
from symbolic_ai.symbolic_decision_engine import SymbolicDecisionEngine

class DummySymbolicEngine:
    def decide(self):
        return {"action": "dummy_action"}

    def get_rule_by_action(self, action):
        if action == {"action": "dummy_action"}:
            return {"rule": "dummy_rule"}
        return None

    def update_rule(self, rule, reward):
        pass

    def mutate_rules(self):
        pass

    def save_rules(self):
        pass

def test_init_with_symbolic_context():
    dummy_engine = DummySymbolicEngine()
    engine = DecisionEngine(symbolic_context=dummy_engine)
    assert engine.engine == dummy_engine

def test_init_without_context_raises():
    with pytest.raises(ValueError):
        DecisionEngine()

def test_init_with_invalid_symbolic_context():
    with pytest.raises(TypeError):
        DecisionEngine(symbolic_context=object())

def test_decide_returns_action():
    dummy_engine = DummySymbolicEngine()
    engine = DecisionEngine(symbolic_context=dummy_engine)
    result = engine.decide()
    assert result == {"action": "dummy_action"}

def test_decide_raises_on_error():
    class BadEngine(DummySymbolicEngine):
        def decide(self):
            raise Exception("fail")

    engine = DecisionEngine(symbolic_context=BadEngine())
    with pytest.raises(RuntimeError):
        engine.decide()

def test_update_calls_update_rule():
    dummy_engine = DummySymbolicEngine()
    dummy_engine.update_rule = MagicMock()
    dummy_engine.get_rule_by_action = MagicMock(return_value={"rule": "r"})
    engine = DecisionEngine(symbolic_context=dummy_engine)
    engine.update({"action": "dummy_action"}, 5.0)
    dummy_engine.update_rule.assert_called_once_with({"rule": "r"}, 5.0)

def test_update_warns_no_rule(monkeypatch):
    dummy_engine = DummySymbolicEngine()
    dummy_engine.get_rule_by_action = MagicMock(return_value=None)
    engine = DecisionEngine(symbolic_context=dummy_engine)
    # Patch logger.warning to capture warning call
    warnings = []
    def fake_warning(msg):
        warnings.append(msg)
    monkeypatch.setattr(engine, "logger", MagicMock(warning=fake_warning))
    engine.update({"action": "dummy_action"}, 5.0)
    # Since no rule, warnings should be appended
    assert len(warnings) == 1

def test_update_raises_on_non_numeric_reward():
    dummy_engine = DummySymbolicEngine()
    engine = DecisionEngine(symbolic_context=dummy_engine)
    with pytest.raises(ValueError):
        engine.update({"action": "dummy_action"}, "not_a_number")

def test_update_raises_on_engine_error():
    class BadEngine(DummySymbolicEngine):
        def get_rule_by_action(self, action):
            raise Exception("fail")

    engine = DecisionEngine(symbolic_context=BadEngine())
    with pytest.raises(RuntimeError):
        engine.update({"action": "dummy_action"}, 5.0)

def test_mutate_calls_engine():
    dummy_engine = DummySymbolicEngine()
    dummy_engine.mutate_rules = MagicMock()
    engine = DecisionEngine(symbolic_context=dummy_engine)
    engine.mutate()
    dummy_engine.mutate_rules.assert_called_once()

def test_mutate_raises_on_error():
    class BadEngine(DummySymbolicEngine):
        def mutate_rules(self):
            raise Exception("fail")

    engine = DecisionEngine(symbolic_context=BadEngine())
    with pytest.raises(RuntimeError):
        engine.mutate()

def test_save_calls_engine():
    dummy_engine = DummySymbolicEngine()
    dummy_engine.save_rules = MagicMock()
    engine = DecisionEngine(symbolic_context=dummy_engine)
    engine.save()
    dummy_engine.save_rules.assert_called_once()

def test_save_raises_on_error():
    class BadEngine(DummySymbolicEngine):
        def save_rules(self):
            raise Exception("fail")

    engine = DecisionEngine(symbolic_context=BadEngine())
    with pytest.raises(RuntimeError):
        engine.save()
