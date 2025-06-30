# symbolic_ai/symbolic_rule_engine.py

import json
import os
import logging
from collections import defaultdict
from typing import List, Dict, Optional, Union

from symbolic_ai.symbolic_rule import SymbolicRule

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

RULES_FILE = "data/symbolic_rule_engine.json"


class SymbolicRuleEngine:
    """
    Motor para manejar reglas simbólicas, permitiendo cargar, guardar,
    evaluar y mantener reglas organizadas por rol.
    """

    def __init__(self, auto_load: bool = True, rules_file: Optional[str] = None) -> None:
        self.rules_file = rules_file or RULES_FILE
        self.rules: Dict[str, List[SymbolicRule]] = defaultdict(list)
        if auto_load:
            self.load_from_file(self.rules_file)

    def _remove_duplicates(self) -> None:
        for rol, rule_list in self.rules.items():
            unique_rules = []
            for rule in rule_list:
                if rule not in unique_rules:
                    unique_rules.append(rule)
            self.rules[rol] = unique_rules

    def _reset_rules_file(self) -> None:
        try:
            if os.path.exists(self.rules_file):
                os.remove(self.rules_file)
                logger.info(f"Archivo de reglas corrupto eliminado: {self.rules_file}")
        except Exception as exc:
            logger.error(f"Error eliminando archivo corrupto {self.rules_file}: {exc}")

        self.rules.clear()
        self._add_default_rules()
        self.save_to_file(self.rules_file)

    def _add_default_rules(self) -> None:
        default_rules = [
            SymbolicRule("action", "explore", "move_forward", "noise == 'calm'"),
            SymbolicRule("action", "rest", "pause", "noise == 'chaos'"),
            SymbolicRule("state", "active", "explore", "pos >= 0"),
            # SymbolicRule("last_noise", "calm", "explore", "last_noise == 'calm'")
        ]
        for rule in default_rules:
            self.add_rule(rule)

    def add_rule(self, rule: Union[str, dict, SymbolicRule]) -> None:
        if isinstance(rule, str):
            rule = SymbolicRule.parse(rule)
        elif isinstance(rule, dict):
            rule = SymbolicRule.from_dict(rule)
        elif not isinstance(rule, SymbolicRule):
            raise TypeError(f"Expected SymbolicRule, dict, or str, got {type(rule)}")

        if any(existing == rule for existing in self.rules.get(rule.rol, [])):
            logger.warning(f"Regla duplicada ignorada: {rule}")
            return

        self.rules.setdefault(rule.rol, []).append(rule)
        self.save_to_file(self.rules_file)
        logger.info(f"Regla añadida: {rule}")

    def remove_rule(self, rule: Union[str, dict, SymbolicRule]) -> bool:
        if isinstance(rule, str):
            rule = SymbolicRule.parse(rule)
        elif isinstance(rule, dict):
            rule = SymbolicRule.from_dict(rule)
        elif not isinstance(rule, SymbolicRule):
            raise TypeError(f"Expected SymbolicRule, dict, or str, got {type(rule)}")

        rules_for_rol = self.rules.get(rule.rol, [])
        for i, existing_rule in enumerate(rules_for_rol):
            if existing_rule == rule:
                del rules_for_rol[i]
                self.save_to_file(self.rules_file)
                logger.info(f"Regla eliminada: {rule}")
                return True

        logger.warning(f"No se encontró la regla para eliminar: {rule}")
        return False

    def update_rule(self, old_rule: SymbolicRule, reward: Optional[float] = None) -> None:
        updated = False
        for i, rule in enumerate(self.rules.get(old_rule.rol, [])):
            if rule == old_rule:
                # Aquí se puede implementar lógica de actualización específica
                updated = True
                break

        if updated:
            self.save_to_file(self.rules_file)
            logger.info(f"Regla actualizada: {old_rule} con recompensa: {reward}")
        else:
            logger.warning(f"No se encontró la regla para actualizar: {old_rule}")

    def evaluate(self, contexto: dict) -> List[SymbolicRule]:
        matched_rules = []
        for rule_list in self.rules.values():
            for rule in rule_list:
                try:
                    if rule.evaluar(contexto):
                        matched_rules.append(rule)
                except Exception as exc:
                    logger.error(f"Error evaluando regla {rule}: {exc}")
        return matched_rules

    # Alias para compatibilidad con tests que usen apply_rules
    def apply_rules(self, contexto: dict) -> List[SymbolicRule]:
        return self.evaluate(contexto)

    def get_rule_by_action(self, accion: str) -> Optional[SymbolicRule]:
        for rule_list in self.rules.values():
            for rule in rule_list:
                if rule.accion == accion:
                    return rule
        return None

    def reset(self) -> None:
        self.rules.clear()
        self._add_default_rules()
        self.save_to_file(self.rules_file)
        logger.info("Entorno simbólico reiniciado.")

    def clear_rules(self) -> None:
        """Elimina todas las reglas sin guardar ni restaurar las reglas por defecto."""
        self.rules.clear()
        logger.info("Todas las reglas simbólicas han sido eliminadas.")

    def assert_fact(self, fact: dict) -> List[SymbolicRule]:
        if not isinstance(fact, dict):
            raise TypeError(f"[assert_fact] Esperado dict, recibido {type(fact)}")

        matched = self.evaluate(fact)
        if matched:
            logger.info(f"{len(matched)} reglas activadas por hecho: {fact}")
            for rule in matched:
                logger.info(f"  - {rule}")
        else:
            logger.info(f"Ninguna regla coincidió con: {fact}")
        return matched

    def save_to_file(self, filepath: str) -> None:
        all_rules = [rule.to_dict() for rule_list in self.rules.values() for rule in rule_list]
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({"rules": all_rules}, f, indent=2, ensure_ascii=False)
            logger.info(f"Reglas guardadas en {filepath}")
        except Exception as exc:
            logger.error(f"Error guardando reglas en {filepath}: {exc}")

    def load_from_file(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            logger.info("No se encontró archivo de reglas. Cargando reglas por defecto.")
            self._add_default_rules()
            self.save_to_file(filepath)
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.rules.clear()

            rules_data = None
            if isinstance(data, dict) and "rules" in data:
                rules_data = data["rules"]
            elif isinstance(data, list):
                rules_data = data
            else:
                raise ValueError(f"Formato inválido en archivo de reglas: {filepath}")

            for rule_dict in rules_data:
                rule_obj = SymbolicRule.from_dict(rule_dict)
                self.rules.setdefault(rule_obj.rol, []).append(rule_obj)

            self._remove_duplicates()
            self.save_to_file(filepath)
            logger.info(f"Reglas cargadas desde {filepath}")

        except Exception as exc:
            logger.error(f"Error cargando reglas desde {filepath}: {exc}")
            logger.info("Borrando reglas corruptas y restaurando por defecto...")
            self._reset_rules_file()


# Singleton export
symbolic_rule_engine = SymbolicRuleEngine()
