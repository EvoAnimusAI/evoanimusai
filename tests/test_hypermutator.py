import pytest
from symbolic_ai.hypermutator import mutate_complete_function

def sample_function(x, y):
    """Función de ejemplo para mutar."""
    return x + y

def test_mutate_complete_function_basic():
    mutated = mutate_complete_function(sample_function)
    assert mutated is not None
    assert callable(mutated)
    assert mutated.__name__.startswith("mutated_")
    assert mutated.__doc__ is not None
    # La función mutada debe devolver lo mismo que la original
    assert mutated(3, 4) == sample_function(3, 4)

def test_mutate_complete_function_invalid_input():
    assert mutate_complete_function(None) is None
    assert mutate_complete_function(123) is None
    assert mutate_complete_function("not a function") is None

def test_mutate_complete_function_wrapper_behavior():
    mutated = mutate_complete_function(sample_function)
    assert mutated.__original_function__ == sample_function
