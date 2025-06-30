# tests/test_targeted_mutation.py

import pytest
from unittest.mock import MagicMock
from metacognition.targeted_mutation import TargetedMutation

class DummyRule:
    def __init__(self, action="wait", reward=0.0, threshold=0.5, weight=1.0):
        self.action = action
        self.reward = reward
        self.threshold = threshold
        self.weight = weight

@pytest.fixture
def dummy_rule_engine():
    engine = MagicMock()
    engine.get_all.return_value = [
        DummyRule(action="wait", reward=-0.3),
        DummyRule(action="advance", reward=0.2)
    ]
    return engine

def test_strong_mutation_applied(dummy_rule_engine):
    tm = TargetedMutation(rule_engine=dummy_rule_engine)
    context = {"recent_rewards": [-1, -1, -1]}
    result = tm.mutate(context)
    assert result is True
    assert len(tm.mutation_history) == 1

def test_moderate_mutation_applied(dummy_rule_engine):
    dummy_rule_engine.get_all.return_value = [DummyRule(reward=0.0, threshold=0.6)]
    tm = TargetedMutation(rule_engine=dummy_rule_engine)
    context = {"rejected_mutations": 10}
    result = tm.mutate(context)
    assert result is True
    assert len(tm.mutation_history) == 1

def test_light_mutation_applied(dummy_rule_engine):
    dummy_rule_engine.get_all.return_value = [DummyRule(reward=0.0, weight=1.2)]
    tm = TargetedMutation(rule_engine=dummy_rule_engine)
    context = {"recent_rewards": [0.5, 0.7]}
    result = tm.mutate(context)
    assert result is True
    assert len(tm.mutation_history) == 1

def test_mutation_fails_if_no_rules():
    empty_engine = MagicMock()
    empty_engine.get_all.return_value = []
    tm = TargetedMutation(rule_engine=empty_engine)
    context = {}
    result = tm.mutate(context)
    assert result is False
    assert len(tm.mutation_history) == 0

def test_mutation_fails_if_required_attributes_missing():
    class IncompleteRule:
        def __init__(self): pass  # no attributes

    engine = MagicMock()
    engine.get_all.return_value = [IncompleteRule()]
    tm = TargetedMutation(rule_engine=engine)
    context = {"rejected_mutations": 10}  # triggers moderate mutation
    result = tm.mutate(context)
    assert result is False
    assert len(tm.mutation_history) == 0

def test_selects_lowest_reward_rule():
    rules = [
        DummyRule(action="calm", reward=0.5),
        DummyRule(action="advance", reward=-0.4),
        DummyRule(action="explore", reward=0.1)
    ]
    engine = MagicMock()
    engine.get_all.return_value = rules
    tm = TargetedMutation(rule_engine=engine)
    selected = tm.select_rule_to_mutate()
    assert selected.reward == -0.4

def test_analyze_context_logic():
    tm = TargetedMutation()
    ctx_strong = {"recent_rewards": [-1, -1, -1]}
    ctx_moderate_rejects = {"rejected_mutations": 6}
    ctx_moderate_entropy = {"current_entropy": 0.8}
    ctx_light = {"recent_rewards": [0.5]}

    assert tm.analyze_context(ctx_strong)["type"] == "strong"
    assert tm.analyze_context(ctx_moderate_rejects)["type"] == "moderate"
    assert tm.analyze_context(ctx_moderate_entropy)["type"] == "moderate"
    assert tm.analyze_context(ctx_light)["type"] == "light"
