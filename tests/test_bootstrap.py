import os
import json
import pytest
from pathlib import Path
from evoai_bootstrap import bootstrap_evoai
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine
from symbolic_ai.symbolic_context import SymbolicContext


@pytest.fixture(autouse=True)
def cleanup_data_dir():
    """Elimina archivos temporales generados por bootstrap al finalizar los tests."""
    yield
    for file in Path("data").glob("symbolic_rules_snapshot_*.json"):
        file.unlink()


def test_bootstrap_returns_engine_and_context():
    engine, context = bootstrap_evoai()
    assert isinstance(engine, SymbolicRuleEngine)
    assert isinstance(context, SymbolicContext)


def test_bootstrap_with_context_data():
    context_data = {"mode": "evaluation", "debug": True}
    _, context = bootstrap_evoai(context_data=context_data)
    assert context["mode"] == "evaluation"
    assert context["debug"] is True


def test_bootstrap_with_invalid_context_raises():
    with pytest.raises(TypeError):
        bootstrap_evoai(context_data="no_es_un_dict")


def test_bootstrap_with_custom_rules_persists_file():
    # Reglas con formato válido esperado: 'rol:valor => accion :: condicion'
    custom_rules = [
        "temperature:>37 => alert = 'fever' :: True",
        "humidity:<20 => status = 'dry' :: True"
    ]

    engine, _ = bootstrap_evoai(custom_rules=custom_rules)
    assert len(engine.rules) >= 2  # Puede haber reglas preexistentes

    # Verifica que el archivo snapshot se haya creado correctamente
    snapshots = list(Path("data").glob("symbolic_rules_snapshot_*.json"))
    assert len(snapshots) == 1

    # Valida formato JSON y contenido esperado
    with open(snapshots[0], encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict)
    assert "rules" in data


def test_bootstrap_with_invalid_custom_rules_raises():
    with pytest.raises(ValueError):
        # Mezcla regla válida y no válida (no string)
        bootstrap_evoai(custom_rules=["valid_rule:1 => action :: True", 1234])
