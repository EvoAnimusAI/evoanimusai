# -*- coding: utf-8 -*-
"""
HaltMonitor — Monitor de eventos HALT y activador simbiótico en EvoAI
Nivel cibernético/militar. Incluye integración con ConcienciaSimulada y visualización.
"""

import datetime
import time
from tools.halt_visualizer import HaltVisualizer

class HaltMonitor:
    def __init__(self, max_halts=3, window_seconds=60, recovery_callback=None):
        self.halt_events = []
        self.historial_ciclos = []
        self.max_halts = max_halts
        self.window_seconds = window_seconds
        self.visualizer = HaltVisualizer()
        self.recovery_callback = recovery_callback  # callback a ConcienciaSimulada

    def registrar_halt(self, razon, contexto):
        evento = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "razon": razon,
            "contexto": contexto,
        }
        self.halt_events.append(time.time())
        self.visualizer.registrar_evento(contexto)
        print(f"[🛑 HALT_MONITOR] HALT registrado: {razon}")
        print(f"[📋 CONTEXTO HALT] {contexto}")

        if self._evaluar_acumulacion():
            print("[⚠️ HALT_MONITOR] Acumulación crítica de HALTs detectada.")
            if self.recovery_callback:
                print("[🧠 HALT_MONITOR] Activando recuperación via ConcienciaSimulada...")
                self.recovery_callback(contexto)
            else:
                print("[❌ HALT_MONITOR] No hay recuperación configurada.")

    def registrar_ciclo(self, contexto_actual):
        ciclo = contexto_actual.get("cycle", -1)
        entropy = contexto_actual.get("entropy", None)
        error_rate = contexto_actual.get("error_rate", None)
        mutation_budget = contexto_actual.get("mutation_budget", None)
        recent_rewards = contexto_actual.get("recent_rewards", [])
        cycles_without_new_rule = contexto_actual.get("cycles_without_new_rule", None)

        print(f"[🧮 HALT_MONITOR] Ciclo {ciclo}")
        print(f" ├─ Entropía: {entropy}")
        print(f" ├─ Tasa de error: {error_rate}")
        print(f" ├─ Mutación disponible: {mutation_budget}")
        print(f" ├─ Sin nuevas reglas: {cycles_without_new_rule}")
        print(f" └─ Recompensas: {recent_rewards[-3:]}")

        self.historial_ciclos.append({
            "ciclo": ciclo,
            "entropy": entropy,
            "error_rate": error_rate,
            "mutation_budget": mutation_budget,
            "rewards": recent_rewards[-3:],
            "sin_nuevas_reglas": cycles_without_new_rule,
        })

        # Alertas preventivas
        if cycles_without_new_rule and cycles_without_new_rule >= 15:
            print(f"[⚠️] Estancamiento posible en ciclo {ciclo}")
        if error_rate and error_rate >= 0.6:
            print(f"[⚠️] Error crítico en ciclo {ciclo}")
        if entropy and entropy >= 0.8:
            print(f"[⚠️] Entropía alta en ciclo {ciclo}")

    def detectar_halt_critico(self) -> bool:
        """
        Detecta si se ha alcanzado un estado HALT crítico basado en condiciones acumuladas.
        """
        if not self.historial_ciclos:
            return False

        ultimo = self.historial_ciclos[-1]
        entropia = ultimo.get("entropy", 0.0)
        error = ultimo.get("error_rate", 0.0)
        sin_nuevas = ultimo.get("sin_nuevas_reglas", 0)

        if entropia >= 0.75:
            print("[⚠️ HALT_MONITOR] Entropía crítica detectada.")
            return True
        if error and error >= 0.6:
            print("[⚠️ HALT_MONITOR] Error crítico detectado.")
            return True
        if sin_nuevas and sin_nuevas >= 20:
            print("[⚠️ HALT_MONITOR] Estancamiento prolongado detectado.")
            return True
        return False

    def _evaluar_acumulacion(self) -> bool:
        self._limpiar_eventos()
        return len(self.halt_events) >= self.max_halts

    def _limpiar_eventos(self):
        umbral = time.time() - self.window_seconds
        self.halt_events = [t for t in self.halt_events if t >= umbral]

    def obtener_eventos_halt(self):
        return self.halt_events

    def obtener_historial_ciclos(self):
        return self.historial_ciclos
