import builtins
import json
import os
import pytest
from unittest.mock import mock_open, patch
from core import config

VALID_CONFIG_JSON = {
    "app_name": "EvoAI",
    "version": "1.0",
    "debug": False,
    "database_url": "sqlite:///prod.db",
    "max_workers": 8,
    "timeout_seconds": 60
}

def test_load_from_file_success(monkeypatch):
    m = mock_open(read_data=json.dumps(VALID_CONFIG_JSON))
    with patch("builtins.open", m):
        cfg = config.Config.load_from_file("fake_path.json")
        assert cfg.app_name == VALID_CONFIG_JSON["app_name"]
        assert cfg.version == VALID_CONFIG_JSON["version"]
        # Singleton instance set
        assert config.Config._instance is cfg

def test_load_from_file_not_found():
    with pytest.raises(FileNotFoundError):
        config.Config.load_from_file("nonexistent.json")

def test_load_from_file_invalid_json(monkeypatch):
    m = mock_open(read_data="not a json")
    with patch("builtins.open", m):
        with pytest.raises(json.JSONDecodeError):
            config.Config.load_from_file("invalid.json")

def test_env_overrides(monkeypatch):
    m = mock_open(read_data=json.dumps(VALID_CONFIG_JSON))
    with patch("builtins.open", m):
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("MAX_WORKERS", "12")
        monkeypatch.setenv("TIMEOUT_SECONDS", "45")
        cfg = config.Config.load_from_file("dummy.json")
        assert cfg.debug is True
        assert cfg.max_workers == 12
        assert cfg.timeout_seconds == 45

def test_missing_required_fields(monkeypatch):
    data = {"debug": True}
    m = mock_open(read_data=json.dumps(data))
    with patch("builtins.open", m):
        with pytest.raises(ValueError):
            config.Config.load_from_file("missing.json")

def test_invalid_app_name(monkeypatch):
    data = {"app_name": "", "version": "1.0"}
    m = mock_open(read_data=json.dumps(data))
    with patch("builtins.open", m):
        with pytest.raises(ValueError):
            config.Config.load_from_file("invalid_app_name.json")

def test_invalid_version(monkeypatch):
    data = {"app_name": "EvoAI", "version": ""}
    m = mock_open(read_data=json.dumps(data))
    with patch("builtins.open", m):
        with pytest.raises(ValueError):
            config.Config.load_from_file("invalid_version.json")

def test_get_instance_without_load():
    config.Config._instance = None
    with pytest.raises(RuntimeError):
        config.Config.get_instance()

def test_get_instance_after_load(monkeypatch):
    m = mock_open(read_data=json.dumps(VALID_CONFIG_JSON))
    with patch("builtins.open", m):
        cfg1 = config.Config.load_from_file("file.json")
        cfg2 = config.Config.get_instance()
        assert cfg1 is cfg2
