import pytest
from symbolic_ai.symbolic_rule import SymbolicRule


def test_creation_valid():
    rule = SymbolicRule("admin", "active", "do_something()", "x > 0")
    assert rule.rol == "admin"
    assert rule.valor == "active"
    assert rule.accion == "do_something()"
    assert rule.condicion == "x > 0"
    assert isinstance(rule.texto, str)


def test_creation_invalid():
    with pytest.raises(ValueError):
        SymbolicRule("", "value", "accion")  # rol vacío
    with pytest.raises(ValueError):
        SymbolicRule("rol", "", "accion")  # valor vacío
    with pytest.raises(ValueError):
        SymbolicRule("rol", "val", "")  # accion vacía


def test_parse_valid():
    s = "user:online => send_alert() :: x == 5"
    rule = SymbolicRule.parse(s)
    assert rule.rol == "user"
    assert rule.valor == "online"
    assert rule.accion == "send_alert()"
    assert rule.condicion == "x == 5"
    assert rule.texto == s

    # Sin condición (debe tomar True)
    s2 = "guest:visitor => welcome_user()"
    rule2 = SymbolicRule.parse(s2)
    assert rule2.condicion == "True"


def test_parse_invalid():
    with pytest.raises(ValueError):
        SymbolicRule.parse("incorrect format without arrows")

    with pytest.raises(ValueError):
        # Cadena inválida: NO tiene ':' en antecedente (antes de =>)
        SymbolicRule.parse("rolval => accion :: missing : separator in antecedent")


def test_evaluar_true_false():
    rule = SymbolicRule("r", "v", "a", "x > 10")
    contexto = {"x": 15}
    assert rule.evaluar(contexto) is True

    contexto = {"x": 5}
    assert rule.evaluar(contexto) is False


def test_evaluar_error_handling(caplog):
    rule = SymbolicRule("r", "v", "a", "undefined_var > 0")
    with caplog.at_level("WARNING", logger="symbolic_ai.symbolic_rule"):
        resultado = rule.evaluar({})
        assert resultado is False
        assert any("Error evaluando" in record.message for record in caplog.records)


def test_to_from_dict():
    rule = SymbolicRule("role", "val", "act()", "cond == True")
    d = rule.to_dict()
    rule2 = SymbolicRule.from_dict(d)
    assert rule == rule2


def test_equality_and_repr_str():
    r1 = SymbolicRule("r", "v", "a", "True")
    r2 = SymbolicRule("r", "v", "a", "True")
    r3 = SymbolicRule("r", "v", "different", "True")

    assert r1 == r2
    assert r1 != r3

    assert str(r1).startswith("<Regla")
    assert repr(r1).startswith("SymbolicRule(texto=")
