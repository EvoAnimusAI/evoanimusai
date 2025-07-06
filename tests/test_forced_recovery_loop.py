# tests/test_forced_recovery_loop.py
import os
import json
from core.engine import EvoAIEngine

def test_boot_creates_valid_log():
    engine = EvoAIEngine()
    engine.boot()

    path = "data/boot_log.json"
    assert os.path.exists(path), "[❌ TEST FAIL] No se creó el archivo boot_log.json"

    with open(path, "r") as f:
        data = json.load(f)

    # Validaciones clave
    assert "timestamp" in data, "[❌ TEST FAIL] Falta campo 'timestamp'"
    assert "rules_loaded" in data, "[❌ TEST FAIL] Falta campo 'rules_loaded'"
    assert "entropy" in data, "[❌ TEST FAIL] Falta campo 'entropy'"
    assert "ser_vivo" in data and data["ser_vivo"] is True, "[❌ TEST FAIL] Campo 'ser_vivo' incorrecto"
    assert "metacognition" in data, "[❌ TEST FAIL] Falta bloque 'metacognition'"
    assert "error_threshold" in data["metacognition"], "[❌ TEST FAIL] Falta 'error_threshold' en metacognition"
    assert "stagnation_limit" in data["metacognition"], "[❌ TEST FAIL] Falta 'stagnation_limit' en metacognition"

    print("[✅ TEST PASS] boot_log.json generado correctamente y con todos los campos requeridos.")
