# tests/test_symbolic_expression.py

import pytest
from symbolic_ai.symbolic_expression import SymbolicExpression


def test_init_with_valid_types():
    assert SymbolicExpression("⟦a:b⟧ ⇒ do_something :: x > 1")
    assert SymbolicExpression(42)
    assert SymbolicExpression({"op": "add", "args": [1, 2]})


def test_init_with_invalid_type_raises():
    with pytest.raises(TypeError):
        SymbolicExpression(["not", "a", "valid", "type"])


def test_evaluate_primitive_types():
    assert SymbolicExpression(5).evaluate() == 5
    assert SymbolicExpression("constant").evaluate() == "constant"
    assert SymbolicExpression(3.14).evaluate() == 3.14


def test_evaluate_add_operation():
    expr = SymbolicExpression({"op": "add", "args": [1, 2, 3]})
    assert expr.evaluate() == 6


def test_evaluate_mul_operation():
    expr = SymbolicExpression({"op": "mul", "args": [2, 3, 4]})
    assert expr.evaluate() == 24


def test_evaluate_with_invalid_op_logs_warning(caplog):
    expr = SymbolicExpression({"op": "div", "args": [1, 2]})
    result = expr.evaluate()
    assert result is None
    assert "Unknown operation" in caplog.text


def test_evaluate_with_non_list_args_logs_warning(caplog):
    expr = SymbolicExpression({"op": "add", "args": 5})
    result = expr.evaluate()
    assert result is None
    assert "Expected 'args' to be a list" in caplog.text


def test_evaluate_with_nested_expressions():
    expr = SymbolicExpression({
        "op": "add",
        "args": [
            1,
            {"op": "mul", "args": [2, 3]}
        ]
    })
    assert expr.evaluate() == 7


def test_head_returns_operator():
    expr = SymbolicExpression({"op": "add", "args": [1]})
    assert expr.head() == "add"


def test_head_returns_none_for_non_dict():
    expr = SymbolicExpression("primitive")
    assert expr.head() is None


def test_body_extracts_action_correctly():
    expr = SymbolicExpression("⟦rol:valor⟧ ⇒ perform_action :: condition")
    assert expr.body() == "perform_action"


def test_body_returns_none_for_malformed_string():
    expr = SymbolicExpression("invalid string without separator")
    assert expr.body() is None


def test_from_dict_valid():
    data = {"op": "add", "args": [1, 2]}
    expr = SymbolicExpression.from_dict(data)
    assert isinstance(expr, SymbolicExpression)
    assert expr.evaluate() == 3


def test_from_dict_invalid_raises():
    with pytest.raises(ValueError):
        SymbolicExpression.from_dict("not a dict")


def test_from_string_valid():
    expr = SymbolicExpression.from_string("⟦a:b⟧ ⇒ act :: x > 2")
    assert isinstance(expr, SymbolicExpression)
    assert expr.body() == "act"


def test_from_string_invalid_raises():
    with pytest.raises(ValueError):
        SymbolicExpression.from_string(42)
