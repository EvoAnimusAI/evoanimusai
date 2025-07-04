import pytest
from core.environment import Environment

def test_initial_state():
    env = Environment()
    state = env.observe()
    assert state["pos"] == 0
    assert state["explored"] is False
    assert state["entropy"] == 0.0
    assert state["energy"] == 100
    assert state["noise"] is None

def test_reset_resets_state():
    env = Environment()
    env.state["pos"] = 3
    env.reset()
    state = env.observe()
    assert state["pos"] == 0
    assert state["explored"] is False
    assert state["entropy"] == 0.0
    assert state["energy"] == 100

def test_act_explore_rewards_and_state_changes():
    env = Environment()
    reward, done = env.act("explore")
    assert reward == 2.0
    assert env.state["explored"] is True

def test_act_explore_redundant_penalty():
    env = Environment()
    env.act("explore")
    reward, done = env.act("explore")
    assert reward == -0.2

def test_act_advance_moves_forward_and_reduces_energy():
    env = Environment()
    old_pos = env.state["pos"]
    old_energy = env.state["energy"]
    reward, done = env.act("advance")
    assert env.state["pos"] == old_pos + 1
    assert env.state["energy"] == old_energy - 5
    assert reward == 1.0

def test_act_advance_limits_movement():
    env = Environment(parameters={"max_position": 1})
    env.state["pos"] = 1
    reward, done = env.act("advance")
    assert reward == -0.5

def test_act_wait_penalty():
    env = Environment()
    reward, done = env.act("wait")
    assert reward == -0.1

def test_act_calm_reduces_entropy():
    env = Environment()
    env.state["entropy"] = 0.5
    reward, done = env.act("calm")
    assert env.state["entropy"] < 0.5
    assert reward == 0.5

def test_act_calm_low_entropy_penalty():
    env = Environment()
    env.state["entropy"] = 0.2
    reward, done = env.act("calm")
    assert reward == -0.1

def test_act_reset_resets_environment():
    env = Environment()
    env.state["pos"] = 3
    reward, done = env.act("reset")
    assert reward == 0.0
    assert env.state["pos"] == 0

def test_act_unrecognized_action_penalty():
    env = Environment()
    reward, done = env.act("unknown_action")
    assert reward == -1.0

def test_act_invalid_action_type_raises():
    env = Environment()
    import pytest
    with pytest.raises(TypeError):
        env.act(123)

def test_act_empty_action_raises():
    env = Environment()
    import pytest
    with pytest.raises(ValueError):
        env.act("")

