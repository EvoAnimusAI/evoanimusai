import logging
import sys
import traceback
import math
import random

from symbolic_ai.symbolic_env import SymbolicEnvironment
from symbolic_ai.symbolic_rule import SymbolicRule  # Asegura que se importe correctamente

logger = logging.getLogger("SymbolicDecisionEngine")
if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] [SymbolicDecisionEngine] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def inject_entropy(context, cycle):
    print(f"[⚙️ ENTROPY_INJECTOR] Inyectando entropía para ciclo #{cycle}...")
    try:
        base_entropy = float(context.get("entropy", 0.0))
        noise_factor = random.uniform(0, 0.05)
        cycle_amplitude = math.sin(cycle / 10.0) * 0.1
        entropy = min(1.0, max(0.0, base_entropy + noise_factor + cycle_amplitude))
        context["entropy"] = round(entropy, 4)
        print(f"[⚙️ ENTROPY_INJECTOR] Entropía final inyectada: {context['entropy']}")
        return context
    except Exception as e:
        logger.error("Error al inyectar entropía: %s", e)
        print(f"[❌ ERROR] Falla en inject_entropy: {e}")
        context["entropy"] = 0.0
        return context

class SymbolicDecisionEngine:
    def __init__(self, context=None):
        print("[🧐 INIT] Iniciando SymbolicDecisionEngine...")
        self.context = context if context else {}
        self.rules = []
        self.cycle_count = 0
        self.last_error = None
        print(f"[🧐 INIT] Estado inicial: contexto={self.context}, reglas={len(self.rules)}")
        logger.info("Motor simbólico inicializado con contexto base.")

    def decide(self):
        print(f"\n[🤖 DECIDE] Ciclo de decisión #{self.cycle_count}")
        try:
            ctx = inject_entropy(self.context, self.cycle_count)
            entropy = ctx.get("entropy", 0.0)
            print(f"[📊 CONTEXTO] Entropía recibida: {entropy}")
            logger.info("Evaluando decisión simbólica con entropía: %.4f", entropy)

            env = SymbolicEnvironment(ctx)
            eval_context = env.get_eval_context()
            ctx_dict = eval_context.__dict__
            print(f"[📦 CONTEXTO EVAL] {ctx_dict}")

            print(f"[📚 EVALUACIÓN] Total reglas cargadas: {len(self.rules)}")
            for i, rule in enumerate(self.rules):
                print(f"[🔁 EVALUAR REGLA {i+1}] {rule.texto if hasattr(rule, 'texto') else rule}")
                if hasattr(rule, "evaluar"):
                    try:
                        result = rule.evaluar(ctx_dict)
                        print(f"[🧠 RESULTADO] '{rule.texto}': {result}")
                        if result:
                            decision = {
                                "action": rule.body(),
                                "reason": "symbolic_rule_match",
                                "rule": rule.texto,
                                "confidence": getattr(rule, "confidence", 1.0)
                            }
                            print(f"[🎯 MATCH] Regla activada: {decision}")
                            self.context["last_decision"] = decision
                            self.cycle_count += 1
                            return decision
                    except Exception as e:
                        print(f"[❌ EVAL_FAIL] Regla falló: {e}")

            print("[🪂 DEFAULT] Ninguna regla activada. Usando fallback por entropía.")
            if eval_context.entropy > 0.75:
                decision = {"action": "explore", "reason": "entropy_high"}
                print("[🚀 DECISION] Acción fallback: explore")
            elif eval_context.entropy > 0.3:
                decision = {"action": "observe", "reason": "entropy_mid"}
                print("[👁️ DECISION] Acción fallback: observe")
            else:
                decision = {"action": "wait", "reason": "entropy_low"}
                print("[🚠 DECISION] Acción fallback: wait")

            decision["entropy"] = eval_context.entropy
            self.context["last_decision"] = decision
            self.cycle_count += 1
            print(f"[✅ OUTPUT] Decisión final: {decision}")
            logger.info("Decisión emitida: %s", decision)
            return decision

        except Exception as ex:
            self.last_error = str(ex)
            traceback_str = traceback.format_exc()
            logger.error("Error en 'decide': %s", self.last_error)
            print(f"[❌ ERROR] Falla en decide(): {self.last_error}")
            print(traceback_str)
            return {"action": "noop", "reason": "exception", "error": self.last_error}

    def get_rule_by_action(self, action):
        print(f"[🔍 BUSQUEDA] get_rule_by_action('{action}')")
        try:
            for rule in self.rules:
                if rule.get("action") == action:
                    print(f"[✅ ENCONTRADA] Regla: {rule}")
                    return rule
            print("[⚠️ SIN REGLA] Ninguna regla coincide con la acción.")
            return {}
        except Exception as ex:
            logger.error("Error en get_rule_by_action: %s", ex)
            print(f"[❌ ERROR] en get_rule_by_action: {ex}")
            return {}

    def update_rule(self, rule, reward):
        print(f"[📈 UPDATE] Actualizando regla con recompensa: {reward}")
        try:
            if rule:
                rule["score"] = rule.get("score", 0.0) + reward
                print(f"[🧾 NUEVO SCORE] Regla actualizada: {rule}")
                logger.info("Regla modificada: %s", rule)
            else:
                print("[⚠️ SKIP] Regla vacía, no se actualiza.")
        except Exception as ex:
            logger.error("Error en update_rule: %s", ex)
            print(f"[❌ ERROR] en update_rule: {ex}")

    def mutate_rules(self):
        print("[🧬 MUTACIÓN] Iniciando mutación de reglas...")
        try:
            if not self.rules:
                print("[⚠️ NO_OP] No hay reglas para mutar.")
                return
            for rule in self.rules:
                original_score = rule.get("score", 0.0)
                rule["score"] = max(0.0, original_score * 0.95)
                print(f"[🔄 MUTADO] Regla: {rule}")
            logger.info("Mutación de reglas completada.")
        except Exception as ex:
            logger.error("Error en mutate_rules: %s", ex)
            print(f"[❌ ERROR] en mutate_rules: {ex}")

    def save_rules(self):
        print("[💾 GUARDADO] Guardando reglas simbólicas (stub)...")
        try:
            logger.info("save_rules() invocado. No implementado aún.")
            print("[ℹ️ STUB] save_rules aún no implementado.")
        except Exception as ex:
            logger.error("Error en save_rules: %s", ex)
            print(f"[❌ ERROR] en save_rules: {ex}")
