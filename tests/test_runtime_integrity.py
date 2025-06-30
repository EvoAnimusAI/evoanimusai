import os
import json
import pytest
from daemon import evoai_config as cfg

def test_symbolic_memory_format():
    """
    Verifica que el archivo de memoria simbólica sea un JSON válido,
    estructurado como diccionario con la clave 'functions' como lista.
    """
    path = cfg.SYMBOLIC_MEMORY_PATH
    if path.exists():
        try:
            content = path.read_text(encoding="utf-8")
            data = json.loads(content)

            # Validaciones estructurales
            assert isinstance(data, dict), "La memoria simbólica debe ser un diccionario"
            assert "functions" in data, "Falta la clave 'functions' en la memoria simbólica"
            assert isinstance(data["functions"], list), "'functions' debe ser una lista"

            # Validaciones opcionales (estructuras internas)
            for func in data["functions"]:
                assert isinstance(func, dict), "Cada entrada en 'functions' debe ser un diccionario"
                assert "code" in func, "Cada función debe tener una clave 'code'"
                assert isinstance(func["code"], str), "'code' debe ser un string"

        except json.JSONDecodeError as e:
            pytest.fail(f"Contenido inválido JSON en {path}: {e}")
        except Exception as e:
            pytest.fail(f"Error al validar {path}: {e}")
