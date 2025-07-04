#!/usr/bin/env python3
# patch_default_rules.py

from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine, SymbolicRule

class PatchedSymbolicRuleEngine(SymbolicRuleEngine):
    def _add_default_rules(self) -> None:
        default_rules = [
            SymbolicRule("action", "explore", "move_forward", "noise == 'calm'"),
            SymbolicRule("action", "rest", "pause", "noise == 'chaos'"),
            SymbolicRule("state", "active", "explore", "pos >= 0"),
            SymbolicRule("entropy", "force_random_action", "disrupt_context",
                         "entropy == 0.0 and last_action"accion" == 'noop'")
        ]
        for rule in default_rules:
            print(f"[➕ PATCH_RULE] Añadiendo: {rule}")
            self.add_rule(rule)

print("[🔁 PATCH] Aplicando parche a reglas por defecto...")
engine = PatchedSymbolicRuleEngine(auto_load=False)
engine._add_default_rules()
engine.save_to_file("data/symbolic_rule_engine_consolidated.json")  # ✅ RUTA ACTUALIZADA
print("[✅ PATCH] Parche aplicado y reglas guardadas.")
