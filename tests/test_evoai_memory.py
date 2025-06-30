# tests/test_evoai_memory.py
# -*- coding: utf-8 -*-
""" Tests de nivel gubernamental para evoai_memory.py """

import os
import json
import tempfile
import shutil
import unittest
from unittest.mock import patch
from daemon import evoai_memory


class TestEvoAIMemory(unittest.TestCase):

    def setUp(self):
        # Crear un directorio temporal aislado para pruebas
        self.test_dir = tempfile.mkdtemp()
        self.symbolic_file = os.path.join(self.test_dir, "symbolic_memory.json")
        self.function_file = os.path.join(self.test_dir, "function_memory.json")

        # Parchar rutas internas del módulo
        self.symbolic_patch = patch.object(evoai_memory, "SYMBOLIC_MEMORY_FILE", self.symbolic_file)
        self.function_patch = patch.object(evoai_memory, "FUNCTION_MEMORY_FILE", self.function_file)
        self.symbolic_patch.start()
        self.function_patch.start()

    def tearDown(self):
        # Detener parches y eliminar directorio temporal
        self.symbolic_patch.stop()
        self.function_patch.stop()
        shutil.rmtree(self.test_dir)

    def test_load_symbolic_memory_when_file_missing(self):
        self.assertEqual(evoai_memory.load_symbolic_memory(), [])

    def test_append_and_load_symbolic_memory(self):
        entry = {"origin": "test", "content": "unit test"}
        evoai_memory.append_to_symbolic_memory(entry)
        data = evoai_memory.load_symbolic_memory()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["origin"], "test")

    def test_save_and_load_function_memory(self):
        function_data = {"name": "unit_function", "steps": [{"action": "test", "param": 0.1}]}
        evoai_memory.save_function_memory(function_data)
        loaded = evoai_memory.load_function_memory()
        self.assertEqual(loaded["name"], "unit_function")
        self.assertEqual(len(loaded["steps"]), 1)

    def test_load_function_memory_with_missing_file_returns_default(self):
        result = evoai_memory.load_function_memory()
        self.assertEqual(result["name"], "base_function")
        self.assertEqual(result["steps"][0]["action"], "calm_down")


if __name__ == "__main__":
    unittest.main()
