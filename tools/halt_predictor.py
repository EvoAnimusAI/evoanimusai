# -*- coding: utf-8 -*-
"""
HaltPredictor — Predicción anticipada de eventos HALT mediante heurísticas simbólicas
Nivel: Cibernético / Análisis Preventivo / Auditoría Evolutiva
"""

import json
import os
from pathlib import Path
import numpy as np

class HaltPredictor:
    def __init__(self, log_path="logs/halt_events.json"):
        self.log_path = Path(log_path)
        self.historial = []
        self._cargar_log()

    def _cargar_log(self):
        if self.log_path.exists():
            try:
                with open(self.log_path, "r") as f:
                    self.historial = json.load(f)
                print(f"[📥 PREDICTOR] Log cargado con {len(self.historial)} eventos HALT.")
            except Exception as e:
                print(f"[❌ PREDICTOR] Error al cargar log: {e}")
        else:
            print("[⚠️ PREDICTOR] No se encontró el archivo de eventos HALT.")

    def evaluar_riesgo(self, contexto: dict) -> float:
        """
        Evalúa riesgo de HALT en base a patrones históricos y condiciones actuales.
        Retorna un valor de riesgo entre 0.0 (seguro) y 1.0 (crítico).
        """
        if not self.historial:
            return 0.0

        ciclo_actual = contexto.get("cycle", 0)
        entropia = contexto.get("entropy", 0.0)
        error = contexto.get("error_rate", 0.0)
        sin_nuevas = contexto.get("cycles_without_new_rule", 0)

        score = 0.0
        if entropia >= 0.75:
            score += 0.4
        if error >= 0.5:
            score += 0.3
        if sin_nuevas >= 15:
            score += 0.3

        score = min(score, 1.0)
        print(f"[🧠 PREDICTOR] Riesgo estimado de HALT: {score:.2f}")
        return score

    def es_riesgoso(self, contexto: dict, umbral=0.7) -> bool:
        return self.evaluar_riesgo(contexto) >= umbral

# CLI rápido
if __name__ == "__main__":
    predictor = HaltPredictor()
    test_contexto = {
        "entropy": 0.81,
        "error_rate": 0.51,
        "cycles_without_new_rule": 17,
        "cycle": 99
    }
    predictor.evaluar_riesgo(test_contexto)
