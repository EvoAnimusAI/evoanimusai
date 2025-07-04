import pytest
from visual.symbolic_view import show_symbolic_state

class MockContext:
    def __init__(self, status="OK"):
        self.status = status

@pytest.mark.parametrize("reward, extra_info", [
    (None, None),
    (1.0, {"note": "success"}),
])
def test_show_symbolic_state_prints_output(capsys, reward, extra_info):
    context = MockContext()
    decision = {"action": "advance"}
    observation = {"action": "advance", "confidence": 0.95}

    show_symbolic_state(context, decision, observation, reward, extra_info)

    captured = capsys.readouterr()
    assert "Symbolic Observation" in captured.out
    assert "Symbolic Decision" in captured.out
    assert "Executed Action: advance" in captured.out
    assert f"Reward: {reward}" in captured.out if reward is not None else True
    if extra_info:
        assert "Additional Information" in captured.out
    assert "Current Symbolic Context: OK" in captured.out
