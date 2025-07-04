import logging
import pytest
from core.input_sanitizer import InputSanitizer

def test_sanitize_defaults_applied(caplog):
    sanitizer = InputSanitizer()
    obs = {'noise': None, 'state': None}
    with caplog.at_level(logging.WARNING):
        sanitized = sanitizer.sanitize(obs)
    assert sanitized['noise'] == 'calm'
    assert sanitized['state'] == 'unknown'
    assert sanitized.get('pos') == 0
    # Verificar que se emitieron las advertencias correspondientes
    warnings = [rec for rec in caplog.records if rec.levelname == "WARNING"]
    assert any("Variable 'noise' era None" in w.message for w in warnings)
    assert any("Variable 'state' era None" in w.message for w in warnings)

def test_sanitize_keeps_valid_values():
    sanitizer = InputSanitizer()
    obs = {'noise': 'chaos', 'state': 'active', 'pos': 5}
    sanitized = sanitizer.sanitize(obs)
    assert sanitized['noise'] == 'chaos'
    assert sanitized['state'] == 'active'
    assert sanitized['pos'] == 5

def test_sanitize_adds_missing_keys():
    sanitizer = InputSanitizer()
    obs = {}
    sanitized = sanitizer.sanitize(obs)
    assert sanitized['noise'] == 'calm'
    assert sanitized['state'] == 'unknown'
    assert sanitized['pos'] == 0
