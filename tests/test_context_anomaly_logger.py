import pytest
import logging
from monitoring.context_anomaly_logger import ContextAnomalyLogger

@pytest.fixture
def valid_context():
    return {
        "state": "active",
        "observations": {"sensor": "ok"},
        "history": [],
        "rewards": [1.0, 0.5],
        "parameters": {"threshold": 0.8}
    }

def test_valid_context_logs_success(caplog, valid_context):
    with caplog.at_level(logging.DEBUG):
        result = ContextAnomalyLogger.validate_and_log(valid_context)
        assert result is True
        assert "[ContextAnomaly] ✅ Contexto validado correctamente." in caplog.text

def test_context_missing_keys(caplog, valid_context):
    context = valid_context.copy()
    del context["history"]
    with caplog.at_level(logging.DEBUG):
        result = ContextAnomalyLogger.validate_and_log(context)
        assert result is False
        assert "Claves faltantes" in caplog.text
        assert "⛔ Contexto inválido detectado" in caplog.text

def test_context_type_mismatch(caplog, valid_context):
    context = valid_context.copy()
    context["rewards"] = "should_be_list"
    with caplog.at_level(logging.DEBUG):
        result = ContextAnomalyLogger.validate_and_log(context)
        assert result is False
        assert "Inconsistencias de tipo" in caplog.text
        assert "⛔ Contexto inválido detectado" in caplog.text

def test_non_dict_context(caplog):
    with caplog.at_level(logging.CRITICAL):
        result = ContextAnomalyLogger.validate_and_log(["not", "a", "dict"])
        assert result is False
        assert "El contexto no es un diccionario" in caplog.text
