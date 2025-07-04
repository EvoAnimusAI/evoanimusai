import os
import builtins
import pytest
import tempfile
import shutil
from unittest.mock import patch, mock_open, MagicMock
import time

import runtime.monitor as monitor


def test_execution_monitor_record_get_clear():
    em = monitor.ExecutionMonitor()

    # Al inicio, lista vacía y tiempo actual
    assert isinstance(em.start_time, float)
    assert em.events == []

    # Registrar un evento
    em.record_event("TEST_TYPE", "This is a test", metadata={"key": "value"})
    assert len(em.events) == 1
    event = em.events[0]
    assert event["type"] == "TEST_TYPE"
    assert event["description"] == "This is a test"
    assert event["metadata"] == {"key": "value"}
    assert isinstance(event["timestamp"], float)

    # Probar get_summary con más de 10 eventos
    for i in range(15):
        em.record_event("TYPE", f"Desc {i}")

    summary = em.get_summary()
    assert summary["total_events"] == 16  # 1 previo + 15
    assert summary["duration"] >= 0
    assert len(summary["events"]) == 10  # últimos 10 eventos
    assert summary["events"][0]["description"] == "Desc 5"  # evento número 6

    # Probar clear reinicia eventos y tiempo
    old_start = em.start_time
    time.sleep(0.01)
    em.clear()
    assert em.events == []
    assert em.start_time > old_start


def test_evoai_monitor_log_and_summary():
    eam = monitor.EvoAIMonitor()
    assert eam.logs == []

    eam.log(1, "obs1", "action1", 5.0)
    eam.log(2, "obs2", "action2", -3.5)
    assert len(eam.logs) == 2

    summary = eam.summary()
    assert summary["total_steps"] == 2
    assert summary["total_reward"] == 1.5  # 5.0 + (-3.5)


def test_log_event_prints_and_writes(tmp_path):
    # Sobrescribir LOG_FILE_PATH para evitar tocar archivos reales
    test_log_file = tmp_path / "system_events.log"
    monitor.LOG_FILE_PATH = str(test_log_file)

    with patch("builtins.print") as mock_print:
        monitor.log_event("TEST_EVENT", "This is a log message", level="WARNING")

        # Verificar que se imprimió en consola
        mock_print.assert_called()
        printed_text = mock_print.call_args[0][0]
        assert "[TEST_EVENT]" in printed_text
        assert "[WARNING]" in printed_text
        assert "This is a log message" in printed_text

        # Verificar que se escribió en archivo
        with open(test_log_file, "r") as f:
            content = f.read()
            assert "This is a log message" in content

    # Probar que si la carpeta no existe, se crea sin error
    non_existent_dir = tmp_path / "nonexistent_dir"
    monitor.LOG_FILE_PATH = str(non_existent_dir / "file.log")

    with patch("builtins.print") as mock_print_error:
        monitor.log_event("EVENT", "msg")

        # Debería crear la carpeta y escribir sin excepción, no debería imprimir error


def test_log_event_handles_write_exception(monkeypatch):
    # Forzar excepción en open()
    def fake_open(*args, **kwargs):
        raise IOError("Fake IOError")

    monkeypatch.setattr("builtins.open", fake_open)
    monkeypatch.setattr("os.makedirs", lambda *a, **k: None)  # evitar error en mkdir

    with patch("builtins.print") as mock_print:
        monitor.log_event("ERR_EVENT", "Error message")
        # Se imprime mensaje de error al no poder escribir en archivo
        printed = [call[0][0] for call in mock_print.call_args_list]
        assert any("[ERROR] No se pudo escribir en log" in line for line in printed)
