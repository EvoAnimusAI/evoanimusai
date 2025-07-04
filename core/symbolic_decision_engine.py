# core/symbolic_decision_engine.py
# -*- coding: utf-8 -*-
"""
Módulo oficial de decisiones simbólicas para EvoAnimusAI.
"""

import logging
from typing import Dict, Any, Optional, List

from core.context import EvoContext
from symbolic_ai.symbolic_entropy_controller import check_entropy, should_halt
from symbolic_ai.rule_manager import version_rule, diff_rules
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine, SymbolicRule

logger = logging.getLogger("EvoAI.SymbolicDecisionEngine")


class ToolManager:
    def initialize(self, verbose: bool = False) -> None:
        if verbose:
            logger.info("[🛠️] Inicializando herramientas auxiliares...")
        print("[🛠️ INIT] ToolManager inicializado.")
        # Aquí podrían inicializarse herramientas futuras.


class SymbolicDecisionEngine:
    def __init__(self, context: EvoContext, engine: Optional[SymbolicRuleEngine] = None) -> None:
        print("[🔧 INIT] Construyendo SymbolicDecisionEngine...")
        if not isinstance(context, EvoContext):
            raise TypeError("El contexto debe ser una instancia de EvoContext.")

        self.context = context
        self.engine = engine or SymbolicRuleEngine()
        self.last_decision = None
        self.tools = ToolManager()

        if not hasattr(self.engine, "evaluate") or not callable(getattr(self.engine, "evaluate")):
            raise AttributeError("[INIT] El motor simbólico proporcionado no implementa 'evaluate(context)'.")

        logger.info("[✅ SymbolicDecisionEngine] Inicializado con contexto, motor simbólico y herramientas auxiliares.")
        print("[✅ INIT] SymbolicDecisionEngine activo y listo.")

    def decide(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug("[🧠] Iniciando evaluación simbólica con contexto externo...")
        print(f"\n[🧩 CONTEXTO ENTRANTE]: {context}")

        entropy = check_entropy(context)
        print(f"[🔢 ENTROPY CHECK]: {entropy}")

        if should_halt(entropy):
            logger.warning(f"[⚠️] Entropía crítica detectada ({entropy:.2f}). Acción: 'halt'.")
            print(f"[🛑 HALT] Entropía crítica ({entropy:.2f}). Acción inmediata: halt")
            return {
                "action": "halt",
                "reason": "High symbolic entropy",
                "entropy": entropy
            }

        try:
            self.log_context_facts()

            # Evaluación simbólica
            rules = self.engine.evaluate(context)
            print(f"[📊 EVALUATE] Total reglas activadas: {len(rules)}")

            # Priorización
            prioritized = self.prioritize_rules(rules)
            if not prioritized:
                logger.warning("[❗] No se pudo priorizar ninguna action. Emitiendo 'noop'.")
                print("[⚠️ WARNING] Ninguna regla priorizada. Acción: 'noop'")
                return {
                    "action": "noop",
                    "reason": "No valid symbolic decision",
                    "entropy": entropy
                }

            selected = prioritized[0].to_dict()
            selected["entropy"] = entropy
            selected["source"] = "symbolic_decision_engine"

            self.last_decision = selected
            self.audit_decision(selected)

            logger.info(f"[✅] Acción seleccionada: {selected}")
            print(f"[🧠 DECISIÓN] {selected}")
            return selected

        except Exception as e:
            logger.error(f"[❌] Fallo crítico en decide(): {e}", exc_info=True)
            print(f"[❌ EXCEPCIÓN EN DECIDE]: {e}")
            return {
                "action": "error",
                "reason": str(e),
                "source": "symbolic_decision_engine"
            }

    def prioritize_rules(self, rules: List[SymbolicRule]) -> List[SymbolicRule]:
        logger.debug("[📊] Priorizando reglas simbólicas...")
        try:
            print(f"[🔎 REGLAS ACTIVADAS]: {[str(r) for r in rules]}")
            prioritized = sorted(
                rules,
                key=lambda r: getattr(r, "confidence", 0.0),
                reverse=True
            )
            print(f"[📈 PRIORITY SORTED]: {[r.confidence for r in prioritized]}")
            return prioritized
        except Exception as e:
            logger.error(f"[❌] Error en priorización simbólica: {e}", exc_info=True)
            print(f"[⚠️ PRIORITY ERROR]: {e}")
            return []

    def prioritize(self, rule_outputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.debug("[📊] Priorizando desde interfaz externa...")
        try:
            prioritized = sorted(
                rule_outputs,
                key=lambda x: x.get("confidence", 0.0),
                reverse=True
            )
            print(f"[📈 PRIORITIZED OUT]: {prioritized}")
            return prioritized
        except Exception as e:
            logger.error(f"[❌] Error al priorizar desde interfaz externa: {e}", exc_info=True)
            print(f"[⚠️ EXTERNAL PRIORITY ERROR]: {e}")
            return []

    def audit_decision(self, decision: Dict[str, Any]) -> None:
        try:
            versioned = version_rule(decision)
            logger.info(f"[🔐] Decisión versionada: {versioned.get('checksum')}")
            print(f"[🧾 VERSIONED] Checksum: {versioned.get('checksum')}")
        except Exception as e:
            logger.warning(f"[⚠️] No se pudo versionar la decisión: {e}", exc_info=True)
            print(f"[⚠️ AUDIT ERROR]: {e}")

    def assert_fact(self, key: str, value: Any) -> None:
        if hasattr(self.engine, "assert_fact") and callable(getattr(self.engine, "assert_fact")):
            logger.debug(f"[➕] Afirmando hecho simbólico: {key} = {value}")
            print(f"[➕ ASSERT_FACT] {key} = {value}")
            try:
                self.engine.assert_fact(key, value)
                logger.info(f"[✅] Hecho simbólico afirmado: {key} = {value}")
            except Exception as e:
                logger.error(f"[❌] Fallo al afirmar hecho simbólico '{key}': {e}", exc_info=True)
                print(f"[❌ ERROR assert_fact] {e}")
        else:
            raise AttributeError("[SymbolicDecisionEngine] El motor simbólico no implementa 'assert_fact'.")

    def log_context_facts(self):
        try:
            if hasattr(self.engine, "facts"):
                print(f"[🧠 CONTEXTO INTERNO DEL MOTOR]: {self.engine.facts}")
            else:
                print(f"[ℹ️] Motor simbólico no expone 'facts'")
        except Exception as e:
            print(f"[⚠️] No se pudo imprimir facts del motor: {e}")
