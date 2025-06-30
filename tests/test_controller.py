import pytest
from metacognition.controller import MetacognitionController
from metacognition.targeted_mutation import TargetedMutation


class DummyMutation(TargetedMutation):
    def mutate(self, context):
        if context.get("fail_mutation"):
            raise RuntimeError("Simulated mutation failure")
        return context.get("should_mutate", False)


@pytest.fixture
def controller():
    return MetacognitionController(mutation_engine=DummyMutation())


def test_should_stop_returns_true_and_reasons(controller):
    context = {
        "recent_rewards": [-1, -2, -3, -4, -5],
        "rejected_mutations": 11,
        "cycles_without_new_rule": 20,
        "current_entropy": 0.98,
    }
    should_stop, reasons = controller.should_stop(context)
    assert should_stop is True
    assert isinstance(reasons, list)
    assert len(reasons) >= 1


def test_should_stop_returns_false(controller):
    context = {
        "recent_rewards": [1, 1, 1],
        "rejected_mutations": 0,
        "cycles_without_new_rule": 0,
        "current_entropy": 0.1,
    }
    should_stop, reasons = controller.should_stop(context)
    assert should_stop is False
    assert reasons == []


def test_should_stop_handles_exception_gracefully(controller):
    context = None  # Invalid context
    should_stop, reasons = controller.should_stop(context)
    assert should_stop is False
    assert any("Error during stop evaluation" in r for r in reasons)


def test_perform_mutation_success(controller):
    context = {"should_mutate": True}
    result = controller.perform_mutation(context)
    assert result is True


def test_perform_mutation_failure(controller):
    context = {"should_mutate": False}
    result = controller.perform_mutation(context)
    assert result is False


def test_perform_mutation_handles_exception_gracefully(controller):
    context = {"fail_mutation": True}
    result = controller.perform_mutation(context)
    assert result is False
