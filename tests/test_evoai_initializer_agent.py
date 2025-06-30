import pytest
from unittest.mock import patch, MagicMock
from core.context import EvoContext
from daemon.evoai_initializer_agent import initialize_agent


@pytest.fixture(autouse=True)
def mock_config_singleton():
    with patch("core.config.Config.get_instance") as mock_get_instance:
        mock_get_instance.return_value = MagicMock()
        yield


def test_initialize_agent_success():
    context = EvoContext()
    agent = initialize_agent(name="UnidadAlpha", context=context)
    assert agent.name == "UnidadAlpha"
    assert agent.context is context


def test_initialize_agent_default_name():
    context = EvoContext()
    agent = initialize_agent(context=context)
    assert agent.name == "EvoAI"


def test_initialize_agent_missing_context():
    with pytest.raises(ValueError):
        initialize_agent(name="SinContexto")
