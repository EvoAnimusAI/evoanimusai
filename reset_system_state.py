#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import traceback
from datetime import datetime

from symbolic_ai.symbolic_context import SymbolicContext
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine
from core.symbolic_decision_engine import SymbolicDecisionEngine
from utils.cond_error_handler import CondErrorHandler

# Utilitario de impresión con timestamp
def printf(tag, msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{tag}] {msg}")

# Fallbacks por defecto
fallbacks = {'pos': 0, 'noise': 'calm', 'state': 'unknown'}

# Reinicio simbólico robusto
try:
    printf("🔧 INIT", "CondErrorHandler inicializado.")
    handler = CondErrorHandler()

    printf("⚙️ CONFIG", f"Fallbacks definidos: {fallbacks}")

    printf("⚙️ INIT", "Inicializando SymbolicRuleEngine...")
    symbolic_engine = SymbolicRuleEngine()
    
    try:
        with open("data/symbolic_rule_engine.json", "r", encoding="utf-8") as f:
            reglas_raw = json.load(f)
        for regla in reglas_raw:
            symbolic_engine.add_rule_from_dict(regla)
        printf("✅ RULE_ENGINE", f"Motor simbólico cargado con {len(reglas_raw)} reglas.")
    except Exception as e:
        printf("❌ RULE_ENGINE", f"Error al cargar reglas desde JSON: {e}")
        raise

    symbolic_context = SymbolicContext()
    symbolic_context.rule_engine = symbolic_engine
    printf("SYMBOLIC_CONTEXT", "Contexto simbólico inicializado.")

    # Exploración de existencia de EvoContext
    printf("🔎 SEARCH", "Buscando clase EvoContext...")
    evo_context = None

    try:
        from core.context import EvoContext
        if issubclass(EvoContext, SymbolicContext):
            printf("🧠 CONTEXT", "Iniciando EvoContext...")
            evo_context = EvoContext()
            printf("✅ CONTEXT", "EvoContext instanciado correctamente.")
        else:
            raise TypeError("EvoContext no es subclase de SymbolicContext.")
    except Exception as e:
        printf("⚠️ CONTEXT", f"Fallo al iniciar EvoContext: {e}")
        evo_context = symbolic_context  # fallback

    # Inicializar motor de decisiones
    try:
        decision_engine = SymbolicDecisionEngine(context=evo_context)
        printf("✅ DECISION_ENGINE", "Motor de decisiones simbólicas inicializado.")
    except Exception as e:
        printf("❌ DECISION_ENGINE", f"Fallo al inicializar motor de decisiones: {e}")
        traceback.print_exc()
        sys.exit(1)

    printf("🔄 RESET", "Sistema simbólico reiniciado exitosamente.")

except Exception as ex:
    printf("❌ ERROR", "Fallo durante el reinicio del sistema simbólico.")
    traceback.print_exc()
    sys.exit(1)
