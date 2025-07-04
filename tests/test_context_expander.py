import pytest
from core.context_expander import ContextExpander

def test_set_and_get():
    ctx = {}
    expander = ContextExpander(ctx)
    expander.set("symbiotic_progress", 0.85)
    assert ctx["symbiotic_progress"] == 0.85
    value = expander.get("symbiotic_progress")
    assert value == 0.85

def test_set_invalid_key():
    ctx = {}
    expander = ContextExpander(ctx)
    with pytest.raises(ValueError):
        expander.set(123, "value")  # clave no es string

def test_delete_key():
    ctx = {"to_delete": 42}
    expander = ContextExpander(ctx)
    expander.delete("to_delete")
    assert "to_delete" not in ctx

def test_delete_nonexistent_key():
    ctx = {}
    expander = ContextExpander(ctx)
    # no debe lanzar error
    expander.delete("nonexistent")

def test_export_all():
    ctx = {"a": 1, "b": 2}
    expander = ContextExpander(ctx)
    exported = expander.export_all()
    assert exported == ctx
    # modificar exportado no afecta el original (es copia)
    exported["a"] = 99
    assert ctx["a"] == 1
