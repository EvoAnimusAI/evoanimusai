# -*- coding: utf-8 -*-
"""
metacognition/metacognitive_recovery_manager.py

Módulo de recuperación simbólica automática — Nivel militar
Gestiona respuestas críticas ante estancamiento evolutivo, agotamiento de mutaciones
o entropía simbólica elevada. Integración directa con ConcienciaSimulada y motor simbólico.
"""

import logging
import datetime
from typing import Dict, Any

from symbolic_ai.symbolic_rule_engine import symbolic_rule_engine

logger = logging.getLogger("EvoAI.RecoveryManager")

def evaluar_contexto_critico(contexto: Dict[str, Any]) -> bool:
    """
    Evalúa si el sistema se encuentra en un estado crítico que requiere recuperación.
    """
    print("[🧠 RECOVERY] Evaluando contexto para posible recuperación...")
    ciclos_sin_reglas = contexto.get("cycles_without_new_rule", 0)
    mutation_budget = contexto.get("mutation_budget", 1)
    entropy = contexto.get("entropy", 0.0)

    print(f"[🔍 CHECK] cycles_without_new_rule = {ciclos_sin_reglas}")
    print(f"[🔍 CHECK] mutation_budget = {mutation_budget}")
    print(f"[🔍 CHECK] entropy = {entropy:.4f}")

    if ciclos_sin_reglas >= 20 or mutation_budget <= 0 or entropy >= 0.95:
        print("[⚠️ RECOVERY_TRIGGER] Condiciones críticas detectadas.")
        return True

    print("[✅ STABLE] Sistema estable. No se requiere recuperación.")
    return False

def iniciar_recuperacion(contexto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inicia protocolo de recuperación simbiótica y reconstrucción simbólica.
    """
    print("[⚕️ INICIO] Activando protocolo de recuperación simbólica...")
    logger.warning("[RECOVERY] Protocolo de recuperación activado.")

    evento = {
        "time": datetime.datetime.utcnow().isoformat(),
        "event": "RECOVERY_TRIGGERED",
        "reason": "Evolution stagnation or critical entropy"
    }

    print(f"[📝 LOG EVENT] {evento}")
    
    try:
        print("[🧯 RESET] Reiniciando motor simbólico...")
        symbolic_rule_engine._reset_rules_file()

        print("[♻️ LOAD] Cargando reglas por defecto tras reinicio...")
        symbolic_rule_engine.load_from_file(symbolic_rule_engine.rules_file)

        print("[🛡️ REBUILD] Regeneración simbólica completada.")
        logger.info("[RECOVERY] Reglas regeneradas con éxito.")
        
        return {
            "status": "recovered",
            "message": "Motor simbólico reiniciado y reglas restauradas.",
            "timestamp": evento["time"]
        }

    except Exception as e:
        print(f"[❌ ERROR][RECOVERY] Fallo durante recuperación: {e}")
        logger.error(f"[RECOVERY] Fallo durante recuperación: {e}", exc_info=True)
        return {
            "status": "failure",
            "message": str(e),
            "timestamp": evento["time"]
        }

def protocolo_de_emergencia(contexto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Función central invocable para evaluar y, si corresponde, ejecutar recuperación automática.
    """
    print("[🧠 PROTOCOLO] Evaluación metacognitiva de emergencia iniciada...")
    if evaluar_contexto_critico(contexto):
        return iniciar_recuperacion(contexto)
    else:
        return {
            "status": "stable",
            "message": "No se requieren acciones de recuperación en este ciclo."
        }
