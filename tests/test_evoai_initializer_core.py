import pytest
from unittest.mock import patch, MagicMock
from daemon import evoai_initializer_core


def test_initialize_core_components_success():
    with patch("daemon.evoai_initializer_core.load_secure_key", return_value="dummy_key"), \
         patch("daemon.evoai_initializer_core.Config.load_from_file"), \
         patch("daemon.evoai_initializer_core.EvoContext") as mock_context_class, \
         patch("daemon.evoai_initializer_core.initialize_agent") as mock_init_agent, \
         patch("daemon.evoai_initializer_core.initialize_engine") as mock_init_engine, \
         patch("daemon.evoai_initializer_core.initialize_decision") as mock_init_decision, \
         patch("daemon.evoai_initializer_core.initialize_executor") as mock_init_executor, \
         patch("daemon.evoai_initializer_core.initialize_support_tools") as mock_init_tools, \
         patch("daemon.evoai_initializer_core.SymbolicRuleEngine") as mock_symbolic_engine:

        mock_context = MagicMock()
        mock_agent = MagicMock()
        mock_engine = MagicMock()
        mock_decision = MagicMock()
        mock_executor = MagicMock()
        mock_tools = {"monitor": MagicMock(), "io": MagicMock()}

        mock_context_class.return_value = mock_context
        mock_init_agent.return_value = mock_agent
        mock_init_engine.return_value = mock_engine
        mock_init_decision.return_value = mock_decision
        mock_init_executor.return_value = mock_executor
        mock_init_tools.return_value = mock_tools
        mock_symbolic_engine.return_value = MagicMock()

        result = evoai_initializer_core.initialize_core_components()

        assert result["context"] is mock_context
        assert result["agent"] is mock_agent
        assert result["engine"] is mock_engine
        assert result["decision"] is mock_decision
        assert result["executor"] is mock_executor
        assert result["monitor"] == mock_tools["monitor"]
        assert result["io"] == mock_tools["io"]


def test_initialize_core_components_config_failure():
    with patch("daemon.evoai_initializer_core.load_secure_key"), \
         patch("daemon.evoai_initializer_core.Config.load_from_file", side_effect=Exception("config missing")):

        with pytest.raises(SystemExit) as excinfo:
            evoai_initializer_core.initialize_core_components()

        assert excinfo.type == SystemExit
        assert excinfo.value.code == 1
