import pytest
from symbolic_ai.symbolic_evaluator import SymbolicEvaluator
import logging


def test_init_valid_and_invalid():
    # Valido
    ev = SymbolicEvaluator("⟦r:v⟧ ⇒ a :: True")
    assert ev.rule_text == "⟦r:v⟧ ⇒ a :: True"

    # Inválido: no string o string vacío
    with pytest.raises(ValueError):
        SymbolicEvaluator("")
    with pytest.raises(ValueError):
        SymbolicEvaluator(None)
    with pytest.raises(ValueError):
        SymbolicEvaluator(123)


def test_extract_condition_basic():
    ev = SymbolicEvaluator("⟦rol:val⟧ ⇒ acc :: x > 0")
    cond = ev.extract_condition()
    assert cond == "x > 0"

    ev2 = SymbolicEvaluator("sin condición")
    cond2 = ev2.extract_condition()
    assert cond2 == ""


def test_evaluate_true_and_false(monkeypatch):
    ev = SymbolicEvaluator("⟦rol:val⟧ ⇒ acc :: x == 10")

    # Caso True
    result_true = ev.evaluate({"x": 10})
    assert result_true is True

    # Caso False
    result_false = ev.evaluate({"x": 5})
    assert result_false is False


def test_evaluate_condition_not_bool(monkeypatch, caplog):
    ev = SymbolicEvaluator("⟦rol:val⟧ ⇒ acc :: 'not bool'")

    # Simulamos que la condición retorna string, no bool
    with caplog.at_level(logging.WARNING):
        result = ev.evaluate({})
        assert result is False
        assert "Evaluación no retornó bool" in caplog.text


def test_evaluate_invalid_expression_logs_error(caplog):
    ev = SymbolicEvaluator("⟦rol:val⟧ ⇒ acc :: invalid_var > 5")

    with caplog.at_level(logging.ERROR):
        result = ev.evaluate({})
        assert result is False
        assert "Error evaluando condición" in caplog.text


def test_evaluate_empty_condition_returns_false(caplog):
    ev = SymbolicEvaluator("Regla sin condición")

    with caplog.at_level(logging.WARNING):
        result = ev.evaluate({"x": 1})
        assert result is False
        assert "No se encontró condición" in caplog.text
