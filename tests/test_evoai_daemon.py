import pytest
from unittest.mock import patch, MagicMock
from daemon import evoai_daemon

def test_main_key_valid_and_diagnostics_pass():
    with patch("daemon.evoai_daemon.setup_signal_handlers"), \
         patch("daemon.evoai_daemon.load_secure_key", return_value="A591243133418571088300454z"), \
         patch("daemon.evoai_daemon.initialize_core_components", return_value={"core": "mock"}), \
         patch("daemon.evoai_daemon.run_cycle_loop") as mock_cycle_loop, \
         patch("daemon.evoai_daemon.SelfDiagnostics") as mock_diag_class:

        mock_diag = MagicMock()
        mock_diag.run_preflight_check.return_value = True
        mock_diag_class.return_value = mock_diag

        evoai_daemon.main("A591243133418571088300454z", test_mode=True)

        mock_cycle_loop.assert_called_once_with(test_mode=True)
        mock_diag.run_preflight_check.assert_called_once()


def test_main_invalid_key_blocks_execution():
    with patch("daemon.evoai_daemon.setup_signal_handlers"), \
         patch("daemon.evoai_daemon.load_secure_key", return_value="SECURE_KEY"), \
         patch("daemon.evoai_daemon.initialize_core_components") as init_components, \
         patch("daemon.evoai_daemon.SelfDiagnostics") as diag, \
         patch("daemon.evoai_daemon.run_cycle_loop") as cycle:

        evoai_daemon.main("WRONG_KEY")

        init_components.assert_not_called()
        diag.assert_not_called()
        cycle.assert_not_called()


def test_main_key_valid_but_diagnostics_fail():
    with patch("daemon.evoai_daemon.setup_signal_handlers"), \
         patch("daemon.evoai_daemon.load_secure_key", return_value="A591243133418571088300454z"), \
         patch("daemon.evoai_daemon.initialize_core_components", return_value={"core": "mock"}), \
         patch("daemon.evoai_daemon.SelfDiagnostics") as mock_diag_class, \
         patch("daemon.evoai_daemon.run_cycle_loop") as mock_cycle_loop:

        mock_diag = MagicMock()
        mock_diag.run_preflight_check.return_value = False
        mock_diag_class.return_value = mock_diag

        evoai_daemon.main("A591243133418571088300454z")

        mock_cycle_loop.assert_not_called()
        mock_diag.run_preflight_check.assert_called_once()
