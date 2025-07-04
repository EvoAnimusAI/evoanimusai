import os
import pytest
from pathlib import Path
from daemon.evoai_config import (
    DAEMON_KEY, MAX_ERRORS,
    CYCLE_DELAY, CYCLES_TO_MUTATE, TEST_CYCLES,
    BASE_DIR, LOG_DIR, LOG_FILE, LOG_PATH,
    KNOWLEDGE_LOGS_DIR, MUTATED_FUNCTIONS_DIR,
    SYMBOLIC_MEMORY_PATH, MEMORY_PATH,
    DEFAULT_PREFERRED_TOPICS, SYMBOLIC_NOISES, SYMBOLIC_STATES,
    LEARNING_URLS,
)

def test_constants_values():
    assert isinstance(DAEMON_KEY, str) and len(DAEMON_KEY) > 10
    assert MAX_ERRORS == 10
    assert CYCLE_DELAY > 0
    assert CYCLES_TO_MUTATE > 0
    assert TEST_CYCLES == 1

def test_paths_are_valid():
    assert BASE_DIR.exists() and BASE_DIR.is_dir()
    assert LOG_DIR.exists() and LOG_DIR.is_dir()
    assert KNOWLEDGE_LOGS_DIR.exists() and KNOWLEDGE_LOGS_DIR.is_dir()
    assert MUTATED_FUNCTIONS_DIR.exists() and MUTATED_FUNCTIONS_DIR.is_dir()

def test_log_file_path():
    assert LOG_PATH.name == LOG_FILE
    assert LOG_PATH.parent == LOG_DIR

def test_memory_paths():
    assert SYMBOLIC_MEMORY_PATH.name == "symbolic_memory.json"
    assert MEMORY_PATH.name == "symbolic_memory.json"

def test_symbolic_model_vars():
    assert isinstance(DEFAULT_PREFERRED_TOPICS, list)
    assert all(isinstance(t, str) for t in DEFAULT_PREFERRED_TOPICS)

    assert isinstance(SYMBOLIC_NOISES, list)
    assert all(t is None or isinstance(t, str) for t in SYMBOLIC_NOISES)

    assert isinstance(SYMBOLIC_STATES, list)
    assert "normal" in SYMBOLIC_STATES

def test_learning_urls():
    assert isinstance(LEARNING_URLS, dict)
    assert "symbolic evolution" in LEARNING_URLS
    assert LEARNING_URLS["symbolic evolution"].startswith("http")

@pytest.mark.parametrize("path", [
    LOG_DIR, KNOWLEDGE_LOGS_DIR, MUTATED_FUNCTIONS_DIR
])
def test_directories_created(path):
    assert path.exists()
    assert path.is_dir()
