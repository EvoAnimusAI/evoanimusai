# tools/load_new_rules.py
# -*- coding: utf-8 -*-
"""
Herramienta para cargar, versionar y actualizar reglas simbólicas en EvoAnimusAI.
Carga reglas desde archivo YAML o JSON, las versiona, guarda y las inyecta en el motor simbólico.
"""

import logging
import yaml
import json
import os
from core.engine import RuleEngineAdapter
from symbolic_ai.symbolic_learning_engine import SymbolicLearningEngine
from symbolic_ai.rule_manager import RuleManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("load_new_rules")

RULES_PATH = "data/rules"
RULES_FILENAME = "default_rules.yaml"
STORAGE_FILENAME = "symbolic_rule_engine_consolidated.json"

def cargar_reglas_desde_yaml(path: str) -> list[dict]:
    if not os.path.exists(path):
        logger.error(f"Archivo de reglas no encontrado: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        reglas = yaml.safe_load(f)
    logger.info(f"Cargadas {len(reglas)} reglas desde YAML.")
    return reglas

def cargar_reglas_guardadas() -> list[dict]:
    manager = RuleManager(storage_path=RULES_PATH)
    reglas = manager.load_rules(filename=STORAGE_FILENAME)

    if isinstance(reglas, dict) and "rules" in reglas:
        logger.warning("El archivo contiene un diccionario con clave 'rules'. Corrigiendo...")
        return reglas["rules"]
    elif isinstance(reglas, list):
        return reglas
    else:
        logger.error("Formato no soportado en archivo de reglas guardadas.")
        return []

def guardar_reglas(reglas: list[dict]) -> None:
    manager = RuleManager(storage_path=RULES_PATH)
    manager.save_rules(reglas, filename=STORAGE_FILENAME)
    logger.info(f"Reglas guardadas correctamente en {STORAGE_FILENAME}.")

def cargar_nuevas_reglas():
    logger.info("🚀 Iniciando carga de nuevas reglas simbólicas...")

    # Cargar reglas actuales guardadas
    reglas_anteriores = cargar_reglas_guardadas()
    logger.info(f"Tipo de reglas_anteriores: {type(reglas_anteriores)}")

    # Cargar reglas nuevas desde YAML
    ruta_yaml = os.path.join(RULES_PATH, RULES_FILENAME)
    reglas_nuevas = cargar_reglas_desde_yaml(ruta_yaml)

    if not reglas_nuevas:
        logger.warning("No se encontraron reglas nuevas para cargar.")
        return

    # Comparar diferencias
    manager = RuleManager(storage_path=RULES_PATH)
    reglas_diferentes = manager.diff_rules(reglas_anteriores, reglas_nuevas)

    if not reglas_diferentes:
        logger.info("No hay reglas nuevas para agregar. Finalizando proceso.")
        return

    logger.info(f"Se detectaron {len(reglas_diferentes)} reglas nuevas a agregar.")

    # Actualizar conjunto de reglas
    if not isinstance(reglas_anteriores, list):
        reglas_anteriores = []
    reglas_actualizadas = reglas_anteriores + reglas_diferentes

    # Guardar reglas actualizadas
    guardar_reglas(reglas_actualizadas)

    # Inicializar motor simbólico con reglas actualizadas
    adapter = RuleEngineAdapter(reglas_actualizadas)
    engine = SymbolicLearningEngine(rule_engine=adapter)

    logger.info("Motor de aprendizaje simbólico inicializado con reglas actualizadas.")

if __name__ == "__main__":
    cargar_nuevas_reglas()
