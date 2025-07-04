import pytest
from unittest.mock import patch, MagicMock
from daemon import evoai_initializer_tools


def test_initialize_support_tools_success():
    with patch("daemon.evoai_initializer_tools.CodeAnalyzer") as mock_code_analyzer, \
         patch("daemon.evoai_initializer_tools.EvoAIMonitor") as mock_monitor, \
         patch("daemon.evoai_initializer_tools.Autoconsciousness") as mock_consciousness, \
         patch("daemon.evoai_initializer_tools.NetworkAccess") as mock_network, \
         patch("daemon.evoai_initializer_tools.EvoCodex") as mock_codex:

        mock_code_analyzer_instance = MagicMock()
        mock_monitor_instance = MagicMock()
        mock_consciousness_instance = MagicMock()
        mock_network_instance = MagicMock()
        mock_codex_instance = MagicMock()

        mock_code_analyzer.return_value = mock_code_analyzer_instance
        mock_monitor.return_value = mock_monitor_instance
        mock_consciousness.return_value = mock_consciousness_instance
        mock_network.return_value = mock_network_instance
        mock_codex.return_value = mock_codex_instance

        tools = evoai_initializer_tools.initialize_support_tools(
            engine="dummy_engine", context="dummy_context", daemon_key="SECUREKEY123456789012"
        )

        assert tools["monitor"] == mock_monitor_instance
        assert tools["code_analyzer"] == mock_code_analyzer_instance
        assert tools["analyzer"] == mock_code_analyzer_instance
        assert tools["consciousness"] == mock_consciousness_instance
        assert tools["network"] == mock_network_instance
        assert tools["codex"] == mock_codex_instance
        assert tools["decision_engine"] == "dummy_engine"


def test_initialize_support_tools_failure():
    with patch("daemon.evoai_initializer_tools.CodeAnalyzer", side_effect=RuntimeError("boom")):
        with pytest.raises(RuntimeError, match="boom"):
            evoai_initializer_tools.initialize_support_tools(
                engine=None, context=None, daemon_key="key"
            )
