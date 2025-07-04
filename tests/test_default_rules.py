import pytest
from utils.default_rules import get_default_rules

def test_get_default_rules_returns_list():
    reglas = get_default_rules()
    assert isinstance(reglas, list), "Debe retornar una lista"
    assert len(reglas) > 0, "La lista no debe estar vacía"

def test_each_rule_structure():
    for regla in get_default_rules():
        assert isinstance(regla, dict), "Cada regla debe ser un diccionario"
        assert "action" in regla, "Falta clave 'action'"
        assert "priority" in regla, "Falta clave 'priority'"
        assert isinstance(regla["action"], str), "El valor de 'action' debe ser str"
        assert isinstance(regla["priority"], float), "El valor de 'priority' debe ser float"
        assert 0.0 <= regla["priority"] <= 1.0, "La prioridad debe estar entre 0.0 y 1.0"
