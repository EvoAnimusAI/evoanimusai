# -*- coding: utf-8 -*-
"""
MetacognitiveSupervisor — Módulo de supervisión metacognitiva de EvoAnimusAI
-------------------------------------------------------------------------------
- Evalúa condiciones internas para detener o adaptar el sistema.
- Compatible con contexto simbólico, adaptativo y de alto riesgo.
- Nivel: Militar / Gubernamental / Ultra
"""

from datetime import datetime

class MetacognitiveSupervisor:
    def __init__(self, error_threshold: float = 0.7, stagnation_limit: int = 20) -> None:
        self.error_threshold = error_threshold
        self.stagnation_limit = stagnation_limit
        self.event_log = []
        print(f"[🧠 INIT] MetacognitiveSupervisor inicializado | error_threshold = {self.error_threshold:.2f}, stagnation_limit = {self.stagnation_limit}")

    def should_stop(self, context: dict) -> tuple[bool, str]:
        print(f"\n[🧠 METACOG] Evaluando contexto metacognitivo...")

        if not isinstance(context, dict):
            print(f"[❌ ERROR] Contexto inválido (tipo={type(context)}). Se esperaba dict.")
            return True, "Contexto inválido"

        error_rate = context.get("error_rate", 0.0)
        mutation_budget = context.get("mutation_budget", 0)
        cycles_without_new_rule = context.get("cycles_without_new_rule", 0)
        recent_rewards = context.get("recent_rewards", [])

        print(f"[🔍 INSPECCIÓN] error_rate={error_rate:.3f} | mutation_budget={mutation_budget} | cycles_without_new_rule={cycles_without_new_rule}")

        if error_rate > self.error_threshold:
            print(f"[🚨 ALERTA] Tasa de error excede umbral: {error_rate:.3f} > {self.error_threshold:.2f}")
            self._log_event("HALT: High error rate")
            return True, "High error rate"

        if cycles_without_new_rule >= self.stagnation_limit:
            print(f"[⚠️ ESTANCAMIENTO] Sin nuevas reglas por {cycles_without_new_rule} ciclos.")
            self._log_event("HALT: Evolution stagnation")
            return True, "Evolution stagnation"

        if isinstance(recent_rewards, list) and recent_rewards:
            reward_avg = sum(recent_rewards) / len(recent_rewards)
            print(f"[📊 REWARDS] Recompensas recientes: avg={reward_avg:.4f}")
            if reward_avg < 0.05:
                print("[🟡 AVISO] Recompensas bajas. Posible bloqueo evolutivo.")
                self._log_event("WARN: Low reward performance")

        print("[✅ CONTINUAR] No se requiere detención. Evolución sigue activa.")
        return False, "Continuar"

    def perform_mutation(self, context: dict) -> bool:
        print(f"\n[🧬 MUTATION] Evaluando posibilidad de mutación adaptativa...")

        if not isinstance(context, dict):
            print(f"[❌ MUTATION ERROR] Contexto inválido: {type(context)}")
            self._log_event("MUTATION_FAIL: Invalid context")
            return False

        mutation_budget = context.get("mutation_budget", 0)
        entropy = context.get("entropy", 0.0)
        error_rate = context.get("error_rate", 0.0)

        print(f"[📈 MUTATION METRICS] mutation_budget={mutation_budget}, entropy={entropy:.4f}, error_rate={error_rate:.3f}")

        if mutation_budget <= 0:
            print("[⛔ MUTATION BLOCKED] Presupuesto agotado.")
            self._log_event("MUTATION_BLOCKED: No budget")
            return False

        if entropy > 0.9:
            print(f"[⚠️ HIGH ENTROPY] Entropía demasiado alta: {entropy:.4f}")
            self._log_event("MUTATION_ABORTED: High entropy")
            return False

        if error_rate < 0.1:
            print("[🟢 BAJA TASA DE ERROR] Mutación innecesaria en condiciones óptimas.")
            self._log_event("MUTATION_SKIPPED: Low error")
            return False

        print("[🛠️ MUTATION INITIATED] Ejecutar lógica adaptativa de mutación simbólica aquí...")
        # 🔒 Lugar reservado para engine de mutación simbólica real
        self._log_event("MUTATION_OK: Placeholder ejecutado")
        return True

    def _log_event(self, reason: str) -> None:
        timestamp = datetime.utcnow().isoformat()
        entry = {"time": timestamp, "event": reason}
        self.event_log.append(entry)
        print(f"[📝 LOG EVENT] {entry}")
