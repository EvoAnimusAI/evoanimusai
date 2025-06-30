"""
symbolic_interpreter.py

SymbolicInterpreter translates symbolic inputs into actionable environment instructions
based on symbolic noise semantics. Rules follow the format:
    ⟦role:value⟧ ⇒ action :: condition

Author: Daniel Santiago Ospina Velasquez :: AV255583
"""

from typing import Any, Dict, Optional
from symbolic_ai.symbolic_rule import SymbolicRule


class SymbolicInterpreter:
    """
    Interprets symbolic commands (e.g., 'decision based on: noise = chaos')
    and parses symbolic rules into structured objects.
    """

    def interpret(self, action_str: str, context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Interprets a symbolic action string and returns a structured command dictionary.

        Parameters:
            action_str (str): The symbolic action command.
            context (dict, optional): Contextual information (currently unused).

        Returns:
            dict or None: A structured action or None if the command is unrecognized.
        """
        if not isinstance(action_str, str) or not action_str.lower().startswith("decision based on: noise ="):
            return None

        noise_value = action_str.split("=")[-1].strip().lower()

        dispatch = {
            "chaos": self._move_randomly,
            "tension": self._explore,
            "harmonic": self._rest,
            "neutral": self._hold_position,
            "calm": self._observe,
        }

        handler = dispatch.get(noise_value)
        return handler(context or {}) if handler else None

    def parse_rule(self, rule_str: str) -> SymbolicRule:
        """
        Parses a symbolic rule string into a SymbolicRule object.

        Parameters:
            rule_str (str): Rule string in the format '⟦role:value⟧ ⇒ action :: condition'.

        Returns:
            SymbolicRule: The parsed symbolic rule.

        Raises:
            ValueError: If the rule format is invalid.
        """
        try:
            parts = rule_str.split("::")
            if len(parts) != 2:
                raise ValueError("Missing '::' separator in rule.")

            action_part, condition = parts
            if "⇒" not in action_part:
                raise ValueError("Missing '⇒' in rule.")

            rol_val, accion = action_part.split("⇒")
            rol_val = rol_val.strip()

            # Validación estricta de los delimitadores ⟦ ⟧
            if not rol_val.startswith("⟦") or not rol_val.endswith("⟧"):
                raise ValueError(f"Missing delimiters '⟦ ⟧' around role:value: '{rol_val}'")

            inner = rol_val.strip("⟦⟧ ").strip()
            if ':' not in inner:
                raise ValueError(f"Missing ':' in role:value: '{inner}'")

            rol, valor = inner.split(":", 1)
            return SymbolicRule(
                rol=rol.strip(),
                valor=valor.strip(),
                accion=accion.strip(),
                condicion=condition.strip(),
                texto=rule_str.strip()
            )
        except Exception as e:
            raise ValueError(f"[❌ parse_rule] Failed to parse rule: '{rule_str}' :: {e}")

    # --- Internal symbolic action handlers ---

    def _move_randomly(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "move",
            "mode": "random",
            "reason": "chaotic_noise",
            "energy_required": 5
        }

    def _explore(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "explore",
            "intensity": "high",
            "depth": 3,
            "energy_required": 8
        }

    def _rest(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "rest",
            "duration": 2,
            "reason": "harmony_detected",
            "energy_gained": 10
        }

    def _hold_position(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "wait",
            "duration": 1,
            "reason": "neutral_state",
            "energy_required": 1
        }

    def _observe(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "observe",
            "area": "local_environment",
            "reason": "symbolic_calm",
            "energy_required": 2
        }
