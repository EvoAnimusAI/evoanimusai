# tests/test_evoai_config.py

"""
Test de integridad para el módulo de configuración EvoAI (nivel gubernamental).
Valida constantes, rutas y estructuras requeridas por el sistema.
"""

import os
from pathlib import Path
from daemon import evoai_config as cfg


def test_daemon_key_is_secure():
    """Verifica que la clave del daemon esté definida correctamente."""
    assert isinstance(cfg.DAEMON_KEY, str)
    assert len(cfg.DAEMON_KEY) >= 20


def test_error_limits():
    """Valida que los límites de errores estén dentro de un rango razonable."""
    assert isinstance(cfg.MAX_ERRORS, int)
    assert 1 <= cfg.MAX_ERRORS <= 100


def test_cycle_parameters():
    """Verifica la validez de los parámetros de ciclos."""
    assert cfg.CYCLE_DELAY > 0
    assert cfg.CYCLES_TO_MUTATE > 0
    assert cfg.TEST_CYCLES >= 1


def test_symbolic_constants():
    """Verifica que los estados y ruidos simbólicos estén bien definidos."""
    assert isinstance(cfg.SYMBOLIC_NOISES, list)
    assert None in cfg.SYMBOLIC_NOISES
    assert isinstance(cfg.SYMBOLIC_STATES, list)
    assert "active" in cfg.SYMBOLIC_STATES


def test_directories_exist():
    """Asegura que los directorios necesarios estén presentes y accesibles."""
    assert cfg.LOG_DIR.exists() and cfg.LOG_DIR.is_dir()
    assert cfg.KNOWLEDGE_LOGS_DIR.exists() and cfg.KNOWLEDGE_LOGS_DIR.is_dir()
    assert cfg.MUTATED_FUNCTIONS_DIR.exists() and cfg.MUTATED_FUNCTIONS_DIR.is_dir()


def test_paths_are_pathlib():
    """Confirma que todas las rutas sean instancias de Path (no str)."""
    assert isinstance(cfg.LOG_DIR, Path)
    assert isinstance(cfg.MEMORY_PATH, Path)
    assert isinstance(cfg.SYMBOLIC_MEMORY_PATH, Path)


def test_learning_urls():
    """Valida que las URLs de aprendizaje estén correctamente formateadas."""
    assert isinstance(cfg.LEARNING_URLS, dict)
    for topic, url in cfg.LEARNING_URLS.items():
        assert topic and url.startswith("http")
