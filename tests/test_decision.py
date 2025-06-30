import pytest
from unittest.mock import Mock
from core.decision import DecisionEngine

def get_mock_symbolic_engine():
    mock = Mock()
    mock.decide.return_value = "some_action"
    mock.get_rule_by_action.return_value = "some_rule"
    mock.update_rule.return_value = None
    mock.mutate_rules.return_value = None
    mock.save_rules.return_value = None
    return mock

def test_init_with_default_engine():
    engine = DecisionEngine()
    assert engine.engine is not None

def test_init_with_custom_engine():
    mock_engine = get_mock_symbolic_engine()
    engine = DecisionEngine(symbolic_context=mock_engine)
    assert engine.engine == mock_engine

def test_init_invalid_engine_type():
    with pytest.raises(TypeError):
        DecisionEngine(symbolic_context="not_an_engine")

def test_decide_success():
    mock_engine = get_mock_symbolic_engine()
    engine = DecisionEngine(symbolic_context=mock_engine)
    context = {"state": "test"}
    action = engine.decide(context)
    assert action == "some_action"
    mock_engine.decide.assert_called_once_with(context)

def test_decide_with_none_context_raises():
    engine = DecisionEngine()
    with pytest.raises(ValueError):
        engine.decide(None)

def test_decide_engine_raises_runtime_error():
    mock_engine = get_mock_symbolic_engine()
    mock_engine.decide.side_effect = RuntimeError("fail decide")
    engine = DecisionEngine(symbolic_context=mock_engine)
    with pytest.raises(RuntimeError):
        engine.decide({"state": "test"})

def test_update_success_with_rule_found():
    mock_engine = get_mock_symbolic_engine()
    engine = DecisionEngine(symbolic_context=mock_engine)
    action = "some_action"
    reward = 1.0
    engine.update(action, reward)
    mock_engine.get_rule_by_action.assert_called_once_with(action)
    mock_engine.update_rule.assert_called_once_with("some_rule", reward)

def test_update_success_with_no_rule_found(caplog):
    mock_engine = get_mock_symbolic_engine()
    mock_engine.get_rule_by_action.return_value = None
    engine = DecisionEngine(symbolic_context=mock_engine)
    with caplog.at_level("WARNING"):
        engine.update("some_action", 1.0)
    assert "No se encontró regla" in caplog.text

def test_update_invalid_reward_type():
    engine = DecisionEngine()
    with pytest.raises(ValueError):
        engine.update("some_action", "not_a_number")

def test_update_engine_raises_runtime_error():
    mock_engine = get_mock_symbolic_engine()
    mock_engine.get_rule_by_action.return_value = "rule1"
    mock_engine.update_rule.side_effect = RuntimeError("fail update")
    engine = DecisionEngine(symbolic_context=mock_engine)
    with pytest.raises(RuntimeError):
        engine.update("some_action", 1.0)

def test_mutate_success():
    mock_engine = get_mock_symbolic_engine()
    engine = DecisionEngine(symbolic_context=mock_engine)
    engine.mutate()
    mock_engine.mutate_rules.assert_called_once()

def test_mutate_engine_raises_runtime_error():
    mock_engine = get_mock_symbolic_engine()
    mock_engine.mutate_rules.side_effect = RuntimeError("fail mutate")
    engine = DecisionEngine(symbolic_context=mock_engine)
    with pytest.raises(RuntimeError):
        engine.mutate()

def test_save_success():
    mock_engine = get_mock_symbolic_engine()
    engine = DecisionEngine(symbolic_context=mock_engine)
    engine.save()
    mock_engine.save_rules.assert_called_once()

def test_save_engine_raises_runtime_error():
    mock_engine = get_mock_symbolic_engine()
    mock_engine.save_rules.side_effect = RuntimeError("fail save")
    engine = DecisionEngine(symbolic_context=mock_engine)
    with pytest.raises(RuntimeError):
        engine.save()
