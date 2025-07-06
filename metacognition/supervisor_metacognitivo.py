# -*- coding: utf-8 -*-
"""
metacognition/supervisor_metacognitivo.py

Supervisor Metacognitivo Continuo — Nivel militar
Monitorea en tiempo real el estado cognitivo del sistema EvoAI.
Ejecuta automáticamente el protocolo de recuperación cuando se detectan condiciones críticas.
"""

import logging
from typing import Dict, Any
from metacognition.metacognitive_recovery_manager import protocolo_de_emergencia

# 🧾 Registro simbiótico de eventos
from utils.logger_simbotico import (
    log_halt_event,
    save_crisis_snapshot,
    append_recovery_session,
)

logger = logging.getLogger("EvoAI.SupervisorMetacognitivo")

class SupervisorMetacognitivo:
    def __init__(self, threshold_cycles: int = 20, entropy_limit: float = 0.95):
        self.threshold_cycles = threshold_cycles
        self.entropy_limit = entropy_limit
        print(f"[🧠 SUPERVISOR] Inicializado. Threshold: {threshold_cycles} ciclos | Límite entropía: {entropy_limit:.2f}")

    def evaluar(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        print("[🔎 SUPERVISOR] Evaluando estado simbólico actual...")

        ciclos = contexto.get("cycles_without_new_rule", 0)
        entropy = contexto.get("entropy", 0.0)
        mutation_budget = contexto.get("mutation_budget", 1)

        print(f"[📊 METRICAS] cycles_without_new_rule = {ciclos} | entropy = {entropy:.4f} | mutation_budget = {mutation_budget}")

        if ciclos >= self.threshold_cycles or entropy >= self.entropy_limit or mutation_budget <= 0:
            print("[⚠️ ALERTA] Se detecta estado crítico. Ejecutando recuperación...")
            logger.warning("[SUPERVISOR] Condiciones críticas detectadas. Ejecutando recuperación automática.")

            # 📝 Registro HALT
            halt_reason = "Evolution stagnation" if ciclos >= self.threshold_cycles else "Entropy overload" if entropy >= self.entropy_limit else "No mutation budget"
            log_halt_event({
                "evento": "HALT",
                "razon": halt_reason,
                "ciclo": contexto.get("cycle", -1),
                "entropia": entropy,
                "mutation_budget": mutation_budget,
                "error_rate": contexto.get("error_rate", "N/A"),
            })

            # 🧊 Guardar snapshot crítico
            save_crisis_snapshot(contexto, contexto.get("cycle", -1))

            # 🛠️ Ejecutar recuperación simbiótica
            resultado = protocolo_de_emergencia(contexto)

            # 📥 Registro de recuperación
            append_recovery_session({
                "motivo": halt_reason,
                "ciclo": contexto.get("cycle", -1),
                "resultado": resultado,
                "entropia": entropy,
            })

            return resultado
        else:
            print("[✅ OK] Sistema simbólico estable. No se requieren acciones.")
            return {
                "status": "stable",
                "message": "Estado simbólico estable bajo supervisión.",
            }
