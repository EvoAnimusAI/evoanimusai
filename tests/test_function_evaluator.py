# tests/test_function_evaluator.py

import pytest
from symbolic_ai.function_evaluator import evaluate_mutated_function

def test_evaluate_mutated_function_success_no_context():
    def sample_func():
        return 42

    result = evaluate_mutated_function(sample_func)
    assert result == 42

def test_evaluate_mutated_function_success_with_context():
    def sample_func(ctx):
        return ctx.get("value", 0)

    context = {"value": 99}
    result = evaluate_mutated_function(sample_func, context)
    assert result == 99

def test_evaluate_mutated_function_handles_exception(caplog):
    def faulty_func():
        raise ValueError("Intentional failure")

    with caplog.at_level("ERROR"):
        result = evaluate_mutated_function(faulty_func)
        assert result is None
        assert "Error while evaluating function" in caplog.text
        assert "Intentional failure" in caplog.text
