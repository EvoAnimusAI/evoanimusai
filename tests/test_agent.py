# tests/test_agent.py

import pytest
from unittest.mock import Mock
from core.agent import EvoAgent


@pytest.fixture
def mock_context():
    context = Mock()
    context.assert_fact = Mock()
    context.update = Mock()
    return context


def test_agent_initialization(mock_context):
    agent = EvoAgent(context=mock_context, name="TestAgent")
    assert agent.name == "TestAgent"
    assert agent.context == mock_context
    assert agent.entropy == 0.0
    mock_context.assert_fact.assert_called_with("agent_name", "TestAgent")


def test_agent_perceive_valid_input(mock_context):
    agent = EvoAgent(context=mock_context)
    observation = {"temperature": 23, "pos": "A1"}
    agent.perceive(observation)

    assert len(agent.observation_history) == 1
    assert "temperature" in agent.observation_history[0]
    mock_context.assert_fact.assert_called_with("position", "A1")
    mock_context.update.assert_called_once()


def test_agent_perceive_invalid_input_type(mock_context):
    agent = EvoAgent(context=mock_context)
    with pytest.raises(TypeError):
        agent.perceive("invalid")  # not a dict


def test_agent_perceive_sanitizes_data(mock_context):
    agent = EvoAgent(context=mock_context)
    observation = {
        123: "bad_key",
        "valid": 42,
        "complex": {"not": "allowed"},
    }
    agent.perceive(observation)
    result = agent.observation_history[-1]
    assert "valid" in result
    assert "complex" not in result
    assert 123 not in result


def test_agent_decide_returns_valid_action():
    agent = EvoAgent()
    observation = {"state": "neutral"}
    action = agent.decide(observation)
    assert action in ["explore", "wait", "calm", "advance"]
    assert agent.states[-1] == observation


def test_agent_learn_and_entropy():
    agent = EvoAgent()
    rewards = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]  # entropy should be ~2.32
    for r in rewards:
        agent.learn({"input": "dummy"}, "advance", r)

    assert len(agent.rewards) == 10
    assert agent.entropy > 2.0 and agent.entropy < 2.5


def test_agent_entropy_with_single_reward():
    agent = EvoAgent()
    agent.learn({"x": 1}, "wait", 10.0)
    assert agent.entropy == 0.0
