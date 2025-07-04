# daemon/evoai_initializer_core.py
# -*- coding: utf-8 -*-
"""
Inicializador del núcleo EvoAI.
Carga segura de configuración, contexto, agente, motor simbólico, decisión, ejecutor y herramientas.
Cumple con estándares gubernamentales, científicos y de ultra secreto.
"""

import os
import logging
import importlib.util

from core.config import Config
from core.context import EvoContext
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine

from daemon.evoai_initializer_security import load_secure_key
from daemon.evoai_initializer_agent import initialize_agent
from daemon.evoai_initializer_engine import initialize_engine
from daemon.evoai_initializer_executor import initialize_executor
from daemon.evoai_initializer_tools import initialize_support_tools
from daemon.evoai_initializer_decision import initialize_decision

logger = logging.getLogger("EvoAI.Core")

def initialize_core_components(initial_state=None):
    logger.info("[INIT] Inicializando núcleo EvoAI...")
    print("[🔧 INIT] Entrando en initialize_core_components()")

    # 🔐 Seguridad: Cargar clave maestra
    daemon_key = load_secure_key()
    print("[🔐 SECURITY] Clave maestra cargada correctamente.")

    # ⚙️ Cargar configuración global
    try:
        Config.load_from_file("config/evo_config.json")
        logger.info("[CONFIG] Configuración cargada exitosamente.")
        print("[⚙️ CONFIG] Configuración cargada desde config/evo_config.json")
    except Exception as e:
        logger.critical(f"[CONFIG] Fallo al cargar configuración: {e}")
        print(f"[❌ ERROR] Fallo al cargar configuración: {e}")
        raise SystemExit(1)

    # 🧠 Inicializar contexto simbiótico-evolutivo (pasando estado si existe)
    try:
        context = EvoContext(initial_state=initial_state or {})
        print("[🧠 CONTEXT] Contexto simbiótico inicializado.")
    except Exception as e:
        print(f"[❌ ERROR] Fallo al inicializar contexto: {e}")
        raise SystemExit(1)

    # 🤖 Inicializar agente principal
    agent = initialize_agent(context=context)
    print("[🤖 AGENT] Agente principal inicializado.")

    # 🔁 Inicializar motor de aprendizaje/evolución
    engine = initialize_engine(agent, context)
    print("[🔁 ENGINE] Motor evolutivo inicializado.")

    # 📄 Verificar existencia del archivo consolidado
    preferred_rules = "data/symbolic_rule_engine_consolidated.json"
    fallback_rules = "data/symbolic_rule_engine_consolidated.json"
    print(f"[📄 RULES] Verificando archivo de reglas preferido: {preferred_rules}")

    if not os.path.exists(preferred_rules):
        print(f"[⚠️ WARNING] Archivo {preferred_rules} no encontrado. Ejecutando auditoría simbólica...")
        try:
            spec = importlib.util.spec_from_file_location("rule_auditor", "tools/rule_auditor.py")
            rule_auditor = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(rule_auditor)
            rule_auditor.main()
            print("[🧼 AUTOAUDIT] Auditoría simbólica ejecutada correctamente.")
        except Exception as e:
            print(f"[❌ ERROR] Fallo al ejecutar auditoría automática: {e}")
            raise SystemExit(1)
    else:
        print(f"[✅ RULES] Archivo {preferred_rules} disponible. No se requiere auditoría.")

    # 🧠 Cargar motor simbólico desde archivo válido
    rules_path = preferred_rules if os.path.exists(preferred_rules) else fallback_rules
    logger.info(f"[RULES] Usando archivo de reglas simbólicas: {rules_path}")
    print(f"[📄 RULES] Cargando reglas simbólicas desde: {rules_path}")
    symbolic_engine = SymbolicRuleEngine(rules_file=rules_path)
    print("[🧠 SYMBOLIC] Motor simbólico cargado exitosamente.")

    # 📈 Inicializar componente de decisión simbólica
    decision = initialize_decision(context, agent, symbolic_engine)
    print("[📈 DECISION] Componente de decisión simbólica inicializado.")

    # 🚀 Inicializar ejecutores del ciclo
    executor = initialize_executor(agent, engine, context)
    print("[🚀 EXECUTOR] Ejecutores del ciclo inicializados.")

    # 🧰 Inicializar herramientas de soporte
    tools = initialize_support_tools(engine, context, daemon_key)
    print("[🧰 TOOLS] Herramientas de soporte inicializadas.")

    logger.info("[INIT] Núcleo EvoAI completamente inicializado y seguro.")
    print("[✅ INIT] Núcleo EvoAI completamente operativo.")

    return {
        "context": context,
        "agent": agent,
        "engine": engine,
        "decision": decision,
        "executor": executor,
        **tools,
    }
