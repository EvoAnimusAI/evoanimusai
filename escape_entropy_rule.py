#!/usr/bin/env python3
# escape_entropy_rule.py

from symbolic_ai.symbolic_rule_engine import symbolic_rule_engine

escape_rule = {
    "rol": "entropy",
    "accion": "force_random_action",
    "consecuencia": "disrupt_context",
    "condicion": "entropy == 0.0 and last_action"accion" == 'noop'",
    "descripcion": "Escape simbólico ante ciclo de entropía nula persistente",
    "prioridad": 99
}

print("[🔧 PATCH] Añadiendo regla simbólica de escape por entropía nula...")
symbolic_rule_engine.add_rule(escape_rule)
print("[✅ PATCH] Regla de escape añadida exitosamente.")
