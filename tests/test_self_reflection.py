import os
import json
import pytest
from core.self_reflection import CodeAnalyzer

TEST_DIR = "tests/test_sample_project"

@pytest.fixture(scope="module")
def setup_test_dir(tmp_path_factory):
    # Crear estructura de directorios y archivos para pruebas
    base_dir = tmp_path_factory.mktemp("test_sample_project")

    # Archivo válido Python
    valid_file = base_dir / "valid.py"
    valid_file.write_text(
        "def foo():\n    pass\n\nclass Bar:\n    pass\n"
    )

    # Archivo con error de sintaxis
    syntax_error_file = base_dir / "syntax_error.py"
    syntax_error_file.write_text(
        "def broken(:\n    pass\n"
    )

    # Archivo no existente no se crea para test negativo

    # Directorio ignorado con archivo python (no debe ser analizado)
    ignored_dir = base_dir / "venv"
    ignored_dir.mkdir()
    ignored_file = ignored_dir / "ignored.py"
    ignored_file.write_text("def ignored_func(): pass")

    yield base_dir

def test_analyze_file_valid(setup_test_dir):
    analyzer = CodeAnalyzer(root_path=str(setup_test_dir))
    analysis = analyzer.analyze_file(str(setup_test_dir / "valid.py"))
    assert analysis is not None
    assert "foo" in analysis["functions"]
    assert "Bar" in analysis["classes"]

def test_analyze_file_invalid(setup_test_dir, caplog):
    analyzer = CodeAnalyzer(root_path=str(setup_test_dir))
    # Prueba archivo con error sintaxis retorna None y loggea error
    with caplog.at_level("ERROR"):
        result = analyzer.analyze_file(str(setup_test_dir / "syntax_error.py"))
    assert result is None
    assert any("Error parsing" in record.message for record in caplog.records)

    # Prueba archivo no existente retorna None y loggea error
    with caplog.at_level("ERROR"):
        result = analyzer.analyze_file(str(setup_test_dir / "nonexistent.py"))
    assert result is None
    assert any("Error parsing" in record.message for record in caplog.records)

def test_scan_project_ignores_dirs_and_files(setup_test_dir):
    analyzer = CodeAnalyzer(root_path=str(setup_test_dir))
    analyzer.scan_project()
    files = list(analyzer.file_data.keys())

    # Debe analizar valid.py
    assert any("valid.py" in f for f in files)
    # No debe analizar archivos en venv (ignored.py)
    assert all("venv" not in f for f in files)
    # No debe tener archivos con error de sintaxis (syntax_error.py no debería estar)
    assert all("syntax_error.py" not in f for f in files)

def test_save_summary_creates_file(tmp_path):
    analyzer = CodeAnalyzer(root_path=".")
    analyzer.file_data = {
        "file1.py": {"functions": ["foo"], "classes": ["Bar"]}
    }
    summary_file = tmp_path / "summary.json"
    analyzer.save_summary(str(summary_file))
    assert summary_file.exists()

    data = json.loads(summary_file.read_text())
    assert "file1.py" in data
    assert data["file1.py"]["functions"] == ["foo"]
    assert data["file1.py"]["classes"] == ["Bar"]

def test_summarize_returns_file_data():
    analyzer = CodeAnalyzer()
    analyzer.file_data = {
        "file.py": {"functions": ["f"], "classes": ["C"]}
    }
    summary = analyzer.summarize()
    assert summary == analyzer.file_data
