import pytest
import os
from unittest.mock import patch, mock_open, MagicMock

from tools import load_new_rules

@patch("tools.load_new_rules.yaml.safe_load")
@patch("builtins.open", new_callable=mock_open, read_data="mocked: rules")
@patch("os.path.exists", return_value=True)
def test_cargar_reglas_desde_yaml(mock_exists, mock_file, mock_yaml):
    mock_yaml.return_value = [{"if": "x > 1", "then": "y = 2"}]
    reglas = load_new_rules.cargar_reglas_desde_yaml("dummy_path.yaml")
    assert isinstance(reglas, list)
    assert reglas[0]["if"] == "x > 1"

@patch("tools.load_new_rules.RuleManager")
def test_cargar_reglas_guardadas_dict(mock_mgr):
    mock_mgr.return_value.load_rules.return_value = {"rules": [{"if": "a", "then": "b"}]}
    reglas = load_new_rules.cargar_reglas_guardadas()
    assert isinstance(reglas, list)
    assert reglas[0]["if"] == "a"

@patch("tools.load_new_rules.RuleManager")
def test_cargar_reglas_guardadas_list(mock_mgr):
    mock_mgr.return_value.load_rules.return_value = [{"if": "foo", "then": "bar"}]
    reglas = load_new_rules.cargar_reglas_guardadas()
    assert isinstance(reglas, list)
    assert reglas[0]["then"] == "bar"

@patch("tools.load_new_rules.RuleManager")
def test_guardar_reglas(mock_mgr):
    reglas = [{"if": "x", "then": "y"}]
    load_new_rules.guardar_reglas(reglas)
    mock_mgr.return_value.save_rules.assert_called_once_with(reglas, filename="symbolic_rule_engine.json")

@patch("tools.load_new_rules.cargar_reglas_guardadas")
@patch("tools.load_new_rules.cargar_reglas_desde_yaml")
@patch("tools.load_new_rules.guardar_reglas")
@patch("tools.load_new_rules.RuleManager")
@patch("tools.load_new_rules.RuleEngineAdapter")
@patch("tools.load_new_rules.SymbolicLearningEngine")
def test_cargar_nuevas_reglas(mock_engine, mock_adapter, mock_mgr, mock_guardar, mock_yaml, mock_guardadas):
    mock_guardadas.return_value = [{"if": "A", "then": "B"}]
    mock_yaml.return_value = [{"if": "A", "then": "B"}, {"if": "X", "then": "Y"}]
    mock_mgr.return_value.diff_rules.return_value = [{"if": "X", "then": "Y"}]

    load_new_rules.cargar_nuevas_reglas()

    mock_guardar.assert_called_once()
    mock_adapter.assert_called_once()
    mock_engine.assert_called_once()
