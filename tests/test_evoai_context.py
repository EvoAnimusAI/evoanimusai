import pytest
from unittest.mock import MagicMock
from daemon.evoai_context import EvoAIContext
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine


@pytest.fixture
def evoai_context():
    rule_engine = SymbolicRuleEngine()
    return EvoAIContext(symbolic_engine=rule_engine)


def test_initialization(evoai_context):
    assert isinstance(evoai_context.symbolic, object)
    assert isinstance(evoai_context.memory, object)
    assert isinstance(evoai_context.state, object)
    assert isinstance(evoai_context.config, object)


def test_update_accepts_valid_observation(evoai_context):
    evoai_context.symbolic.observe = MagicMock()
    evoai_context.state.update = MagicMock()

    observation = {"event": "test", "value": 42}
    evoai_context.update(observation)

    evoai_context.symbolic.observe.assert_called_once_with(observation)
    evoai_context.state.update.assert_called_once_with(observation)


def test_update_rejects_invalid_observation(evoai_context):
    with pytest.raises(TypeError):
        evoai_context.update("not a dict")


def test_update_logs_observation(evoai_context, caplog):
    caplog.set_level("INFO")
    evoai_context.symbolic.observe = MagicMock()
    evoai_context.state.update = MagicMock()

    observation = {"event": "log_test"}
    evoai_context.update(observation)

    assert any("Observación registrada" in record.message for record in caplog.records)


def test_add_concept_valid(evoai_context):
    evoai_context.symbolic.register_concept = MagicMock()
    evoai_context.add_concept("inteligencia", source="prueba")

    evoai_context.symbolic.register_concept.assert_called_once_with("inteligencia", "prueba")


def test_add_concept_invalid_empty_string(evoai_context):
    with pytest.raises(ValueError):
        evoai_context.add_concept("")


def test_add_concept_invalid_non_string(evoai_context):
    with pytest.raises(ValueError):
        evoai_context.add_concept(1234)


def test_add_concept_logs_addition(evoai_context, caplog):
    caplog.set_level("INFO")
    evoai_context.symbolic.register_concept = MagicMock()

    evoai_context.add_concept("autonomía", source="unidad-test")

    assert any("Concepto agregado" in record.message for record in caplog.records)


def test_get_state_snapshot_returns_expected_structure(evoai_context):
    evoai_context.symbolic.export_state = MagicMock(return_value={"concepts": ["A", "B"]})

    evoai_context.memory = MagicMock()
    evoai_context.memory.summary.return_value = {"items": 5}

    evoai_context.state.status = MagicMock(return_value={"active": True})

    snapshot = evoai_context.get_state_snapshot()

    assert "timestamp_utc" in snapshot
    assert snapshot["symbolic_state"] == {"concepts": ["A", "B"]}
    assert snapshot["memory_summary"] == {"items": 5}
    assert snapshot["state_status"] == {"active": True}
    assert snapshot["config_version"] == "1.0.0"


def test_get_state_snapshot_logs_error(caplog, evoai_context):
    caplog.set_level("ERROR")

    evoai_context.symbolic.export_state = MagicMock(side_effect=RuntimeError("Forced error"))

    with pytest.raises(RuntimeError):
        evoai_context.get_state_snapshot()

    assert any("Error al obtener snapshot del estado" in record.message for record in caplog.records)
