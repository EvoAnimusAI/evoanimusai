# symbolic_ai/symbolic_rule_engine.py
import json
import os
import logging
from collections import defaultdict
from typing import List, Dict, Optional, Union, Any

from symbolic_ai.symbolic_rule import SymbolicRule

logger = logging.getLogger("EvoAI.SymbolicRuleEngine")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

RULES_FILE = "data/symbolic_rule_engine.json"

class SymbolicRuleEngine:
    def __init__(self, auto_load: bool = True, rules_file: Optional[str] = None) -> None:
        print("[⚙️ INIT] Inicializando SymbolicRuleEngine...")
        self.rules_file = rules_file or RULES_FILE
        self.rules: Dict[str, List[SymbolicRule]] = defaultdict(list)
        if auto_load:
            self.load_from_file(self.rules_file)

    def evaluate(self, contexto: dict) -> List[SymbolicRule]:
        def flatten_context(d, parent_key='', sep='.'):
            items = {}
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.update(flatten_context(v, new_key, sep=sep))
                else:
                    items[new_key] = v
            if not parent_key:
                items.update(d)
            return items

        print(f"[🧠 EVALUATE] Contexto recibido: {contexto}")

        # --- Propagación desde last_action ---
        if "last_action" in contexto and isinstance(contexto["last_action"], dict):
            last_action = contexto["last_action"]
            for key in ("entropy", "state", "noise"):
                if key not in contexto or contexto[key] is None:
                    if key in last_action and last_action[key] is not None:
                        contexto[key] = last_action[key]
                        print(f"[🛡️ PROPAGATE] {key} extraído desde last_action.{key} → {contexto[key]}")

        flat_context = flatten_context(contexto)
        print(f"[🧪 CONTEXTO FLATTEN]: {flat_context}")

        matched_rules = []
        total = sum(len(r) for r in self.rules.values())
        count = 0
        print(f"[📊 EVALUATE] Total reglas disponibles: {total}")

        for rule_list in self.rules.values():
            for rule in rule_list:
                count += 1
                print(f"[🔁 PROGRESO] Evaluando regla {count}/{total}: {rule}")
                print(f"     ↳ Condición: {rule.condicion}")
                try:
                    result = rule.evaluar(flat_context)
                    print(f"     ✅ Resultado: {result}")
                    if result:
                        matched_rules.append(rule)
                except Exception as exc:
                    logger.error(f"[EVALUATE] Error evaluando regla {rule}: {exc}")
                    print(f"[❌ EVALUATE ERROR] Regla: {rule} — Excepción: {exc}")

        print(f"[✅ EVALUATE] Total reglas activadas: {len(matched_rules)}")
        return matched_rules

    def apply_rules(self, contexto: dict) -> List[SymbolicRule]:
        print(f"[🚀 APPLY_RULES] Ejecutando reglas sobre contexto: {contexto}")
        return self.evaluate(contexto)

    def assert_fact(self, key: str, value: Any) -> List[SymbolicRule]:
        print(f"[➕ ASSERT_FACT] Afirmando hecho: {key} = {value}")
        if not isinstance(key, str):
            raise TypeError(f"[ASSERT_FACT] Clave inválida, se esperaba str y se recibió {type(key)}")
        contexto = {key: value}
        matched = self.evaluate(contexto)
        print(f"[📊 ASSERT_FACT] Reglas activadas: {[r.name for r in matched]}")
        return matched

    def assert_facts_bulk(self, facts: Dict[str, Any]) -> List[SymbolicRule]:
        print(f"[📦 ASSERT_FACTS_BULK] Hechos: {facts}")
        if not isinstance(facts, dict):
            raise TypeError(f"[ASSERT_FACTS_BULK] Se esperaba dict, se recibió {type(facts)}")
        matched = self.evaluate(facts)
        print(f"[📊 BULK] Reglas activadas: {[r.name for r in matched]}")
        return matched

    def add_rule(self, rule: Union[str, dict, SymbolicRule]) -> None:
        print(f"[➕ ADD_RULE] Agregando regla: {rule}")
        if isinstance(rule, str):
            rule = SymbolicRule.parse(rule)
        elif isinstance(rule, dict):
            rule = SymbolicRule.from_dict(rule)
        elif not isinstance(rule, SymbolicRule):
            raise TypeError(f"Expected SymbolicRule, dict, or str, got {type(rule)}")

        if any(existing == rule for existing in self.rules.get(rule.rol, [])):
            logger.warning(f"[ADD_RULE] Regla duplicada ignorada: {rule}")
            return

        self.rules.setdefault(rule.rol, []).append(rule)
        self.save_to_file(self.rules_file)
        logger.info(f"[ADD_RULE] Regla añadida: {rule}")

    def remove_rule(self, rule: Union[str, dict, SymbolicRule]) -> bool:
        print(f"[🗑️ REMOVE_RULE] Eliminando regla: {rule}")
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
                logger.info(f"[REMOVE_RULE] Regla eliminada: {rule}")
                return True

        logger.warning(f"[REMOVE_RULE] No se encontró la regla para eliminar: {rule}")
        return False

    def update_rule(self, new_rule: dict) -> None:
        print(f"[🔁 UPDATE_RULE] Actualizando regla con acción: {new_rule.get('action')}")
        try:
            if not isinstance(new_rule, dict):
                raise TypeError(f"[UPDATE_RULE] Se esperaba dict, se recibió {type(new_rule)}")
            if 'action' not in new_rule:
                raise ValueError("[UPDATE_RULE] La regla debe contener la clave 'action'.")

            accion = new_rule['action']
            actualizado = False
            for rule_list in self.rules.values():
                for i, rule in enumerate(rule_list):
                    if rule.accion == accion:
                        rule_dict = rule.to_dict()
                        rule_dict.update(new_rule)
                        updated_rule = SymbolicRule.from_dict(rule_dict)
                        rule_list[i] = updated_rule
                        actualizado = True
                        logger.info(f"[UPDATE_RULE] Regla actualizada: {updated_rule}")
                        break
                if actualizado:
                    break

            if not actualizado:
                nueva_regla = SymbolicRule.from_dict(new_rule)
                self.rules.setdefault(nueva_regla.rol, []).append(nueva_regla)
                logger.info(f"[UPDATE_RULE] Regla insertada: {nueva_regla}")

            self.save_to_file(self.rules_file)

        except Exception as e:
            logger.error(f"[UPDATE_RULE] Error: {e}")
            raise

    def get_rule_by_action(self, accion: str) -> Optional[SymbolicRule]:
        print(f"[🔍 GET_RULE] Buscando regla por acción: {accion}")
        for rule_list in self.rules.values():
            for rule in rule_list:
                if rule.accion == accion:
                    return rule
        return None

    def reset(self) -> None:
        print("[♻️ RESET] Reiniciando reglas simbólicas...")
        self.rules.clear()
        self._add_default_rules()
        self.save_to_file(self.rules_file)
        logger.info("[RESET] Entorno simbólico reiniciado con reglas por defecto.")

    def clear_rules(self) -> None:
        print("[🧹 CLEAR_RULES] Limpiando todas las reglas simbólicas...")
        self.rules.clear()
        logger.info("[CLEAR] Todas las reglas simbólicas han sido eliminadas.")

    def save_to_file(self, filepath: str) -> None:
        all_rules = [
            rule.to_dict()
            for rule_list in self.rules.values()
            for rule in rule_list
        ]
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({"rules": all_rules}, f, indent=2, ensure_ascii=False)
            logger.info(f"[SAVE] Reglas guardadas en {filepath}")
        except Exception as exc:
            logger.error(f"[SAVE] Error guardando reglas en {filepath}: {exc}")

    def load_from_file(self, filepath: str) -> None:
        print(f"[📂 LOAD] Cargando reglas desde archivo: {filepath}")
        if not os.path.exists(filepath):
            logger.info("[LOAD] Archivo no encontrado. Cargando reglas por defecto.")
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
            logger.info(f"[LOAD] Reglas cargadas desde {filepath}")
        except Exception as exc:
            logger.error(f"[LOAD] Error cargando reglas desde {filepath}: {exc}")
            logger.warning("[LOAD] Restaurando reglas por defecto tras corrupción.")
            self._reset_rules_file()

    def _remove_duplicates(self) -> None:
        print("[🧽 DEDUPE] Eliminando reglas duplicadas...")
        for rol, rule_list in self.rules.items():
            unique_rules = []
            for rule in rule_list:
                if rule not in unique_rules:
                    unique_rules.append(rule)
            self.rules[rol] = unique_rules

    def _reset_rules_file(self) -> None:
        print("[🧯 RESET_FILE] Reiniciando archivo de reglas...")
        try:
            if os.path.exists(self.rules_file):
                os.remove(self.rules_file)
                logger.info(f"[RESET] Archivo de reglas corrupto eliminado: {self.rules_file}")
        except Exception as exc:
            logger.error(f"[RESET] Error eliminando archivo corrupto {self.rules_file}: {exc}")
        self.rules.clear()
        self._add_default_rules()
        self.save_to_file(self.rules_file)

    def _add_default_rules(self) -> None:
        print("[➕ DEFAULT_RULES] Insertando reglas por defecto...")
        default_rules = [
            SymbolicRule("action", "explore", "move_forward", "noise == 'calm'"),
            SymbolicRule("action", "rest", "pause", "noise == 'chaos'"),
            SymbolicRule("state", "active", "explore", "pos >= 0"),
        ]
        for rule in default_rules:
            self.add_rule(rule)

    def get_all(self) -> List[SymbolicRule]:
        print("[📥 GET_ALL] Recuperando todas las reglas...")
        return [rule for rule_list in self.rules.values() for rule in rule_list]


# Instancia global
symbolic_rule_engine = SymbolicRuleEngine()
