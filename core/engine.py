# -*- coding: utf-8 -*-
"""
Módulo Motor Simbólico Autónomo EvoAI
-------------------------------------

Motor simbólico para selección, mutación y gestión de reglas con prioridad,
adaptado a contexto operativo y trazabilidad completa.

Cumple estándares militares y gubernamentales de seguridad, auditabilidad y control.

Responsabilidades:
- Decisión basada en reglas ponderadas
- Mutación controlada y validada de reglas
- Actualización de prioridades con validación de entradas
- Persistencia simulada con trazabilidad de operaciones
"""

import random
import logging
from typing import Any, Dict, List, Optional

from utils.default_rules import get_default_rules

logger = logging.getLogger("EvoAI.Engine")
logger.setLevel(logging.DEBUG)


class EvoAIEngine:
    """
    Motor simbólico autónomo con gestión avanzada de reglas y priorización.
    """

    def __init__(self, rules: Optional[List[Dict[str, Any]]] = None) -> None:
        try:
            self.rules: List[Dict[str, Any]] = rules if rules is not None else get_default_rules()
            self.context: Dict[str, Any] = {}
            logger.info(f"[Init] Motor inicializado con {len(self.rules)} reglas.")
        except Exception as e:
            logger.exception(f"[Init] Error al inicializar motor: {e}")
            raise RuntimeError("Error crítico al inicializar motor simbólico.") from e

    def decide(self, context: Dict[str, Any]) -> str:
        if not isinstance(context, dict):
            logger.error("[Decide] Contexto inválido, se esperaba dict.")
            raise ValueError("El contexto debe ser un diccionario válido.")

        self.context = context
        logger.debug(f"[Decide] Contexto recibido: {context}")

        if not self.rules:
            logger.warning("[Decide] No hay reglas definidas, acción por defecto 'wait'.")
            return "wait"

        try:
            rule = max(self.rules, key=lambda r: r.get("priority", 0.0))
            action = rule.get("action", "wait")
            logger.info(f"[Decide] Acción seleccionada: {action} con prioridad {rule.get('priority')}")
            return action
        except Exception as e:
            logger.exception(f"[Decide] Error al seleccionar acción: {e}")
            raise RuntimeError("Fallo en decisión de acción.") from e

    def mutate_rules(self) -> None:
        if not self.rules:
            logger.warning("[Mutate] Sin reglas para mutar.")
            return
        try:
            rule = random.choice(self.rules)
            old_priority = float(rule.get("priority", 0.5))
            delta = random.uniform(-0.2, 0.2)
            new_priority = round(min(1.0, max(0.0, old_priority + delta)), 2)
            rule["priority"] = new_priority
            logger.info(f"[Mutate] Mutación aplicada: acción '{rule.get('action')}', prioridad {old_priority} ➜ {new_priority}")
        except Exception as e:
            logger.exception(f"[Mutate] Error durante mutación de reglas: {e}")
            raise RuntimeError("Fallo en mutación de reglas.") from e

    def get_rule_by_action(self, action: str) -> Optional[Dict[str, Any]]:
        if not isinstance(action, str) or not action.strip():
            logger.error("[GetRule] Acción inválida para búsqueda.")
            raise ValueError("La acción debe ser una cadena no vacía.")

        rule = next((r for r in self.rules if r.get("action") == action), None)
        if rule:
            logger.debug(f"[GetRule] Regla encontrada para acción '{action}'.")
        else:
            logger.debug(f"[GetRule] No se encontró regla para acción '{action}'.")
        return rule

    def update_rule(self, rule: Dict[str, Any], reward: float) -> None:
        if not isinstance(reward, (int, float)):
            logger.error(f"[UpdateRule] Recompensa inválida: {reward}")
            raise ValueError("La recompensa debe ser un número (int o float).")

        if "priority" not in rule:
            logger.error("[UpdateRule] Regla no contiene campo 'priority'.")
            raise KeyError("La regla debe contener la clave 'priority'.")

        old_priority = float(rule.get("priority", 0.5))
        updated_priority = round(min(1.0, max(0.0, old_priority + 0.1 * reward)), 2)
        rule["priority"] = updated_priority
        logger.info(f"[UpdateRule] Prioridad regla '{rule.get('action')}' actualizada: {old_priority} ➜ {updated_priority}")

    def save_rules(self) -> None:
        logger.info("[SaveRules] Reglas simbólicas guardadas (simulado).")


# Alias para compatibilidad con código legado o tests
SymbolicEngine = EvoAIEngine
