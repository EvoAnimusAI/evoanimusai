# symbolic_ai/symbolic_entropy_controller.py
# -*- coding: utf-8 -*-
"""
Controlador de Entropía Simbólica de EvoAnimusAI
Nivel: Seguridad militar / Ultra-secreto / Producción endurecida

Funciones:
• Supervisa, regula y rastrea entropía simbólica.
• Previene loops caóticos, fuerza mutaciones adaptativas.
• Emite decisiones de contención y estabilización del sistema.

Trazabilidad: Total, con seguimiento tipo printf en cada etapa crítica.
"""

import logging
from typing import Optional

ENTROPY_THRESHOLD = 0.95
FORCE_MUTATION_THRESHOLD = 1.0
RECOVERY_ACTION = "wait"
ALPHA_DECAY = 0.05
MAX_SAFE_RESET_ENTROPY = 0.01

logger = logging.getLogger(__name__)

class SymbolicEntropyController:
    def __init__(self, entropy: float = 0.0):
        self.entropy = entropy
        self.high_entropy_counter = 0
        self.active = True
        self.recovery_mode = False
        print(f"[🔧 INIT] Controlador de Entropía inicializado con entropy = {self.entropy:.4f}")

    def update_entropy(self, value: float):
        print(f"[🧮 UPDATE] Valor recibido: {value}")
        if not isinstance(value, (int, float)):
            print(f"[❌ ERROR] Tipo inválido para entropy: {type(value)}")
            return
        if not 0.0 <= value <= 1.0:
            print(f"[❌ ERROR] Valor fuera de rango permitido: {value}")
            return
        old_entropy = self.entropy
        self.entropy = value
        print(f"[↔️ SET] Entropy actualizada: {old_entropy:.4f} ➜ {self.entropy:.4f}")
        logger.debug(f"[EntropyController] Entropía actualizada: {old_entropy:.4f} ➜ {self.entropy:.4f}")

        if self.entropy >= ENTROPY_THRESHOLD:
            self.high_entropy_counter += 1
            print(f"[⚠️ ALERT] Entropía crítica (≥ {ENTROPY_THRESHOLD}). Contador elevado a {self.high_entropy_counter}")
        else:
            if self.high_entropy_counter > 0:
                print(f"[🔁 RESET] Contador de entropía crítica reiniciado")
                self.high_entropy_counter = 0

    def update_entropy_change(self, reward: float) -> None:
        print(f"[🔄 ENTROPY_CHANGE] Recompensa recibida: {reward}")
        if not isinstance(reward, (int, float)):
            print(f"[❌ ERROR] Recompensa inválida: {reward}")
            return
        # Penaliza con mayor intensidad recompensas negativas
        delta = 0.01 * abs(reward)
        if reward < 0:
            delta *= 1.5
        old_entropy = self.entropy
        self.entropy = min(1.0, self.entropy + delta)
        print(f"[📈 ENTROPY] Cambio aplicado: +{delta:.4f} ➜ Entropy: {old_entropy:.4f} ➜ {self.entropy:.4f}")
        logger.info(f"[EntropyController] Cambio de entropía aplicado: {old_entropy:.4f} ➜ {self.entropy:.4f}")

    def requires_halt(self) -> bool:
        resultado = self.entropy >= FORCE_MUTATION_THRESHOLD
        print(f"[🚦 HALT_CHECK] Entropy = {self.entropy:.4f} ➜ ¿Requiere HALT? {resultado}")
        return resultado

    def should_force_mutation(self) -> bool:
        resultado = self.entropy >= FORCE_MUTATION_THRESHOLD and self.high_entropy_counter >= 2
        print(f"[🧬 FORCE_MUTATION] Evaluación ➜ {resultado} (entropy = {self.entropy:.4f}, contador = {self.high_entropy_counter})")
        return resultado

    def get_recovery_action(self) -> str:
        print(f"[🛟 RECOVERY_ACTION] Acción de recuperación emitida: '{RECOVERY_ACTION}'")
        return RECOVERY_ACTION

    def reduce_entropy(self):
        old_entropy = self.entropy
        self.entropy = max(0.0, self.entropy - ALPHA_DECAY)
        print(f"[⬇️ DECAY] Reducción de entropy: {old_entropy:.4f} ➜ {self.entropy:.4f}")
        logger.info(f"[EntropyController] Reducción: {old_entropy:.4f} ➜ {self.entropy:.4f}")

    def enforce_stabilization(self, symbolic_engine: Optional[object] = None):
        print(f"[🔒 STABILIZATION] Protocolo de estabilización activado")
        if self.requires_halt():
            print(f"[🚨 EMERGENCY] HALT activado por entropy ≥ {FORCE_MUTATION_THRESHOLD}")
            self.recovery_mode = True
            if symbolic_engine:
                print(f"[🤖 ENGINE] Ejecutando acción de recuperación en motor simbólico...")
                symbolic_engine.apply_action(self.get_recovery_action())
                symbolic_engine.record_event("entropy_control", {
                    "event": "emergency_halt",
                    "entropy": self.entropy,
                    "action": RECOVERY_ACTION
                })
        else:
            print(f"[✅ OK] Entropía bajo umbral. No se requiere estabilización.")

    def report(self) -> dict:
        reporte = {
            "entropy": round(self.entropy, 4),
            "high_entropy_counter": self.high_entropy_counter,
            "recovery_mode": self.recovery_mode,
            "requires_halt": self.requires_halt()
        }
        print(f"[📋 REPORT] Estado actual del controlador: {reporte}")
        return reporte

    def reset(self):
        print(f"[🔄 RESET] Intentando reiniciar controlador...")
        if self.entropy > MAX_SAFE_RESET_ENTROPY:
            print(f"[🛑 BLOQUEADO] Entropy = {self.entropy:.4f} > {MAX_SAFE_RESET_ENTROPY} ➜ Reinicio denegado.")
            return
        self.entropy = 0.0
        self.high_entropy_counter = 0
        self.recovery_mode = False
        print(f"[✅ RESET_OK] Controlador reiniciado correctamente: entropy = 0.0")

# === INTERFAZ GLOBAL ===
_controller = SymbolicEntropyController()

def check_entropy(context: Optional[object] = None) -> float:
    print(f"[🧩 CHECK_ENTROPY] Procesando contexto: {context}")
    if context and hasattr(context, "get_context"):
        ctx = context.get_context()
        entropy = ctx.get("entropy", 0.0)
        print(f"[📥 CONTEXT] Entropía extraída: {entropy}")
        _controller.update_entropy(entropy)
    else:
        print(f"[❔ NO_CONTEXT] Contexto inválido o ausente. Se asume entropy = 0.0")
    return _controller.entropy

def should_halt(entropy: Optional[float] = None) -> bool:
    if entropy is not None:
        print(f"[📤 DIRECT_INPUT] Entropy directa recibida: {entropy}")
        _controller.update_entropy(entropy)
    return _controller.requires_halt()
