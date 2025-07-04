import os
import json
from unittest.mock import patch
from core.self_reflection import CodeAnalyzer

def test_analyze_file_valid(tmp_path):
    file_path = tmp_path / "sample.py"
    file_path.write_text(
        "def foo():\n    pass\n\n"
        "class Bar:\n    def method(self):\n        pass\n"
    )
    analyzer = CodeAnalyzer(root_path=str(tmp_path))
    result = analyzer.analyze_file(str(file_path))
    assert result and "foo" in result["functions"] and "Bar" in result["classes"]

def test_analyze_file_syntax_error(tmp_path):
    bad_file = tmp_path / "bad.py"
    bad_file.write_text("def bad(:")
    analyzer = CodeAnalyzer(root_path=str(tmp_path))
    assert analyzer.analyze_file(str(bad_file)) is None

def test_scan_project_collects_data_and_saves(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("")
    (tmp_path / "pkg" / "mod1.py").write_text("def a():\n    pass")
    (tmp_path / "pkg" / "mod2.py").write_text("class X:\n    pass")

    summary_file = tmp_path / "summary.json"

    # Función sustituta que guarda el resumen en summary_file
    def _save(self, filename="evoai_code_summary.json"):
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(self.file_data, f, indent=2)

    with patch("core.self_reflection.CodeAnalyzer.save_summary", new=_save):
        analyzer = CodeAnalyzer(root_path=str(tmp_path))
        analyzer.scan_project()

    assert summary_file.exists()
    data = json.loads(summary_file.read_text())
    assert any("mod1.py" in p for p in data)
    assert any("mod2.py" in p for p in data)
    for item in data.values():
        assert "functions" in item and "classes" in item
