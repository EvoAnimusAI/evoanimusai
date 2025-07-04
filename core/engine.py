# core/engine.py
# -*- coding: utf-8 -*-
"""
EvoAIEngine — Núcleo heurístico de EvoAnimusAI
-----------------------------------------------
- Motor de decisiones heurísticas basado en reglas y prioridad adaptativa
- Compatible con aprendizaje simbólico, control de entropía y supervisión metacognitiva
- Nivel: Militar / Gubernamental / Ultra
"""

import logging
import random
import re
from typing import Any, Dict, List

from utils.default_rules import get_default_rules
from symbolic_ai.symbolic_learning_engine import SymbolicLearningEngine
from symbolic_ai.symbolic_entropy_controller import SymbolicEntropyController
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine
from metacognition.metacognitive_supervisor import MetacognitiveSupervisor  # ✅ Integrado

logger = logging.getLogger("EvoAI.Engine")
logger.setLevel(logging.INFO)

def parse_symbolic_rule(rule_str: str) -> Dict[str, Any]:
    match = re.match(r"⟦(?P<rol>\w+):(?P<valor>\w+)⟧ ⇒ (?P<accion>\w+) :: (?P<condicion>.+)", rule_str)
    if not match:
        raise ValueError(f"[❌ ERROR] Formato inválido de regla simbólica: {rule_str}")
    return {
        "role": match.group("rol"),
        "value": match.group("valor"),
        "action": match.group("accion"),
        "condition": match.group("condicion"),
        "priority": 1.0
    }

class RuleEngineAdapter:
    def __init__(self, rules: List[Dict[str, Any]]) -> None:
        self.rules = [r for r in rules if isinstance(r, dict)]
        print(f"[🔧 RuleEngineAdapter] Inicializado con {len(self.rules)} reglas válidas.")

    def evaluate(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        print(f"[📥 EVALUATE] Contexto recibido: {context}")
        results = []
        for r in self.rules:
            try:
                cond = r.get("condition", "True")
                if eval(cond, {}, context):  # ⚠️ Solo en entornos cerrados
                    results.append(r)
            except Exception as e:
                print(f"[⚠️ ERROR] Evaluación fallida para regla {r}: {e}")
        sorted_results = sorted(results, key=lambda r: r.get("priority", 1.0), reverse=True)
        print(f"[📤 RESULTADOS] Evaluación heurística: {sorted_results}")
        return sorted_results

    def add_rule(self, rule: Any) -> None:
        print(f"[➕ ADD_RULE] Intentando agregar: {rule}")
        if isinstance(rule, str):
            try:
                rule = parse_symbolic_rule(rule)
            except ValueError as e:
                print(f"[❌ ADD_RULE ERROR] {e}")
                return
        elif not isinstance(rule, dict):
            print(f"[❌ ADD_RULE ERROR] Tipo no soportado: {type(rule)}")
            return
        self.rules.append(rule)
        print(f"[✅ ADD_RULE] Regla agregada: {rule}")

    def remove_rule(self, rule: Any) -> None:
        print(f"[➖ REMOVE_RULE] Intentando eliminar: {rule}")
        if rule in self.rules:
            self.rules.remove(rule)
            print("[✅ REMOVE_RULE] Regla eliminada.")
        else:
            print("[⚠️ REMOVE_RULE] Regla no encontrada.")

class EvoAIEngine:
    def __init__(self) -> None:
        print("[🔧 INIT] Iniciando EvoAnimusAI...")
        self.rules = get_default_rules()
        self.adapter = RuleEngineAdapter(self.rules)
        self.learning_engine = SymbolicLearningEngine(self.adapter)
        self.entropy_controller = SymbolicEntropyController(entropy=0.0)
        self.metacog = MetacognitiveSupervisor(error_threshold=0.8, stagnation_limit=20)  # ✅ Militar
        print(f"[INFO] [INIT] Motor heurístico inicializado con {len(self.rules)} reglas.")

    def decide(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print(f"\n🔄 [CICLO #{context.get('cycle', '?')}] ------------------------------")
        print(f"[🧠 DECIDE] Contexto heurístico: {context}")

        entropy = context.get("entropy", 0.0)
        self.entropy_controller.update_entropy(entropy)

        try:
            stop, reasons = self.metacog.should_stop(context)
            if stop:
                print(f"[🧠 METACOG STOP] Detenido por supervisor metacognitivo. Razones: {reasons}")
                return {"action": "halt"}
        except Exception as e:
            print(f"[⚠️ METACOG ERROR] Error en evaluación metacognitiva: {e}")

        if self.entropy_controller.requires_halt():
            print("[🚨 HALT] Entropía excedida. Decisión: HALT")
            return {"action": "halt"}

        evaluated = self.adapter.evaluate(context)

        if evaluated:
            selected = evaluated[0]
            print(f"[✅ SELECTED] Acción seleccionada: {selected.get('action')}")
            return {"action": selected.get("action", "wait")}
        else:
            print("[⚠️ DEFAULT ACTION] Acción: wait")
            return {"action": "wait"}

    def learn(self, context: Dict[str, Any], action: str, reward: float) -> None:
        print(f"[📚 LEARN] Observación: {context}, Acción: {action}, Recompensa: {reward}")
        try:
            self.learning_engine.update_rule(action, reward)
        except Exception as e:
            print(f"[❌ ERROR] Fallo en aprendizaje simbólico: {e}")

        try:
            self.entropy_controller.update_entropy_change(reward)
        except AttributeError as e:
            print(f"[❌ ERROR] Faltante método 'update_entropy_change': {e}")
        except Exception as e:
            print(f"[❌ ERROR] Fallo en controlador de entropía: {e}")
