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
        self.facts: Dict[str, Any] = {}  # <--- aquí se almacenan los hechos afirmados
        if auto_load:
            self.load_from_file(self.rules_file)

    def flatten_context(self, d, parent_key='', sep='.'):
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self.flatten_context(v, new_key, sep=sep))
            else:
                items[new_key] = v
        if not parent_key:
            items.update(d)
        return items

    def evaluate(self, contexto: dict) -> List[SymbolicRule]:
        print(f"[🧠 EVALUATE] Contexto recibido: {contexto}")
        if "last_action" in contexto and isinstance(contexto["last_action"], dict):
            last_action = contexto["last_action"]
            for key in ("entropy", "state", "noise"):
                if key not in contexto or contexto[key] is None:
                    if key in last_action and last_action[key] is not None:
                        contexto[key] = last_action[key]
                        print(f"[🛡️ PROPAGATE] {key} extraído desde last_action.{key} → {contexto[key]}")
        flat_context = self.flatten_context(contexto)
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

    def insertar_regla(self, regla: dict) -> None:
        print(f"[➕ INSERTAR_REGLA] Insertando regla nueva: {regla}")
        if not isinstance(regla, dict):
            raise TypeError("[INSERTAR_REGLA] Se esperaba un diccionario con datos de regla.")
        try:
            nueva_regla = SymbolicRule.from_dict(regla)
            if any(r == nueva_regla for r in self.rules.get(nueva_regla.rol, [])):
                print(f"[⚠️ INSERTAR_REGLA] Regla duplicada detectada, se ignora: {nueva_regla}")
                return
            self.rules[nueva_regla.rol].append(nueva_regla)
            self.save_to_file(self.rules_file)
            print(f"[✅ INSERTAR_REGLA] Regla insertada correctamente.")
        except Exception as e:
            print(f"[❌ ERROR][INSERTAR_REGLA] Fallo al insertar regla: {e}")
            raise

    def get_all(self) -> List[SymbolicRule]:
        print("[📥 GET_ALL] Recuperando todas las reglas...")
        return [rule for rule_list in self.rules.values() for rule in rule_list]

    def clear_rules(self) -> None:
        print("[🧹 CLEAR_RULES] Limpiando todas las reglas simbólicas...")
        self.rules.clear()
        logger.info("[CLEAR] Todas las reglas simbólicas han sido eliminadas.")

    def save_to_file(self, filepath: str) -> None:
        all_rules = [rule.to_dict() for rule_list in self.rules.values() for rule in rule_list]
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
            rules_data = data.get("rules", [])
            for rule_dict in rules_data:
                rule_obj = SymbolicRule.from_dict(rule_dict)
                self.rules[rule_obj.rol].append(rule_obj)
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
            self.rules.setdefault(rule.rol, []).append(rule)

    def assert_fact(self, key: str, value: Any) -> None:
        print(f"[➕ ASSERT_FACT] Registrando hecho simbólico: {key} = {value}")
        try:
            self.facts[key] = value
            logger.info(f"[ASSERT_FACT] Hecho registrado: {key} = {value}")
        except Exception as e:
            logger.error(f"[ERROR] Fallo en assert_fact('{key}', {value}): {e}")
            raise

# Instancia global
symbolic_rule_engine = SymbolicRuleEngine()
