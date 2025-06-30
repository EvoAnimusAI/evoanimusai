import pytest
from unittest.mock import MagicMock
from symbolic_ai.symbolic_learning_engine import SymbolicLearningEngine, RuleEngineInterface


class DummyRule:
    def __init__(self, texto):
        self.texto = texto


@pytest.fixture
def mock_rule_engine():
    engine = MagicMock(spec=RuleEngineInterface)
    return engine


def test_init_requires_rule_engine():
    with pytest.raises(ValueError, match="obligatorio"):
        SymbolicLearningEngine()


def test_register_concept_adds_to_generated_rules(mock_rule_engine):
    engine = SymbolicLearningEngine(rule_engine=mock_rule_engine)
    engine.register_concept("autonomía", "núcleo")
    assert ("autonomía", "núcleo") in engine.generated_rules


def test_observe_logs_observation(mock_rule_engine, caplog):
    engine = SymbolicLearningEngine(rule_engine=mock_rule_engine)
    with caplog.at_level("INFO"):
        engine.observe({"sensor": "alerta"})
    assert any("Observación recibida" in msg for msg in caplog.messages)


def test_apply_rules_returns_texts(mock_rule_engine):
    mock_rule_engine.evaluate.return_value = [
        DummyRule("accion_1"),
        DummyRule("accion_2"),
    ]
    engine = SymbolicLearningEngine(rule_engine=mock_rule_engine)
    context = {"estado": "activo"}
    resultado = engine.apply_rules(context)
    assert resultado == ["accion_1", "accion_2"]
    mock_rule_engine.evaluate.assert_called_once_with(context)


def test_add_rule_delegates_to_engine(mock_rule_engine):
    engine = SymbolicLearningEngine(rule_engine=mock_rule_engine)
    rule = DummyRule("acción_X")
    engine.add_rule(rule)
    mock_rule_engine.add_rule.assert_called_once_with(rule)


def test_export_state_includes_all_internal_data(mock_rule_engine):
    engine = SymbolicLearningEngine(rule_engine=mock_rule_engine)
    engine.register_concept("inteligencia", "simbolismo")
    state = engine.export_state()

    assert isinstance(state, dict)
    assert "generated_rules" in state
    assert ("inteligencia", "simbolismo") in state["generated_rules"]
    assert state["engine_type"] == type(mock_rule_engine).__name__
