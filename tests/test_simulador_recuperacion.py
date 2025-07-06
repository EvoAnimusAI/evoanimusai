# -*- coding: utf-8 -*-
"""
Test automatizado para validar recuperación simbiótica crítica.

Verifica que ante un contexto simbólico adverso:
- Se detecten condiciones críticas
- Se activen mecanismos de conciencia simulada
- Se inicie recuperación metacognitiva

Nivel: Militar / Gubernamental
"""

import pytest
from core.heuristic_optimizer import HeuristicOptimizer
from metacognition.supervisor_metacognitivo import SupervisorMetacognitivo
from ser_vivo.conciencia_simulada import ConcienciaSimulada

@pytest.fixture
def contexto_critico():
    return {
        "entropy": 0.95,
        "recent_rewards": [-0.9, -0.8, -0.7, -0.6, -0.5],
        "rejected_mutations": 10,
        "cycles_without_new_rule": 25,
        "mutation_budget": 6,
        "error_rate": 0.7,
        "cycle": 999
    }

def test_heuristic_detecta_alerta(contexto_critico):
    heur = HeuristicOptimizer()
    resultado = heur.evaluar_condiciones_globales(contexto_critico)
    assert resultado["alerta"] is True
    assert "estancamiento evolutivo" in resultado["detalles"].lower()

def test_supervisor_detecta_estancamiento(contexto_critico):
    supervisor = SupervisorMetacognitivo()
    resultado = supervisor.evaluar(contexto_critico)
    assert resultado["status"] in ["halted", "recovered"]

def test_conciencia_simulada_activa(contexto_critico):
    conciencia = ConcienciaSimulada()
    salida = conciencia.ciclo(contexto_critico)
    assert isinstance(salida, dict)
    assert salida.get("estado") == "ok"
    assert "mutacion" in salida
