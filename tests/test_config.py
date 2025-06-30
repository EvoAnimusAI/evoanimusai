import os
import json
import pytest
from core.config import Config

VALID_CONFIG = {
    "app_name": "EvoAI",
    "version": "1.0.0",
    "debug": False,
    "database_url": "sqlite:///evoai.db",
    "max_workers": 8,
    "timeout_seconds": 60
}

def write_json(tmp_path, data):
    path = tmp_path / "config.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return path

def test_load_valid_config(tmp_path):
    path = write_json(tmp_path, VALID_CONFIG)
    cfg = Config.load_from_file(str(path))
    assert cfg.app_name == VALID_CONFIG["app_name"]
    assert cfg.version == VALID_CONFIG["version"]
    assert cfg.debug == VALID_CONFIG["debug"]
    assert cfg.max_workers == VALID_CONFIG["max_workers"]
    assert cfg.timeout_seconds == VALID_CONFIG["timeout_seconds"]
    assert cfg.database_url == VALID_CONFIG["database_url"]

def test_missing_required_fields(tmp_path):
    config = VALID_CONFIG.copy()
    del config["app_name"]
    path = write_json(tmp_path, config)
    with pytest.raises(ValueError) as e:
        Config.load_from_file(str(path))
    assert "app_name" in str(e.value)

def test_invalid_types(tmp_path):
    config = VALID_CONFIG.copy()
    config["max_workers"] = 0  # invalid, must be >= 1
    path = write_json(tmp_path, config)
    with pytest.raises(ValueError):
        Config.load_from_file(str(path))

def test_env_overrides(tmp_path, monkeypatch):
    path = write_json(tmp_path, VALID_CONFIG)
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("MAX_WORKERS", "10")
    cfg = Config.load_from_file(str(path))
    assert cfg.debug is True
    assert cfg.max_workers == 10

def test_get_instance_before_load():
    Config._instance = None  # reset singleton forcibly
    with pytest.raises(RuntimeError):
        Config.get_instance()

def test_get_instance_after_load(tmp_path):
    path = write_json(tmp_path, VALID_CONFIG)
    cfg1 = Config.load_from_file(str(path))
    cfg2 = Config.get_instance()
    assert cfg1 is cfg2

def test_invalid_json(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{invalid json}", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        Config.load_from_file(str(path))

def test_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        Config.load_from_file(str(tmp_path / "nonexistent.json"))
