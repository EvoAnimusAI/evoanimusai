# tests/test_hypermutation.py

import pytest
import ast
from symbolic_ai.hypermutation import hypermutation
from unittest.mock import patch


def get_binops(expr: str):
    """Extrae todos los operadores binarios de una expresión."""
    tree = ast.parse(expr, mode='eval')
    return [type(node.op).__name__ for node in ast.walk(tree) if isinstance(node, ast.BinOp)]


def test_mutation_changes_operator():
    expr = "a + b"
    mutated = hypermutation(expr)
    assert isinstance(mutated, str)
    assert mutated != expr
    original_op = get_binops(expr)[0]
    mutated_op = get_binops(mutated)[0]
    assert original_op != mutated_op


def test_mutation_preserves_syntax():
    expr = "(x + y) * 2"
    mutated = hypermutation(expr)
    try:
        ast.parse(mutated, mode='eval')
    except SyntaxError:
        pytest.fail("La mutación produjo una expresión inválida")


def test_mutation_returns_none_on_invalid_input():
    assert hypermutation(12345) is None
    assert hypermutation(None) is None
    assert hypermutation([]) is None


def test_mutation_accepts_ast_directly():
    expr = "a - b"
    tree = ast.parse(expr, mode='eval')
    mutated = hypermutation(tree)
    assert isinstance(mutated, str)
    assert mutated != expr


@patch("random.choice", return_value=ast.Mult)  # ✅ CORREGIDO: devolvemos la clase, no la instancia
def test_mutation_is_deterministic_with_patch(mock_choice):
    expr = "a + b"
    mutated = hypermutation(expr)
    assert "*".join(expr.split("+")) in mutated or "a * b" in mutated
