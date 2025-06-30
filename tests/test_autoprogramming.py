import os
import json
import pytest
import shutil
import tempfile
import uuid
from pathlib import Path

from autoprogramming.symbolic_function import SymbolicFunction
from autoprogramming.mutation_generator import generate_and_save_mutation
from autoprogramming.mutation_evaluation import (
    memory,
    save_memory,
    evaluate_mutation,
)

@pytest.fixture(scope="function")
def temp_data_dir(monkeypatch):
    """
    Redirige el directorio de datos a un entorno temporal para pruebas seguras.
    """
    tmp_dir = tempfile.mkdtemp()
    monkeypatch.setenv("EVOAI_OUTPUT_DIR", tmp_dir)
    monkeypatch.setattr("autoprogramming.mutation_generator.OUTPUT_DIR", tmp_dir)
    monkeypatch.setattr("autoprogramming.mutation_generator.LOG_FILE", os.path.join(tmp_dir, "mutation_log.json"))
    monkeypatch.setattr("autoprogramming.mutation_evaluation.DATA_DIR", tmp_dir)
    monkeypatch.setattr("autoprogramming.mutation_evaluation.MEMORY_FILE", os.path.join(tmp_dir, "symbolic_memory.json"))
    yield tmp_dir
    shutil.rmtree(tmp_dir)

@pytest.fixture(scope="function")
def clear_memory():
    """
    Limpia memoria simbólica antes y después de cada test.
    """
    original = memory["functions"][:]
    memory["functions"].clear()
    try:
        yield
    finally:
        memory["functions"] = original
        save_memory()

class DummyContext(dict):
    def __init__(self):
        super().__init__()
        self.update({
            "entropy": 0.3,
            "energy": 80
        })

def test_generate_and_save_mutation(temp_data_dir, clear_memory):
    symbolic_function = generate_and_save_mutation()

    assert isinstance(symbolic_function, SymbolicFunction)
    assert symbolic_function.code.strip() != ""
    assert symbolic_function.name.startswith("mutation_")

    # Verifica archivo en disco
    output_path = Path(temp_data_dir) / f"{symbolic_function.name}.py"
    assert output_path.exists()
    content = output_path.read_text()
    assert symbolic_function.code.strip() in content

    # Verifica entrada en log
    log_path = Path(temp_data_dir) / "mutation_log.json"
    assert log_path.exists()
    log_data = json.loads(log_path.read_text())
    names = [entry["filename"] for entry in log_data]
    assert f"{symbolic_function.name}.py" in names

def test_memory_persistence(temp_data_dir, clear_memory):
    symbolic_function = generate_and_save_mutation()
    memory["functions"].append(symbolic_function)
    save_memory()

    memory_path = Path(temp_data_dir) / "symbolic_memory.json"
    assert memory_path.exists()
    with open(memory_path) as f:
        loaded = json.load(f)
        names = [f["name"] for f in loaded["functions"]]
        assert symbolic_function.name in names

def test_evaluate_mutation_registers(temp_data_dir, clear_memory):
    symbolic_function = generate_and_save_mutation()
    context = DummyContext()

    result = evaluate_mutation(symbolic_function, context)

    if result:
        assert symbolic_function in memory["functions"]
    else:
        assert symbolic_function not in memory["functions"]

    # Garantiza persistencia en disco coherente
    memory_path = Path(temp_data_dir) / "symbolic_memory.json"
    if memory_path.exists():
        with open(memory_path) as f:
            saved = json.load(f)
            names = [f["name"] for f in saved["functions"]]
            if result:
                assert symbolic_function.name in names
            else:
                assert symbolic_function.name not in names
