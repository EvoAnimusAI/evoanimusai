import os
import tempfile
import pytest
from core.evo_codex import EvoCodex

class DummyContext:
    def __init__(self):
        self.metacognitions = []
    def register_metacognition(self, msg):
        self.metacognitions.append(msg)

def test_analizar_codigo_valid(tmp_path):
    file = tmp_path / "valid.py"
    file.write_text("print('hello')")
    codex = EvoCodex()
    tree, source = codex.analizar_codigo(str(file))
    assert tree is not None
    assert "print" in source

def test_analizar_codigo_syntax_error(tmp_path):
    file = tmp_path / "bad.py"
    file.write_text("def f(:")
    codex = EvoCodex()
    tree, msg = codex.analizar_codigo(str(file))
    assert tree is None
    assert "SyntaxError" in msg

def test_sugerir_reescritura_replaces_todo():
    code = "x = 1  # TODO\nprint(x)"
    codex = EvoCodex()
    rewritten = codex.sugerir_reescritura(code)
    assert "Improved based on symbolic reasoning" in rewritten
    assert "# TODO" not in rewritten

def test_comparar_y_guardar_creates_diff_and_writes(tmp_path):
    original = "print(1)\nprint(2)"
    modified = "print(1)\nprint(3)"
    file = tmp_path / "file.py"
    file.write_text(original)
    codex = EvoCodex(root_path=str(tmp_path))
    changed, log_path = codex.comparar_y_guardar(original, modified, str(file))
    assert changed is True
    assert os.path.exists(log_path)
    with open(str(file), "r") as f:
        content = f.read()
    assert "print(3)" in content

def test_comparar_y_guardar_no_changes(tmp_path):
    code = "print(1)"
    file = tmp_path / "file.py"
    file.write_text(code)
    codex = EvoCodex(root_path=str(tmp_path))
    changed, log_path = codex.comparar_y_guardar(code, code, str(file))
    assert changed is False
    assert log_path is None

def test_execute_auto_rewrite_with_syntax_error(monkeypatch, tmp_path):
    file = tmp_path / "bad.py"
    file.write_text("def f(:")
    dummy_context = DummyContext()
    monkeypatch.setattr("core.evo_codex.symbolic_context", dummy_context)
    codex = EvoCodex()
    changed, log_path = codex.execute_auto_rewrite(str(file))
    assert changed is False
    assert log_path is None
    assert any("Syntax error detected" in m for m in dummy_context.metacognitions)

def test_execute_auto_rewrite_applies_changes(monkeypatch, tmp_path):
    code = "x = 1  # TODO"
    file = tmp_path / "file.py"
    file.write_text(code)
    dummy_context = DummyContext()
    monkeypatch.setattr("core.evo_codex.symbolic_context", dummy_context)
    codex = EvoCodex(root_path=str(tmp_path))
    changed, log_path = codex.execute_auto_rewrite(str(file))
    assert changed is True
    assert log_path is not None
    assert any("Symbolic auto-rewrite applied" in m for m in dummy_context.metacognitions)
