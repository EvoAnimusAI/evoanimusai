# tests/test_symbolic_logger.py
import pytest
import logging
import threading
import os
from symbolic_ai.symbolic_logger import SecureSymbolicLogger

@pytest.fixture
def logger_no_encrypt(tmp_path):
    log_path = tmp_path / "log_no_encrypt.jsonl"
    return SecureSymbolicLogger(log_file=str(log_path))  # Paréntesis de cierre añadido aquí

def test_basic_log_entry(logger_no_encrypt, tmp_path):
    logger = logger_no_encrypt
    logger.log("Mensaje básico", logging.INFO)
    log_file = tmp_path / "log_no_encrypt.jsonl"
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1
    import json
    entry = json.loads(lines[0])
    assert entry["message"] == "Mensaje básico"
    assert entry["level"] == "INFO"
    assert "timestamp" in entry
    assert "hostname" in entry
    assert "thread" in entry

def test_log_specialized_methods(logger_no_encrypt, tmp_path):
    logger = logger_no_encrypt
    logger.log_entry(agent="AG01", environment="Lab", cycle=7)
    logger.log_agent("AG01")
    logger.log_decision("AG01", "tipoX", "Decisión crítica")
    logger.log_synthesis("Síntesis prueba")
    logger.log_concept("ConceptoX", "sourceA")
    logger.log_learning("sourceB", "Insight importante")
    logger.log_rewrite("compA", description="Desc.", file_path="file.py")

    log_file = tmp_path / "log_no_encrypt.jsonl"
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 7
    import json
    types = [json.loads(line)["type"] for line in lines]
    expected_types = [
        "cycle_entry",
        "agent_activation",
        "agent_decision",
        "symbolic_synthesis",
        "symbolic_concept",
        "learning_event",
        "code_rewrite",
    ]
    assert types == expected_types

def test_thread_safety(logger_no_encrypt, tmp_path):
    logger = logger_no_encrypt
    def worker(i):
        logger.log(f"Mensaje concurrente #{i}", logging.INFO)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    log_file = tmp_path / "log_no_encrypt.jsonl"
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 10

def test_internal_exception_handling(monkeypatch, logger_no_encrypt):
    logger = logger_no_encrypt

    def fake_build_record(*args, **kwargs):
        raise RuntimeError("Error forzado")

    monkeypatch.setattr(logger, "_build_record", fake_build_record)

    # Debería imprimir en consola sin levantar excepción
    logger.log("Mensaje que genera excepción interna", logging.INFO)

def test_encryption_and_decryption(tmp_path):
    key = os.urandom(32)
    log_path = tmp_path / "encrypted_log.jsonl"
    logger = SecureSymbolicLogger(log_file=str(log_path), encryption_key=key)

    plaintext = "Mensaje sensible"
    logger.log(plaintext, logging.INFO)

    with open(log_path, "r", encoding="utf-8") as f:
        encrypted_line = f.readline().strip()

    # El mensaje no debe ser texto plano JSON
    assert plaintext not in encrypted_line

    # Prueba interna de desencriptado (método privado)
    decrypted_bytes = logger._decrypt(encrypted_line)
    assert plaintext == decrypted_bytes.decode("utf-8")

def test_checksum_computation(tmp_path):
    log_path = tmp_path / "check_log.jsonl"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("test\nchecksum\n")

    logger = SecureSymbolicLogger(log_file=str(log_path))
    checksum = logger._compute_file_checksum(str(log_path))
    import hashlib
    sha256 = hashlib.sha256()
    sha256.update(b"test\nchecksum\n")
    expected = sha256.hexdigest()
    assert checksum == expected
