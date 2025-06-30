# tests/test_interfaces.py

import pytest
from metacognition.interfaces import StoppingStrategy, MutationStrategy
from metacognition.autonomous_stop import evaluate_contextual_stop
from metacognition.targeted_mutation import TargetedMutation


class AutonomousStopWrapper(StoppingStrategy):
    """
    Adapter class to wrap the evaluate_contextual_stop function into a class-based interface.
    """

    def should_stop(self, context):
        return evaluate_contextual_stop(context)


# Dummy classes to satisfy the TargetedMutation dependency
class DummyRule:
    def __init__(self):
        self.reward = -5
        self.action = "wait"
        self.threshold = 0.5
        self.weight = 0.8


class DummyRuleEngine:
    def get_all(self):
        return [DummyRule()]


@pytest.fixture
def sample_context():
    return {
        "recent_rewards": [-1, -1, -1, -1, -1],
        "rejected_mutations": 12,
        "cycles_without_new_rule": 20,
        "current_entropy": 0.98
    }


def test_autonomous_stop_implements_interface(sample_context):
    stopper = AutonomousStopWrapper()
    assert isinstance(stopper, StoppingStrategy)
    should_stop, reasons = stopper.should_stop(sample_context)
    assert should_stop is True
    assert isinstance(reasons, list)
    assert all(isinstance(r, str) for r in reasons)


def test_targeted_mutation_implements_interface(sample_context):
    mutator = TargetedMutation(rule_engine=DummyRuleEngine())
    assert isinstance(mutator, MutationStrategy)
    result = mutator.mutate(sample_context)
    assert isinstance(result, bool)
