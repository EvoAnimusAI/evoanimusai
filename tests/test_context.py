import pytest
from unittest.mock import Mock
from core import context  # Ajusta el import según tu estructura


def test_initial_state():
    evo_ctx = context.EvoContext()
    state = evo_ctx.get_context()
    assert state["observation"] is None
    assert state["last_action"] is None
    assert state["last_decision"] is None
    assert state["entropy"] == 0.0
    assert isinstance(state["rewards"], list) and len(state["rewards"]) == 0


def test_update_valid_observation():
    evo_ctx = context.EvoContext()
    obs = {"entropía": 0.42, "data": 123}
    updated_state = evo_ctx.update(obs)
    assert updated_state["observation"] == obs
    assert updated_state["entropy"] == 0.42


def test_update_invalid_observation_type():
    evo_ctx = context.EvoContext()
    with pytest.raises(TypeError):
        evo_ctx.update("no es diccionario")


def test_decide_with_no_observation():
    evo_ctx = context.EvoContext()
    result = evo_ctx.decide()
    assert result == (None, None)


def test_decide_with_agent_and_engine_success():
    mock_agent = Mock()
    mock_agent.decide.return_value = "agent_action"
    mock_engine = Mock()
    mock_engine.decide.return_value = "engine_decision"

    evo_ctx = context.EvoContext(agent=mock_agent, engine=mock_engine)
    evo_ctx.update({"data": 1})
    agent_action, engine_decision = evo_ctx.decide()

    assert agent_action == "agent_action"
    assert engine_decision == "engine_decision"
    # Verifica estado interno actualizado
    state = evo_ctx.get_context()
    assert state["last_action"] == "agent_action"
    assert state["last_decision"] == "engine_decision"


def test_decide_agent_raises():
    class FaultyAgent:
        def decide(self, _):
            raise RuntimeError("fail agent")

    mock_engine = Mock()
    mock_engine.decide.return_value = "engine_decision"

    evo_ctx = context.EvoContext(agent=FaultyAgent(), engine=mock_engine)
    evo_ctx.update({"data": 1})

    agent_action, engine_decision = evo_ctx.decide()

    assert agent_action is None
    assert engine_decision == "engine_decision"


def test_decide_engine_raises():
    mock_agent = Mock()
    mock_agent.decide.return_value = "agent_action"

    class FaultyEngine:
        def decide(self, _):
            raise RuntimeError("fail engine")

    evo_ctx = context.EvoContext(agent=mock_agent, engine=FaultyEngine())
    evo_ctx.update({"data": 1})

    agent_action, engine_decision = evo_ctx.decide()

    assert agent_action == "agent_action"
    assert engine_decision is None


def test_record_reward_valid_and_limit():
    evo_ctx = context.EvoContext()
    for i in range(25):
        evo_ctx.record_reward(float(i))

    state = evo_ctx.get_context()
    # Solo los últimos 20 se deben mantener
    assert len(state["rewards"]) == 20
    assert state["rewards"][0] == 5.0
    assert state["rewards"][-1] == 24.0


def test_record_reward_invalid_type():
    evo_ctx = context.EvoContext()
    with pytest.raises(TypeError):
        evo_ctx.record_reward("no es número")


def test_assert_fact_no_engine():
    evo_ctx = context.EvoContext(engine=None)
    result = evo_ctx.assert_fact("key", "value")
    assert result is False


def test_assert_fact_engine_without_method():
    class EngineNoAssert:
        pass

    evo_ctx = context.EvoContext(engine=EngineNoAssert())
    result = evo_ctx.assert_fact("key", "value")
    assert result is False


def test_assert_fact_engine_method_raises():
    class FaultyEngine:
        def assert_fact(self, key, value):
            raise RuntimeError("fail assert")

    evo_ctx = context.EvoContext(engine=FaultyEngine())
    result = evo_ctx.assert_fact("key", "value")
    assert result is False


def test_assert_fact_engine_method_success(capfd):
    class EngineWithAssert:
        def assert_fact(self, key, value):
            # Simula éxito, sin error ni retorno
            pass

    engine = EngineWithAssert()
    evo_ctx = context.EvoContext(engine=engine)
    result = evo_ctx.assert_fact("key", "value")

    assert result is True

    captured = capfd.readouterr()
    assert "[INFO] Hecho afirmado" in captured.out


def test_get_context_returns_copy():
    evo_ctx = context.EvoContext()
    evo_ctx.state["observation"] = {"data": 123}
    context_copy = evo_ctx.get_context()
    # Modificar copia no afecta el original
    context_copy["observation"]["data"] = 999
    assert evo_ctx.state["observation"]["data"] == 123


def test_status_property_returns_copy():
    evo_ctx = context.EvoContext()
    evo_ctx.state["observation"] = {"data": 321}
    status_copy = evo_ctx.status
    status_copy["observation"]["data"] = 555
    assert evo_ctx.state["observation"]["data"] == 321
