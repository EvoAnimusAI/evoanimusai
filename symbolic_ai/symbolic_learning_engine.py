# symbolic_ai/symbolic_learning_engine.py
# -*- coding: utf-8 -*-
"""
Núcleo de Aprendizaje Simbólico de EvoAI — Nivel gubernamental, científico y militar.
--------------------------------------------------------------------------------------
Responsabilidades:
- Aplicación de reglas simbólicas en contextos inteligentes.
- Aprendizaje por refuerzo sobre acciones simbólicas.
- Generación y mutación de reglas simbólicas.
- Exportación trazable del state de razonamiento.

Autor: Daniel Santiago Ospina Velasquez :: AV255583
"""

import logging
from typing import Dict, List, Optional, Any, Set, Tuple, Protocol

from symbolic_ai.mutation_validator import validate_and_prepare  # 🔐 Validación militar
from symbolic_ai.semantic_utils import normalizar_observacion   # ✅ Sin circularidad

logger = logging.getLogger("EvoAI.SymbolicLearningEngine")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# 🔌 Interfaz para compatibilidad con motores simbólicos
class RuleEngineInterface(Protocol):
    def evaluate(self, context: Dict[str, Any]) -> List[Any]: ...
    def add_rule(self, rule: Any) -> None: ...
    def remove_rule(self, rule: Any) -> None: ...

class SymbolicLearningEngine:
    def __init__(self, rule_engine: Optional[RuleEngineInterface] = None):
        if rule_engine is None:
            raise ValueError("El parámetro 'rule_engine' es obligatorio para entornos de auditoría.")
        self.rule_engine = rule_engine
        self.reinforcement_history: Dict[Tuple[str, str], List[float]] = {}
        self.generated_rules: Set[Tuple[str, str]] = set()

        print(f"[🧠 INIT] SymbolicLearningEngine inicializado con motor: {type(rule_engine).__name__}")
        logger.info("[Init] SymbolicLearningEngine inicializado con motor: %s", type(rule_engine).__name__)

    def observe(self, observation: Dict[str, Any]) -> None:
        print(f"[👁️ OBSERVE] Observación bruta: {observation}")
        observation = normalizar_observacion(observation)
        print(f"[🎯 OBSERVE - NORMALIZADO] => {observation}")
        logger.info("[Observe] Observación simbólica recibida: %s", observation)

    def register_concept(self, concept: str, source: str = "unknown") -> None:
        print(f"[📌 REGISTRO] Concepto simbólico: {concept} | fuente={source}")
        self.generated_rules.add((concept, source))
        logger.info("[RegisterConcept] Concepto registrado: %s (fuente: %s)", concept, source)

    def apply_rules(self, context: Dict[str, Any]) -> List[str]:
        print(f"[🧠 APPLY_RULES] Contexto recibido: {context}")
        logger.debug("[ApplyRules] Contexto recibido: %s", context)
        normalized_context = normalizar_observacion(context)
        print(f"[📐 CONTEXTO NORMALIZADO] => {normalized_context}")
        try:
            resultado = self.rule_engine.evaluate(normalized_context)
            acciones = []
            if isinstance(resultado, list):
                for r in resultado:
                    if hasattr(r, "texto") and isinstance(r.texto, str):
                        acciones.append(r.texto)
                    elif isinstance(r, str):
                        acciones.append(r)
                    else:
                        acciones.append(str(r))
            else:
                print("[⚠️ WARNING] Resultado inesperado: no es lista.")
                logger.warning("[ApplyRules] Resultado inesperado: no es lista.")
            print(f"[✅ RESULTADO] Acciones simbólicas: {acciones}")
            logger.info("[ApplyRules] Resultado simbólico procesado: %s", acciones)
            return acciones
        except Exception as e:
            print(f"[❌ ERROR] Al aplicar reglas: {e}")
            logger.error("[ApplyRules] Error crítico al aplicar reglas: %s", e, exc_info=True)
            return []

    def add_rule(self, rule: Any) -> None:
        print(f"[➕ ADD_RULE] Intentando agregar: {rule}")
        logger.info("[AddRule] Solicitando agregar regla: %s", rule)
        try:
            safe_rule = validate_and_prepare(rule)  # 🔐 Validación de seguridad
            self.rule_engine.add_rule(safe_rule)
            print(f"[✔️ ADD_RULE] Regla agregada exitosamente.")
        except Exception as e:
            print(f"[❌ ADD_RULE ERROR] No se pudo agregar la regla: {e}")
            logger.warning("[AddRule] Fallo al agregar regla validada: %s", e)

    def update_rule(self, action: str, reward: float, alpha: float = 0.1) -> None:
        key = ("action", action)
        if key not in self.reinforcement_history:
            print(f"[🧪 INIT_RULE] Acción nueva detectada: {action} ➜ prioridad=1.0")
            self.reinforcement_history[key] = [1.0]  # Inicialización optimista

        prev = self.reinforcement_history[key][-1]
        updated = prev + alpha * (reward - prev)
        self.reinforcement_history[key].append(updated)

        print(f"[📊 UPDATE_RULE] Acción: {action} | Recompensa: {reward:.3f} | Prioridad: {prev:.3f} ➜ {updated:.3f}")
        logger.info("[update_rule] Campos actualizados: {'action': '%s', 'priority': %.3f}", action, updated)
        logger.info("[update_rule] Priority ajustada: %.3f ➜ %.3f (reward=%.3f, α=%.2f)", prev, updated, reward, alpha)

        if key not in self.generated_rules:
            simulated_rule = f"⟦action:{action}⟧ ⇒ {action} :: True"
            self.generated_rules.add(key)
            print(f"[🧠 SIM_RULE] Generada simbólicamente: {simulated_rule}")
            logger.info("[update_rule] Regla simbólica generada: %s", simulated_rule)

            try:
                if not isinstance(simulated_rule, str):
                    raise TypeError(f"[❌ ERROR] Regla simbólica generada no es cadena: {type(simulated_rule)}")

                safe_rule = validate_and_prepare(simulated_rule)
                self.rule_engine.add_rule(safe_rule)
                print(f"[✔️ SIM_RULE] Regla agregada correctamente.")
            except Exception as e:
                print(f"[❌ SIM_RULE ERROR] No se pudo agregar regla simbólica: {e}")
                logger.warning("[update_rule] No se pudo agregar la regla generada: %s", e)

    def export_state(self) -> Dict[str, Any]:
        state = {
            "reinforcement_history": dict(self.reinforcement_history),
            "generated_rules": list(self.generated_rules),
            "engine_type": type(self.rule_engine).__name__
        }
        print(f"[📦 EXPORT] Estado exportado: {state}")
        logger.debug("[ExportState] Estado exportado: %s", state)
        return state
