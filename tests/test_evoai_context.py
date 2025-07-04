import pytest
from unittest.mock import MagicMock, patch
from daemon.evoai_context import EvoAIContext

@pytest.fixture
def mock_context():
    with patch("daemon.evoai_context.SymbolicLearningEngine") as mock_engine_class, \
         patch("daemon.evoai_context.AgentMemory") as mock_memory_class, \
         patch("daemon.evoai_context.StateManager") as mock_state_class, \
         patch("daemon.evoai_context.Config") as mock_config_class:

        mock_engine = MagicMock()
        mock_memory = MagicMock()
        mock_state = MagicMock()
        mock_config = MagicMock()

        mock_engine_class.return_value = mock_engine
        mock_memory_class.return_value = mock_memory
        mock_state_class.return_value = mock_state
        mock_config_class.return_value = mock_config

        ctx = EvoAIContext()
        ctx.symbolic = mock_engine
        ctx.memory = mock_memory
        ctx.state = mock_state
        ctx.config = mock_config
        return ctx

def test_update_valid_observation(mock_context):
    obs = {"input": "test data"}
    mock_context.update(obs)
    mock_context.symbolic.observe.assert_called_once_with(obs)
    mock_context.state.update.assert_called_once_with(obs)

def test_update_invalid_observation_type(mock_context):
    with pytest.raises(TypeError):
        mock_context.update("not a dict")

def test_add_concept_valid(mock_context):
    mock_context.symbolic.register_concept = MagicMock()
    mock_context.add_concept("test_concept", source="unit_test")
    mock_context.symbolic.register_concept.assert_called_once_with("test_concept", "unit_test")

def test_add_concept_invalid(mock_context):
    with pytest.raises(ValueError):
        mock_context.add_concept("   ")  # concepto vacío

def test_add_concept_without_register_method(mock_context):
    del mock_context.symbolic.register_concept  # simula método ausente
    # No debe lanzar excepción
    mock_context.add_concept("fallback_concept")

def test_get_state_snapshot(mock_context):
    mock_context.symbolic.export_state.return_value = {"symbolic": "ok"}
    mock_context.memory.summary.return_value = {"memory": "ok"}
    mock_context.state.status.return_value = {"status": "ok"}
    mock_context.config.version = "1.2.3"

    snapshot = mock_context.get_state_snapshot()

    assert "timestamp_utc" in snapshot
    assert snapshot["symbolic_state"] == {"symbolic": "ok"}
    assert snapshot["memory_summary"] == {"memory": "ok"}
    assert snapshot["state_status"] == {"status": "ok"}
    assert snapshot["config_version"] == "1.2.3"
