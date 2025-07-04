import pytest
from unittest.mock import MagicMock
from core.symbolic_decision_engine import SymbolicDecisionEngine
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine, SymbolicRule
from core.context import EvoContext


class DummyRule(SymbolicRule):
    def __init__(self, name, confidence):
        self.name = name
        self.confidence = confidence
    def to_dict(self):
        # Incluir la clave que el motor espera
        return {"action": self.name, "rule": self.name, "confidence": self.confidence}


class DummyRuleEngine(SymbolicRuleEngine):
    def evaluate(self, context):
        return [
            DummyRule("rule1", 0.5),
            DummyRule("rule2", 0.9),
            DummyRule("rule3", 0.2),
        ]
    def assert_fact(self, key, value):
        pass


def test_decide_returns_highest_priority_rule(monkeypatch):
    context = MagicMock(spec=EvoContext); context.state = {}
    monkeypatch.setattr("core.symbolic_decision_engine.check_entropy", lambda ctx: 0.2)
    monkeypatch.setattr("core.symbolic_decision_engine.should_halt", lambda e: False)
    monkeypatch.setattr("core.symbolic_decision_engine.version_rule", lambda d: {"checksum": "abc"})
    sde = SymbolicDecisionEngine(context, DummyRuleEngine())
    result = sde.decide({"x": "y"})
    assert result["action"] == "rule2"
    assert result["confidence"] == 0.9
    assert result["source"] == "symbolic_decision_engine"


def test_decide_returns_noop_if_no_rules(monkeypatch):
    class EmptyEngine(SymbolicRuleEngine):
        def evaluate(self, ctx): return []
    context = MagicMock(spec=EvoContext); context.state = {}
    monkeypatch.setattr("core.symbolic_decision_engine.check_entropy", lambda ctx: 0.1)
    monkeypatch.setattr("core.symbolic_decision_engine.should_halt", lambda e: False)
    sde = SymbolicDecisionEngine(context, EmptyEngine())
    resp = sde.decide({"ctx": 1})
    assert resp["action"] == "noop"


def test_decide_halts_on_high_entropy(monkeypatch):
    context = MagicMock(spec=EvoContext); context.state = {}
    monkeypatch.setattr("core.symbolic_decision_engine.check_entropy", lambda ctx: 1.3)
    monkeypatch.setattr("core.symbolic_decision_engine.should_halt", lambda e: True)
    sde = SymbolicDecisionEngine(context, DummyRuleEngine())
    resp = sde.decide({"any": "ctx"})
    assert resp["action"] == "halt"


def test_prioritize_orders_by_confidence():
    context = MagicMock(spec=EvoContext)
    sde = SymbolicDecisionEngine(context, DummyRuleEngine())
    rules = [DummyRule("a", 0.1), DummyRule("b", 0.8), DummyRule("c", 0.5)]
    prio = sde.prioritize_rules(rules)
    assert [r.name for r in prio] == ["b", "c", "a"]


def test_public_prioritize_handles_dicts():
    context = MagicMock(spec=EvoContext)
    sde = SymbolicDecisionEngine(context, DummyRuleEngine())
    lst = [{"action": "a", "confidence": 0.3}, {"action": "b", "confidence": 0.7}]
    res = sde.prioritize(lst)
    assert res[0]["action"] == "b" and res[1]["action"] == "a"


def test_assert_fact_calls_engine():
    class FactEngine(DummyRuleEngine):
        def __init__(self): super().__init__(); self.fact = None
        def assert_fact(self, k, v): self.fact = (k, v)
    ctx = MagicMock(spec=EvoContext)
    eng = FactEngine()
    SymbolicDecisionEngine(ctx, eng).assert_fact("thr", "high")
    assert eng.fact == ("thr", "high")


def test_init_invalid_context_raises():
    with pytest.raises(TypeError):
        SymbolicDecisionEngine("not-context")
