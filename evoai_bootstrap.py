# evoai_bootstrap.py

import os
import datetime
from symbolic_ai.symbolic_rule import SymbolicRule
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine
from symbolic_ai.symbolic_context import SymbolicContext

from utils.logger import log  # Logging unificado obligatorio
from utils.default_rules import get_default_rules  # Carga opcional de reglas base


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

    if context_data and not isinstance(context_data, dict):
        raise TypeError(f"Contexto inválido: se esperaba dict, se recibió {type(context_data).__name__}")

    context = SymbolicContext()
    if context_data:
        # Insertar cada clave-valor como un dict independiente en la historia para que el __getitem__ funcione correctamente
        for key, value in context_data.items():
            context.history.append({key: value})

    engine = SymbolicRuleEngine(auto_load=True)

    if custom_rules:
        if not all(isinstance(rule, str) for rule in custom_rules):
            raise ValueError("Todas las reglas personalizadas deben ser strings simbólicos.")

        # Validar formato estricto: debe contener '=>'
        formatted_rules = []
        for rule in custom_rules:
            if "=>" not in rule:
                raise ValueError(
                    f"Regla inválida, debe contener '=>'. Formato esperado: 'rol:valor => accion :: condicion'. Regla: {rule}"
                )
            formatted_rules.append(rule)

        for rule in formatted_rules:
            engine.add_rule(rule)

        # Guardar snapshot de reglas personalizadas
        os.makedirs("data", exist_ok=True)
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        file_path = f"data/symbolic_rules_snapshot_{timestamp}.json"
        engine.save_to_file(file_path)
        log(f"[📄 Bootstrap] Reglas personalizadas guardadas en: {file_path}", level="DEBUG")

    log(f"[✅ Bootstrap] Motor listo con {len(engine.rules)} reglas activas.", level="INFO")
    log(f"[📊 Contexto] Valores iniciales: {context.values}", level="DEBUG")

    return engine, context
