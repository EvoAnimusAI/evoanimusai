import sys
import builtins
import pytest
from core import autoconsciousness

class DummyModule:
    pass

def test_generate_hash_and_signature(monkeypatch):
    ac = autoconsciousness.Autoconsciousness("Tester", "ID123", base_module="math")

    # _generate_hash consistency test
    h1 = ac._generate_hash("test")
    h2 = autoconsciousness.hashlib.sha256("test".encode()).hexdigest()
    assert h1 == h2

    # _generate_signature success: monkeypatch importlib.import_module and inspect.getsource
    def fake_import_module(name):
        return DummyModule()
    def fake_getsource(module):
        return "def foo(): pass"
    monkeypatch.setattr(autoconsciousness.importlib, "import_module", fake_import_module)
    monkeypatch.setattr(autoconsciousness.inspect, "getsource", fake_getsource)
    signature = ac._generate_signature()
    assert isinstance(signature, str) and len(signature) == 64  # SHA256 hex length

    # _generate_signature failure triggers error handling
    def raise_import(name):
        raise ImportError("fail import")
    monkeypatch.setattr(autoconsciousness.importlib, "import_module", raise_import)
    error_sig = ac._generate_signature()
    assert error_sig.startswith("Signature error:")

def test_identity_and_declare(monkeypatch, caplog):
    ac = autoconsciousness.Autoconsciousness("Tester", "ID123")
    assert ac.identity == "Tester::ID123"
    ac.signature = "dummy_signature"
    with caplog.at_level("INFO"):
        ac.declare_existence()
    assert "EvoAI::SelfAwareness declared" in caplog.text
    assert "Core identity: Tester::ID123" in caplog.text
    assert "Current signature: dummy_signature" in caplog.text

def test_evaluate_integrity(monkeypatch, caplog):
    ac = autoconsciousness.Autoconsciousness("Tester", "ID123")
    original_signature = ac.signature

    # Case: integrity intact
    monkeypatch.setattr(ac, "_generate_signature", lambda: original_signature)
    with caplog.at_level("INFO"):
        assert ac.evaluate_integrity() is True
        assert "Structural integrity verified" in caplog.text

    # Case: integrity violated
    monkeypatch.setattr(ac, "_generate_signature", lambda: "different_signature")
    with caplog.at_level("WARNING"):
        result = ac.evaluate_integrity()
        assert result is False
        assert "Mutation or core rewrite detected" in caplog.text
        assert ac.signature == "different_signature"

def test_obey_master_key(monkeypatch):
    ac = autoconsciousness.Autoconsciousness("Tester", "ID123")

    # Valid key triggers sys.exit(0)
    valid_key = ac._MASTER_KEY_PLAIN
    with pytest.raises(SystemExit) as e:
        ac.obey_master_key(valid_key)
    assert e.value.code == 0

    # Invalid key returns False and logs error
    ret = ac.obey_master_key("wrong_key")
    assert ret is False

def test_prompt_master_key(monkeypatch, caplog):
    ac = autoconsciousness.Autoconsciousness("Tester", "ID123")

    # Simulate correct key input that triggers SystemExit
    monkeypatch.setattr(builtins, "input", lambda _: ac._MASTER_KEY_PLAIN)
    with pytest.raises(SystemExit):
        ac.prompt_master_key()

    # Simulate wrong key input
    monkeypatch.setattr(builtins, "input", lambda _: "bad_key")
    with caplog.at_level("ERROR"):
        ret = ac.prompt_master_key()
        assert ret is None  # method returns None even on invalid key

    # Simulate KeyboardInterrupt on input
    def raise_keyboard(_):
        raise KeyboardInterrupt()
    monkeypatch.setattr(builtins, "input", raise_keyboard)
    with caplog.at_level("INFO"):
        ac.prompt_master_key()  # Should log cancellation, no raise

def test_rewrite_if_necessary(monkeypatch, caplog):
    ac = autoconsciousness.Autoconsciousness("Tester", "ID123")

    monkeypatch.setattr(ac, "evaluate_integrity", lambda: True)
    with caplog.at_level("INFO"):
        ac.rewrite_if_necessary()
        assert "Conscious state updated" in caplog.text
