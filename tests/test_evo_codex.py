# tests/test_evo_codex.py

import os
import tempfile
import shutil
import pytest
from core.evo_codex import EvoCodex
from symbolic_ai.symbolic_context import symbolic_context


class TestEvoCodex:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.temp_dir, "test_code.py")
        self.codex = EvoCodex(root_path=self.temp_dir)

        self.code_with_todo = "def test():\n    pass  # TODO: improve"
        self.code_without_todo = "def test():\n    pass"

    def teardown_method(self):
        shutil.rmtree(self.temp_dir)

    def test_analyze_code_success(self):
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            f.write(self.code_without_todo)
        tree, code = self.codex.analizar_codigo(self.test_file_path)
        assert tree is not None
        assert "def test()" in code

    def test_analyze_code_syntax_error(self):
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            f.write("def invalid(:\n    pass")
        tree, error = self.codex.analizar_codigo(self.test_file_path)
        assert tree is None
        assert "syntax" in error.lower()

    def test_suggest_rewrite_replaces_todo(self):
        rewritten = self.codex.sugerir_reescritura(self.code_with_todo)
        assert "# 🧠" in rewritten
        assert "based on symbolic reasoning" in rewritten.lower()

    def test_suggest_rewrite_no_todo(self):
        rewritten = self.codex.sugerir_reescritura(self.code_without_todo)
        assert rewritten == self.code_without_todo

    def test_compare_and_save_with_changes(self):
        original = self.code_with_todo
        modified = self.code_with_todo.replace("# TODO", "# 🧠 Rewrite")
        changed, log_path = self.codex.comparar_y_guardar(original, modified, self.test_file_path)
        assert changed is True
        assert os.path.exists(log_path)
        with open(self.test_file_path, encoding="utf-8") as f:
            assert "# 🧠" in f.read()

    def test_compare_and_save_without_changes(self):
        changed, log_path = self.codex.comparar_y_guardar(self.code_without_todo, self.code_without_todo, self.test_file_path)
        assert changed is False
        assert log_path is None

    def test_execute_auto_rewrite_with_change(self):
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            f.write(self.code_with_todo)

        metacog_log = []

        original = symbolic_context.register_metacognition
        symbolic_context.register_metacognition = lambda text: metacog_log.append(text)

        try:
            changed, log_path = self.codex.ejecutar_auto_reescritura(self.test_file_path)
            assert changed is True
            assert log_path is not None
            assert any("symbolic auto-rewrite applied" in t.lower() for t in metacog_log)
        finally:
            symbolic_context.register_metacognition = original

    def test_execute_auto_rewrite_without_change(self):
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            f.write(self.code_without_todo)

        metacog_log = []

        original = symbolic_context.register_metacognition
        symbolic_context.register_metacognition = lambda text: metacog_log.append(text)

        try:
            changed, log_path = self.codex.ejecutar_auto_reescritura(self.test_file_path)
            assert changed is False
            assert log_path is None
            assert any("no changes necessary" in t.lower() for t in metacog_log)
        finally:
            symbolic_context.register_metacognition = original
