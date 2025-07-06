# core/heuristic_optimizer.py
# -*- coding: utf-8 -*-
"""
HeuristicOptimizer — Optimizador heurístico adaptativo para EvoAI

Evalúa continuamente el estado del sistema simbólico y ajusta prioridades,
entropía, o gatilla mutaciones forzadas cuando detecta patrones de estancamiento
o comportamiento no deseado.

Nivel: Militar / Autónomo / Reacción en tiempo real
"""

class HeuristicOptimizer:
    def __init__(self):
        self.entropy_threshold = 0.85
        self.max_stagnation_cycles = 15
        self.max_error_rate = 0.35

    def evaluar_condiciones_globales(self, contexto: dict) -> dict:
        resultado = {"alerta": False, "detalles": []}

        entropy = contexto.get("entropy", 0)
        error_rate = contexto.get("error_rate", 0)
        stagnation = contexto.get("cycles_without_new_rule", 0)

        if entropy > self.entropy_threshold:
            resultado["alerta"] = True
            resultado["detalles"].append(f"Entropía alta: {entropy}")

        if stagnation >= self.max_stagnation_cycles:
            resultado["alerta"] = True
            resultado["detalles"].append(f"Estancamiento detectado: {stagnation} ciclos sin nuevas reglas")

        if error_rate > self.max_error_rate:
            resultado["alerta"] = True
            resultado["detalles"].append(f"Tasa de error elevada: {error_rate}")

        return resultado

    def corregir_estado(self, contexto: dict) -> dict:
        acciones = []

        if contexto.get("entropy", 0) > self.entropy_threshold:
            acciones.append("disminuir_prioridad")

        if contexto.get("cycles_without_new_rule", 0) >= self.max_stagnation_cycles:
            acciones.append("forzar_mutacion")

        if contexto.get("error_rate", 0) > self.max_error_rate:
            acciones.append("despriorizar_acciones_fallidas")

        return {"correcciones": acciones, "estado": "ejecutado" if acciones else "estable"}
