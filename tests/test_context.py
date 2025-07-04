import pytest
from unittest.mock import patch, MagicMock
from core.context import EvoContext

class DummyAgent:
    def decide(self, observation):
        return "agent_action"

class DummyEngine:
    def decide(self, observation):
        return "symbolic_decision"
    def assert_fact(self, key, value):
        pass

@pytest.fixture(autouse=True)
def mock_config():
    with patch("core.context.Config") as MockConfig:
        MockConfig.get_instance.return_value = MagicMock()
        yield

def test_update_and_get_context():
    ctx = EvoContext()
    obs = {"entropy": 0.75, "sensor": "value"}
    updated = ctx.update(obs)
    assert updated["observation"] == obs
    assert updated["entropy"] == 0.75

def test_decide_returns_none_when_no_observation():
    ctx = EvoContext()
    agent_action, symbolic_decision = ctx.decide()
    assert agent_action is None
    assert symbolic_decision is None

def test_decide_with_agent_and_engine():
    ctx = EvoContext(agent=DummyAgent(), engine=DummyEngine())
    ctx.update({"entropy": 0.3})
    agent_action, symbolic_decision = ctx.decide()
    assert agent_action == "agent_action"
    assert symbolic_decision == "symbolic_decision"
    assert ctx.state["last_action"] == "agent_action"
    assert ctx.state["last_decision"] == "symbolic_decision"

def test_record_reward_limits_history():
    ctx = EvoContext()
    for i in range(30):
        ctx.record_reward(float(i))
    assert len(ctx.state["rewards"]) == ctx.MAX_REWARDS_HISTORY
    assert ctx.state["rewards"][0] == 10.0

def test_assert_fact_returns_true_when_successful():
    ctx = EvoContext()
    dummy_engine = DummyEngine()
    ctx.engine = dummy_engine
    result = ctx.assert_fact("test_key", "test_value")
    assert result is True

def test_assert_fact_returns_false_when_no_engine_support():
    class NoAssertEngine:
        pass

    ctx = EvoContext()
    ctx.engine = NoAssertEngine()
    ctx.symbolic_engine = None
    result = ctx.assert_fact("key", "value")
    assert result is False

def test_update_context_and_get_context():
    ctx = EvoContext()
    ctx.update_context("new_key", 123)
    context_dict = ctx.get_context()
    assert context_dict["new_key"] == 123

def test_symbolic_decision_engine_property():
    ctx = EvoContext()
    ctx.symbolic_engine = "dummy"
    assert ctx.symbolic_decision_engine == "dummy"
    ctx.symbolic_engine = None
    assert ctx.symbolic_decision_engine is None
