import os
import json
import pytest
import shutil
import tempfile
from pathlib import Path

from autoprogramming.symbolic_function import SymbolicFunction
from autoprogramming.mutation_generator import generate_and_save_mutation

def test_generate_and_save_mutation_creates_file_and_log():
    tmp_dir = tempfile.mkdtemp(prefix="evoai_test_")
    try:
        os.environ["EVOAI_OUTPUT_DIR"] = tmp_dir
        # Ajustar variables internas del módulo
        import autoprogramming.mutation_generator as mg
        mg.OUTPUT_DIR = tmp_dir
        mg.LOG_FILE = os.path.join(tmp_dir, "mutation_log.json")

        symbolic_function = generate_and_save_mutation()

        # Tipo y formato básico
        assert isinstance(symbolic_function, SymbolicFunction)
        assert symbolic_function.code.strip() != ""
        assert symbolic_function.name.startswith("mutation_")

        # Archivo en disco
        output_path = Path(tmp_dir) / f"{symbolic_function.name}.py"
        assert output_path.exists()
        content = output_path.read_text()
        assert symbolic_function.code.strip() in content

        # Archivo log actualizado
        log_path = Path(tmp_dir) / "mutation_log.json"
        assert log_path.exists()
        log_data = json.loads(log_path.read_text())
        filenames = [entry["filename"] for entry in log_data]
        assert f"{symbolic_function.name}.py" in filenames

    finally:
        shutil.rmtree(tmp_dir)

def test_generated_code_is_valid_python():
    tmp_dir = tempfile.mkdtemp(prefix="evoai_test_")
    try:
        os.environ["EVOAI_OUTPUT_DIR"] = tmp_dir
        import autoprogramming.mutation_generator as mg
        mg.OUTPUT_DIR = tmp_dir
        mg.LOG_FILE = os.path.join(tmp_dir, "mutation_log.json")

        symbolic_function = generate_and_save_mutation()

        try:
            compile(symbolic_function.code, "<string>", "exec")
        except SyntaxError as e:
            pytest.fail(f"Código generado inválido: {e}")

    finally:
        shutil.rmtree(tmp_dir)
