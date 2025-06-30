import pytest
from symbolic_ai.interpreter import ExpresionSimbolica


def test_creacion_exitosa():
    expr = ExpresionSimbolica("x + y")
    assert expr.expresion == "x + y"


def test_creacion_tipo_invalido():
    with pytest.raises(TypeError):
        ExpresionSimbolica(123)


def test_evaluacion_sin_contexto():
    expr = ExpresionSimbolica("x + y")
    result = expr.evaluar()
    assert isinstance(result, str)
    assert result == "x + y"


def test_evaluacion_con_contexto_simple():
    expr = ExpresionSimbolica("x + y")
    result = expr.evaluar({"x": "1", "y": "2"})
    assert "1" in result and "2" in result


def test_evaluacion_con_contexto_parcial():
    expr = ExpresionSimbolica("x + y + z")
    result = expr.evaluar({"x": "1"})
    assert "1" in result
    assert "y" in result and "z" in result


def test_evaluacion_contexto_con_clave_no_str(caplog):
    expr = ExpresionSimbolica("x + y")
    with caplog.at_level("WARNING", logger="evoai.interpreter"):
        result = expr.evaluar({42: "invalid", "x": "1"})
        assert "1" in result
        assert any("Variable de contexto inválida" in message for message in caplog.messages)


def test_repr():
    expr = ExpresionSimbolica("x + y")
    assert repr(expr) == "<ExpresionSimbolica: x + y>"


def test_evaluacion_error_interno():
    expr = ExpresionSimbolica("x + y")

    class FakeContext:
        def items(self):
            raise RuntimeError("Fallo forzado durante evaluación")

    with pytest.raises(ValueError, match="Error evaluando expresión: Fallo forzado durante evaluación"):
        expr.evaluar(FakeContext())
