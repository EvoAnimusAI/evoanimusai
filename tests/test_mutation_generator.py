import os, json, tempfile, unittest, uuid
from unittest.mock import patch
from autoprogramming import mutation_generator as mg

# --- Mock mínimo de SymbolicFunction --------------------------------
class MockSF:
    def __init__(self, name, code, metadata):
        self.name, self.code, self.metadata = name, code, metadata
    def to_dict(self): return {"name": self.name, "code": self.code, "metadata": self.metadata}

# --------------------------------------------------------------------
class TestMutationGenerator(unittest.TestCase):
    def setUp(self):
        self.p_sf = patch.object(mg, "SymbolicFunction", MockSF)
        self.p_sf.start()

    def tearDown(self):
        self.p_sf.stop()

    def test_generate_mutation_basic(self):
        with patch.object(mg, "mutate_function", return_value="def foo(): pass"), \
             patch("uuid.uuid4", return_value=uuid.UUID("12345678123456781234567812345678")):
            res = mg.generate_mutation("def x(): pass", source_name="src")
        self.assertIsInstance(res, MockSF)
        self.assertIn("src_mut_", res.name)
        self.assertEqual(res.code, "def foo(): pass")

    def test_generate_and_save_mutation_creates_files_and_log(self):
        with tempfile.TemporaryDirectory() as td, \
             patch.object(mg, "OUTPUT_DIR", td), \
             patch.object(mg, "LOG_FILE", os.path.join(td, "mutation_log.json")), \
             patch.object(mg, "mutate_function", return_value="def bar(): pass"), \
             patch("inspect.getsource", return_value="def basic_advance(): pass"), \
             patch("uuid.uuid4", return_value=uuid.UUID("fedcba9876543210fedcba9876543210")):

            res = mg.generate_and_save_mutation()
            py_file = os.path.join(td, f"{res.name}.py")
            self.assertTrue(os.path.exists(py_file))
            with open(py_file) as f:
                self.assertEqual(f.read(), "def bar(): pass")

            with open(mg.LOG_FILE) as f:
                log = json.load(f)
            self.assertEqual(len(log), 1)
            self.assertEqual(log[0]["filename"], f"{res.name}.py")
