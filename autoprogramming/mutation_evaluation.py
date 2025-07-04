# evoai/autoprogramming/mutation_evaluation.py

import json
import os
import random
import ast
from autoprogramming.symbolic_function import SymbolicFunction

# Configuración de persistencia
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
MEMORY_FILE = os.path.join(DATA_DIR, "symbolic_memory.json")

# Memoria simbólica (lista de funciones exitosas)
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        raw_memory = json.load(f)
        memory = {
            "functions": [
                SymbolicFunction.from_dict(d) for d in raw_memory.get("functions", [])
                if isinstance(d, dict) and "name" in d and "code" in d
            ]
        }
else:
    memory = {"functions": []}


def evaluate_mutation(new_function: SymbolicFunction, current_context: dict) -> bool:
    """
    Evalúa si una función simbólica mutada mejora el sistema.
    Primero valida sintácticamente el código con ast.parse.

    :param new_function: instancia de SymbolicFunction mutada
    :param current_context: contexto simbólico actual
    :return: bool indicando si se considera mejora
    """
    # Validación sintáctica estricta
    try:
        ast.parse(new_function.code)
    except SyntaxError:
        mark_for_debugging(new_function)
        return False  # Código inválido, rechazo inmediato

    # Evaluación aleatoria provisional (futuro: métrica simbólica)
    improvement = random.choice([True, False])

    if improvement:
        register_successful_function(new_function)
    else:
        mark_for_debugging(new_function)

    return improvement


def register_successful_function(func: SymbolicFunction):
    memory["functions"].append(func)
    save_memory()


def mark_for_debugging(func: SymbolicFunction):
    # TODO: implementar sistema de revisión
    pass


def save_memory(output_dir=None):
    """
    Guarda la memoria simbólica como JSON.

    :param output_dir: directorio donde guardar el archivo.
                       Si no se especifica, usa la ubicación por defecto.
    """
    dir_path = output_dir or DATA_DIR
    os.makedirs(dir_path, exist_ok=True)
    target = os.path.join(dir_path, "symbolic_memory.json")
    serializable = {"functions": [f.to_dict() for f in memory["functions"]]}
    with open(target, "w") as f:
        json.dump(serializable, f, indent=2)
