import unittest
import os
import json

class TestEvoAIArchivos(unittest.TestCase):
    # Carpeta donde está este archivo test.py, para rutas absolutas seguras
    carpeta = os.path.dirname(os.path.abspath(__file__))

    archivos = [
        "funciones_mutadas",
        "reglas.json",
        "memoria_simbolica.json",
        "reglas_simbolicas.json",
        "mutaciones_exitosas.json",
        "symbolic_context.json",
        "regla_temporal.json",
        "symbolic_rule_engine.json"
    ]

    def test_archivos_existentes(self):
        print("\n[TEST] Verificando existencia de archivos...")
        for archivo in self.archivos:
            path = os.path.join(self.carpeta, archivo)
            print(f" - Comprobando archivo: {path}")
            self.assertTrue(os.path.isfile(path), f"Archivo {archivo} no encontrado en {path}")

    def test_json_validos(self):
        print("\n[TEST] Validando formato JSON de archivos...")
        for archivo in self.archivos:
            if archivo.endswith(".json"):
                path = os.path.join(self.carpeta, archivo)
                print(f" - Validando JSON en: {path}")
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        json.load(f)
                except Exception as e:
                    self.fail(f"Archivo JSON {archivo} inválido o no legible: {e}")

    def test_funciones_mutadas_no_vacio(self):
        path = os.path.join(self.carpeta, "funciones_mutadas")
        print(f"\n[TEST] Verificando que {path} no esté vacío")
        self.assertTrue(os.path.isfile(path), "Archivo funciones_mutadas no encontrado")
        with open(path, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            self.assertTrue(len(contenido) > 0, "Archivo funciones_mutadas está vacío")

    def test_cargar_reglas_simbolicas(self):
        path = os.path.join(self.carpeta, "reglas_simbolicas.json")
        print(f"\n[TEST] Cargando reglas simbólicas desde {path}")
        self.assertTrue(os.path.isfile(path), "Archivo reglas_simbolicas.json no encontrado")
        with open(path, "r", encoding="utf-8") as f:
            reglas = json.load(f)
            self.assertIsInstance(reglas, dict, "Reglas simbólicas no es un diccionario")

    def test_symbolic_rule_engine_integridad(self):
        path = os.path.join(self.carpeta, "symbolic_rule_engine.json")
        print(f"\n[TEST] Verificando integridad de symbolic_rule_engine en {path}")
        self.assertTrue(os.path.isfile(path), "Archivo symbolic_rule_engine.json no encontrado")
        with open(path, "r", encoding="utf-8") as f:
            contenido = json.load(f)
            # Chequeo básico: debe tener keys importantes (ejemplo)
            claves_esperadas = ["rules", "engine_version"]
            for clave in claves_esperadas:
                self.assertIn(clave, contenido, f"Clave '{clave}' faltante en symbolic_rule_engine.json")

if __name__ == "__main__":
    unittest.main()

