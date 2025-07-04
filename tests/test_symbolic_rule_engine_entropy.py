# tests/test_symbolic_rule_engine_entropy.py

import pytest
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine
from symbolic_ai.symbolic_rule import SymbolicRule


@pytest.fixture
def regla_entropy():
    return SymbolicRule.parse("⟦action:explore⟧ ⇒ move_forward :: entropy > 0.5")


def test_regla_entropy_mayor_05_activa(regla_entropy):
    contexto = {"entropy": 0.8}
    engine = SymbolicRuleEngine([regla_entropy])
    activas = engine.evaluate(contexto)
    assert len(activas) == 1
    assert activas[0].accion == "move_forward"
    print("✅ test_regla_entropy_mayor_05_activa pasó correctamente")


def test_regla_entropy_menor_igual_05_no_activa(regla_entropy):
    contexto = {"entropy": 0.2}
    engine = SymbolicRuleEngine([regla_entropy])
    activas = engine.evaluate(contexto)
    assert len(activas) == 0
    print("✅ test_regla_entropy_menor_igual_05_no_activa pasó correctamente")
