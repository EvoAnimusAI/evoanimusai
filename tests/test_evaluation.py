import json
import os
import ast
import random
import pytest
from pathlib import Path

from autoprogramming.symbolic_function import SymbolicFunction
from autoprogramming.mutation_evaluation import (
    memory,
    evaluate_mutation,
    save_memory,
)

@pytest.fixture(autouse=True)
def clear_memory_tmp(tmp_path, monkeypatch):
    """
    Limpia la memoria antes de cada test y redirige la persistencia a tmp_path.
    """
    original = memory["functions"][:]
    memory["functions"].clear()

    # Asegurarse de que save_memory use tmp_path
    monkeypatch.setenv("AUTOPROGRAM_DATA_DIR", str(tmp_path))
    yield
    memory["functions"] = original
    save_memory(tmp_path)

def test_evaluate_mutation_rejects_invalid_code(tmp_path):
    bad_code = "def foo(:\n pass"
    bad_func = SymbolicFunction(name="bad", code=bad_code)

    with pytest.raises(SyntaxError):
        ast.parse(bad_code)

    result = evaluate_mutation(bad_func, {})
    assert result is False
    assert bad_func not in memory["functions"]

def test_evaluate_mutation_registers_success(tmp_path, monkeypatch):
    # forzamos mejora
    monkeypatch.setattr(random, "choice", lambda x: True)

    good_code = "def foo():\n  return 1"
    good_func = SymbolicFunction(name="good", code=good_code)

    result = evaluate_mutation(good_func, {})
    assert result is True
    assert good_func in memory["functions"]

    # Verificamos persistencia
    save_memory(tmp_path)
    data = json.load((tmp_path / "symbolic_memory.json").open())
    assert any(d["name"] == "good" for d in data["functions"])

def test_evaluate_mutation_rejects_success(tmp_path, monkeypatch):
    # forzamos rechazo (mejora aleatoria = False)
    monkeypatch.setattr(random, "choice", lambda x: False)

    code = "def bar():\n  return 2"
    func = SymbolicFunction(name="bar", code=code)

    result = evaluate_mutation(func, {})
    assert result is False
    assert func not in memory["functions"]
