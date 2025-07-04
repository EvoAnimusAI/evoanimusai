import logging
import pytest
from core import cac

def test_detect_behavior_loop():
    certifier = cac.BehaviorCertifier(max_loop_threshold=3, repetition_window=5)

    # No loop: history menor a ventana
    history_short = ["a", "b"]
    assert not certifier.detect_behavior_loop(history_short)

    # No loop: ventana llena pero sin repeticiones suficientes
    history_no_loop = ["a", "b", "a", "c", "b"]
    assert not certifier.detect_behavior_loop(history_no_loop)

    # Loop detectado: una action repetida más del umbral
    history_loop = ["a", "a", "a", "b", "c"]
    assert certifier.detect_behavior_loop(history_loop)

def test_apply_certification():
    certifier = cac.BehaviorCertifier(max_loop_threshold=2, repetition_window=3)

    # Decisión vacía o sin "action"
    decision_empty = {}
    history = ["x", "y", "z"]
    assert certifier.apply_certification(decision_empty, history) == decision_empty

    decision_no_action = {"priority": 5}
    assert certifier.apply_certification(decision_no_action, history) == decision_no_action

    # Sin ciclo detectado: decisión certificada True
    decision = {"action": "explore", "priority": 2}
    history_no_loop = ["a", "b", "c"]
    result = certifier.apply_certification(decision.copy(), history_no_loop)
    assert result["certified"] is True
    assert result["priority"] == 2

    # Con ciclo detectado: prioridad reducida y certificado False
    decision = {"action": "wait", "priority": 0}
    history_loop = ["wait", "wait", "wait"]
    result = certifier.apply_certification(decision.copy(), history_loop)
    assert result["certified"] is False
    assert result["priority"] == -1  # 0 - 1

    # Prioridad no baja más que -10
    decision = {"action": "wait", "priority": -10}
    result = certifier.apply_certification(decision.copy(), history_loop)
    assert result["priority"] == -10

def test_log_behavioral_anomaly(caplog):
    certifier = cac.BehaviorCertifier()
    class DummyContext:
        state = {"test": 123}

    with caplog.at_level(logging.ERROR):
        certifier.log_behavioral_anomaly(42, DummyContext())
        assert "[CAC] Anomalía conductual detectada en paso 42" in caplog.text
        assert "'test': 123" in caplog.text or "123" in caplog.text

