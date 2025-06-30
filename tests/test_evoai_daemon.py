# tests/test_evoai_daemon.py
# -*- coding: utf-8 -*-
"""
Test gubernamental para evoai_daemon.py
"""

import pytest
from unittest import mock
from daemon import evoai_daemon


def test_main_with_invalid_key(caplog):
    caplog.set_level("CRITICAL")
    evoai_daemon.main(daemon_key="clave_incorrecta", test_mode=True)
    assert "Clave inválida. Acceso denegado." in caplog.text


@mock.patch("daemon.evoai_daemon.initialize_core_components")
@mock.patch("daemon.evoai_daemon.run_cycle_loop")
def test_main_with_valid_key(mock_run_cycle_loop, mock_initialize_core, caplog):
    caplog.set_level("INFO")

    # Simular componentes devueltos por el inicializador
    mock_initialize_core.return_value = {"dummy": "component"}

    evoai_daemon.main(daemon_key=evoai_daemon.DAEMON_KEY, test_mode=True)

    assert "Clave aceptada. Iniciando EvoAI..." in caplog.text
    mock_initialize_core.assert_called_once()
    mock_run_cycle_loop.assert_called_once_with({"dummy": "component"}, test_mode=True)
