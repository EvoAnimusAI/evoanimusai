# evoai_bootstrap.py
# -*- coding: utf-8 -*-

import os
import datetime

from symbolic_ai.symbolic_rule import SymbolicRule
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine
from symbolic_ai.symbolic_context import SymbolicContext

from utils.logger import log  # Logging unificado obligatorio
from utils.default_symbolic_rules import get_default_symbolic_rules  # Reglas simbólicas por defecto


def bootstrap_evoai(context_data: dict = None, custom_rules: list[str] = None):
    """
    Inicializa EvoAI con contexto simbólico y motor de reglas configurado.

    Args:
        context_data (dict): Diccionario con datos iniciales del contexto simbólico.
        custom_rules (list[str]): Reglas simbólicas personalizadas en formato 'rol:valor => accion :: condicion'.

    Returns:
        Tuple[SymbolicRuleEngine, SymbolicContext]: Instancias listas para operación.

    Raises:
        ValueError: Si alguna regla no cumple el formato esperado.
        TypeError: Si context_data no es dict.
    """
    log("[🚀 Bootstrap] Inicializando entorno EvoAI...", level="INFO")
    print("[🟢] Iniciando bootstrap EvoAI...")

    if context_data and not isinstance(context_data, dict):
        raise TypeError(f"Contexto inválido: se esperaba dict, se recibió {type(context_data).__name__}")

    context = SymbolicContext()
    if context_data:
        for key, value in context_data.items():
            context.history.append({key: value})
        print(f"[📥 CONTEXTO INICIAL] {context_data}")

    engine = SymbolicRuleEngine(auto_load=True)
    print("[⚙️] Motor de reglas cargado.")

    if not custom_rules:
        print("[ℹ️] No se especificaron reglas personalizadas. Cargando reglas por defecto.")
        custom_rules = get_default_symbolic_rules()

    if not all(isinstance(rule, str) for rule in custom_rules):
        raise ValueError("Todas las reglas personalizadas deben ser strings simbólicos.")

    formatted_rules = []
    for rule in custom_rules:
        if "=>" not in rule or "::" not in rule:
            raise ValueError(f"Regla inválida: {rule}. Formato esperado: 'rol:valor => accion :: condicion'")
        formatted_rules.append(rule)

    for rule in formatted_rules:
        print(f"[➕ REGLA] {rule}")
        engine.add_rule(rule)

    os.makedirs("data", exist_ok=True)
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    file_path = f"data/symbolic_rules_snapshot_{timestamp}.json"
    engine.save_to_file(file_path)
    log(f"[📄 Bootstrap] Reglas guardadas en: {file_path}", level="DEBUG")
    print(f"[💾 SNAPSHOT] Guardado en {file_path}")

    total_reglas = sum(len(rules) for rules in engine.rules.values())
    print(f"[✅] Motor simbólico listo con {total_reglas} reglas.")
    print(f"[📊 REGLAS ACTIVAS]")
    for rol, rules in engine.rules.items():
        print(f"   - {rol}: {len(rules)} reglas")

    print(f"[📦 CONTEXTO FINAL] {context.values}")
    log(f"[✅ Bootstrap] Motor listo con {len(engine.rules)} reglas activas.", level="INFO")
    log(f"[📊 Contexto] Valores iniciales: {context.values}", level="DEBUG")

    return engine, context
