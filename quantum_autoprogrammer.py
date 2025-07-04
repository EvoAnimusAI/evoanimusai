# evoai/autoprogramming/quantum_autoprogrammer.py
# -*- coding: utf-8 -*-

"""
Quantum AutoProgrammer — Núcleo cuántico simbólico de EvoAI
------------------------------------------------------------
Motor de mutación y evaluación de funciones simbólicas con trazabilidad,
aprendizaje adaptativo y evolución estructural inteligente.

Nivel: Estratégico / Cuántico / Autónomo
"""

import ast
import astor
import hashlib
import logging
import time
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

# === Logger con trazabilidad ===

logger = logging.getLogger("QuantumAutoProgrammer")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# === Enums ===

class EvolutionPhase(Enum):
    EXPLORATION = "exploration"
    EXPLOITATION = "exploitation"
    TRANSCENDENCE = "transcendence"

class MutationType(Enum):
    SYNTACTIC = "syntactic"
    SEMANTIC = "semantic"
    QUANTUM = "quantum"

# === Estados y funciones ===

@dataclass
class QuantumState:
    phase: EvolutionPhase = EvolutionPhase.EXPLORATION
    entropy: float = 1.0
    coherence: float = 0.0
    observation_count: int = 0

class EnhancedSymbolicFunction:
    def __init__(self, name: str, code: str, metadata: Dict = None):
        self.name = name
        self.code = code
        self.metadata = metadata or {}
        self.quantum_signature = self._generate_quantum_signature()
        self.mutation_tree = []
        self.fitness_history = []

    def _generate_quantum_signature(self) -> str:
        payload = f"{self.name}:{self.code}:{time.time()}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "code": self.code,
            "metadata": self.metadata,
            "quantum_signature": self.quantum_signature,
            "mutation_tree": self.mutation_tree,
            "fitness_history": self.fitness_history,
        }

# === Motor Cuántico de Mutación ===

class QuantumMutationEngine:
    def __init__(self, quantum_state: QuantumState):
        self.quantum_state = quantum_state
        self.rng = random.Random(42)

    def mutate(self, func: EnhancedSymbolicFunction) -> EnhancedSymbolicFunction:
        mutation_type = self._select_mutation_type()
        logger.info(f"[Mutate] Tipo: {mutation_type.name} | Función: {func.name}")

        try:
            if mutation_type == MutationType.QUANTUM:
                code = self._apply_quantum_superposition(func.code)
            elif mutation_type == MutationType.SYNTACTIC:
                code = self._syntactic_mutation(func.code)
            elif mutation_type == MutationType.SEMANTIC:
                code = self._semantic_mutation(func.code)
            else:
                return func

            mutated = EnhancedSymbolicFunction(
                name=f"{func.name}_{mutation_type.name.lower()}",
                code=code,
                metadata={**func.metadata, "mutation_type": mutation_type.name}
            )
            mutated.mutation_tree = func.mutation_tree + [mutation_type.name]
            logger.info(f"[Mutate] Finalizada: {mutated.name}")
            return mutated

        except Exception as e:
            logger.error(f"[Mutate] Error: {e}")
            return func

    def _select_mutation_type(self) -> MutationType:
        phase = self.quantum_state.phase
        weights = {
            EvolutionPhase.EXPLORATION: [0.4, 0.4, 0.2],
            EvolutionPhase.EXPLOITATION: [0.2, 0.5, 0.3],
            EvolutionPhase.TRANSCENDENCE: [0.1, 0.3, 0.6],
        }.get(phase, [0.3, 0.4, 0.3])
        return self.rng.choices(list(MutationType), weights=weights)[0]

    def _apply_quantum_superposition(self, code: str) -> str:
        lines = code.split('\n')
        result = []
        for line in lines:
            if 'if' in line and self.rng.random() < 0.4:
                result.append(line)
                result.append(line.replace('if', 'if not'))
                logger.debug(f"[Quantum] Superposición: {line}")
            else:
                result.append(line)
        return '\n'.join(result)

    def _syntactic_mutation(self, code: str) -> str:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                old = node.name
                node.name = f"{old}_v{self.rng.randint(100,999)}"
                logger.debug(f"[Syntactic] Nombre: {old} -> {node.name}")
                break
        return astor.to_source(tree)

    def _semantic_mutation(self, code: str) -> str:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                old = node.value
                if isinstance(old, int):
                    node.value += self.rng.randint(-2, 2)
                else:
                    node.value += self.rng.uniform(-0.3, 0.3)
                logger.debug(f"[Semantic] Valor: {old} -> {node.value}")
        return astor.to_source(tree)

# === Modo Autónomo (Standalone) ===

if __name__ == "__main__":
    logger.info("[EvoAI] Inicializando Quantum AutoProgrammer...")

    state = QuantumState(phase=EvolutionPhase.TRANSCENDENCE)
    engine = QuantumMutationEngine(state)

    demo_code = '''
def demo_func(x):
    if x > 0:
        return x * 2
    else:
        return x - 1
'''
    func = EnhancedSymbolicFunction(name="demo_func", code=demo_code)
    mutated = engine.mutate(func)

    logger.info("[EvoAI] Código mutado:\n" + mutated.code)
    logger.info("[EvoAI] Árbol de mutación: " + str(mutated.mutation_tree))
