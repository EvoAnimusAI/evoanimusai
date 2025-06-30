import pytest
from autoprogramming.mutation_operator import (
    generate_function_name,
    generate_class_name,
    mutate_function
)

@pytest.fixture
def seeded_rng():
    import random
    rng = random.Random(42)
    return rng

def test_generate_function_name_format(seeded_rng):
    name = generate_function_name(seeded_rng)
    assert name.startswith("func_")
    assert len(name) == 11
    assert all(c.islower() for c in name[5:])

def test_generate_class_name_format(seeded_rng):
    name = generate_class_name(seeded_rng)
    assert name.startswith("Class_")
    assert len(name) == 10  # "Class_" + 4 letras
    assert all(c.isupper() for c in name[6:])  # Solo sufijo aleatorio

def test_mutate_function_changes_name(seeded_rng):
    code = """
def hello():
    return 42
"""
    mutated = mutate_function(code, rng=seeded_rng, force_all_mutations=True)
    assert "hello" not in mutated
    assert "def func_" in mutated

def test_mutate_if_condition_negation(seeded_rng):
    code = """
def check(x):
    if x > 0:
        return True
    return False
"""
    mutated = mutate_function(code, rng=seeded_rng, force_all_mutations=True)
    assert "if not" in mutated or "ast.UnaryOp" in mutated

def test_mutate_try_body_else_swap_and_exception_name_change(seeded_rng):
    code = """
def risky():
    try:
        print("ok")
    except Exception:
        print("fail")
    else:
        print("done")
"""
    mutated = mutate_function(code, rng=seeded_rng, force_all_mutations=True)
    assert "Exception" in mutated
    except_clause = mutated.split("except ")[1].split(":")[0].strip()
    assert except_clause != "Exception"
    assert "Exception" in except_clause
