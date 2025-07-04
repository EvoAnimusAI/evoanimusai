# evoai_state.py
# -*- coding: utf-8 -*-
""" Manejo del state simbólico y funcional del Daemon EvoAI (nivel gubernamental). """

import os
import json
import random
import logging
import time

logger = logging.getLogger("EvoAI.State")

MEMORY_PATH = "symbolic_memory.json"
CYCLES_TO_MUTATE = 10

# Estado funcional inicial
cycle_counter = 0
current_function = {
    "name": "base_function",
    "steps": [
        {"action": "calm_down", "param": 1.0},
        {"action": "slow_down", "param": 2.0}
    ]
}
preferred_topics = ["calm_down", "slow_down"]


def ensure_logs_dir():
    os.makedirs("knowledge_logs", exist_ok=True)


def load_memory():
    global current_function
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            current_function = json.load(f)


def save_memory():
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(current_function, f, indent=2, ensure_ascii=False)


def get_symbolic_context():
    """ Genera un contexto simbólico dinámico y semántico. """
    return {
        'noise': random.choice(["neutral", "harmonic", "chaos", "tension", "calm", None]),
        'state': random.choice(["normal", "active", "stressed"])
    }


def execute_directed_function(func: dict):
    """ Ejecuta paso a paso una función simbólicamente dirigida. """
    logger.info(f"[Directed] Ejecutando función dirigida: {func.get('name')}")
    for step in func.get("steps", []):
        logger.info(f"  • Acción: {step.get('action')} | Param: {step.get('param')}")


def save_to_symbolic_memory(code: str):
    path = "data/symbolic_memory.json"
    memory = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            memory = json.load(f)
    memory.append({"code": code, "origin": "mutation"})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


def update_cycle_counter():
    global cycle_counter
    cycle_counter += 1
    return cycle_counter
