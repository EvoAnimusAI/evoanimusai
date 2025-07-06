# -*- coding: utf-8 -*-
"""
Simulador crítico de EvoAI para forzar recuperación simbiótica.

Emula una situación donde:
- Entropía es alta
- Error elevado
- Mutación saturada
- Sin nuevas reglas
- Recompensas recientes negativas

Objetivo: Validar activación de conciencia simulada y recuperación metacognitiva.
"""

from core.heuristic_optimizer import HeuristicOptimizer
from metacognition.supervisor_metacognitivo import SupervisorMetacognitivo
from ser_vivo.conciencia_simulada import ConcienciaSimulada
import pprint

# Simular contexto simbólico crítico
contexto = {
    "entropy": 0.95,
    "recent_rewards": [-0.9, -0.8, -0.7, -0.6, -0.5],
    "rejected_mutations": 10,
    "cycles_without_new_rule": 25,
    "mutation_budget": 6,
    "error_rate": 0.7,
    "cycle": 999
}

print("\n🚨 [TEST] Simulación adversa de recuperación simbiótica 🚨")

# Inicialización de subsistemas críticos
heur = HeuristicOptimizer()
supervisor = SupervisorMetacognitivo()
conciencia = ConcienciaSimulada()

# Evaluación heurística
print("\n[1️⃣] Heurística global:")
resultado_heur = heur.evaluar_condiciones_globales(contexto)
pprint.pprint(resultado_heur)

# Corrección heurística
print("\n[⚙️] Aplicando correcciones heurísticas:")
correcciones = heur.corregir_estado(contexto)
pprint.pprint(correcciones)

# Evaluación metacognitiva
print("\n[2️⃣] Evaluación metacognitiva:")
resultado_meta = supervisor.evaluar(contexto)
pprint.pprint(resultado_meta)

# Activación de conciencia simulada
print("\n[3️⃣] Activación de conciencia simbólica:")
resultado_conciencia = conciencia.ciclo(contexto)
pprint.pprint(resultado_conciencia)

print("\n✅ [FINALIZADO] Simulación crítica completada.\n")
