import json
import pytest
from pathlib import Path

from autoprogramming.mutation_generator import generate_and_save_mutation
from autoprogramming.mutation_evaluation import memory, save_memory

@pytest.fixture(scope="function", autouse=True)
def clear_memory():
    """Limpia la memoria simbólica antes y después de cada test."""
    original = memory["functions"][:]
    memory["functions"].clear()
    yield
    memory["functions"] = original
    save_memory()  # Se guarda en la ubicación por defecto al finalizar el test

def test_memory_persistence(tmp_path):
    symbolic_function = generate_and_save_mutation()
    memory["functions"].append(symbolic_function)
    # Se guarda la memoria en el directorio temporal (tmp_path)
    save_memory(tmp_path)

    memory_path = Path(tmp_path) / "symbolic_memory.json"
    assert memory_path.exists(), f"No se encontró el archivo en {memory_path}"

    with memory_path.open() as f:
        loaded = json.load(f)
        names = [record["name"] for record in loaded["functions"]]
        assert symbolic_function.name in names, "El nombre de la función no se encuentra en la memoria persistida"
