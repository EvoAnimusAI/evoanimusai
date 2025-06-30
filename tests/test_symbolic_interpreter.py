import pytest
from symbolic_ai.symbolic_interpreter import SymbolicInterpreter
from symbolic_ai.symbolic_rule import SymbolicRule

@pytest.fixture
def interpreter():
    return SymbolicInterpreter()

@pytest.mark.parametrize("valid_rule, expected", [
    ("⟦agent:scout⟧ ⇒ move_randomly :: condition",
     SymbolicRule(rol="agent", valor="scout", accion="move_randomly", condicion="condition", texto="⟦agent:scout⟧ ⇒ move_randomly :: condition")),
    ("⟦role:value⟧ ⇒ action :: cond",
     SymbolicRule(rol="role", valor="value", accion="action", condicion="cond", texto="⟦role:value⟧ ⇒ action :: cond")),
])
def test_parse_rule_valid(interpreter, valid_rule, expected):
    result = interpreter.parse_rule(valid_rule)
    assert result.rol == expected.rol
    assert result.valor == expected.valor
    assert result.accion == expected.accion
    assert result.condicion == expected.condicion
    assert result.texto == expected.texto

@pytest.mark.parametrize("bad_rule", [
    "⟦agent scout⟧ ⇒ move_randomly :: condition",  # Missing ':'
    "⟦agent:scout⟧ move_randomly :: condition",   # Missing ⇒
    "agent:scout ⇒ move :: condition",            # Missing brackets
    "⟦agent:scout⟧ ⇒ move",                       # Missing condition
    "⟦agent:scout⟧ :: context['x'] == 1",         # Missing ⇒
    ":: context['x'] == 1",                       # Missing everything
])
def test_parse_rule_invalid_raises(interpreter, bad_rule):
    with pytest.raises(ValueError):
        interpreter.parse_rule(bad_rule)
