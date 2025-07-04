import pytest
from metacognition.controller import MetacognitionController
from metacognition.targeted_mutation import TargetedMutation


class DummyMutationEngine:
    def __init__(self, should_succeed=True):
        self.should_succeed = should_succeed
        self.called = False

    def mutate(self, context):
        self.called = True
        if self.should_succeed:
            return True
        raise Exception("Mutation failed")


@pytest.fixture
def controller_success():
    engine = DummyMutationEngine(should_succeed=True)
    return MetacognitionController(mutation_engine=engine), engine


@pytest.fixture
def controller_failure():
    engine = DummyMutationEngine(should_succeed=False)
    return MetacognitionController(mutation_engine=engine), engine


def test_should_stop_returns_expected_structure():
    controller = MetacognitionController()
    context = {
        "recent_rewards": [-1, -1, -1, -1, -1],
        "rejected_mutations": 15,
        "cycles_without_new_rule": 20,
        "current_entropy": 0.99
    }
    stop_flag, reasons = controller.should_stop(context)
    assert isinstance(stop_flag, bool)
    assert isinstance(reasons, list)
    assert stop_flag is True
    assert len(reasons) >= 1


def test_should_stop_handles_exception_gracefully():
    controller = MetacognitionController()
    stop_flag, reasons = controller.should_stop(None)  # Invalid input
    assert stop_flag is False
    assert any("Error during stop evaluation" in r for r in reasons)


def test_perform_mutation_success(controller_success):
    controller, engine = controller_success
    result = controller.perform_mutation({"some": "context"})
    assert result is True
    assert engine.called is True


def test_perform_mutation_failure(controller_failure):
    controller, engine = controller_failure
    result = controller.perform_mutation({"some": "context"})
    assert result is False
    assert engine.called is True
