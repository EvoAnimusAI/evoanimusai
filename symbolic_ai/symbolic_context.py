# symbolic_ai/symbolic_context.py

import json
import os
import datetime
import logging
from typing import List, Dict, Any, Optional, Union

from symbolic_ai.symbolic_rule import SymbolicRule
from .interpreter import ExpresionSimbolica

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class SymbolicContext:
    """
    Context manager for symbolic AI including history, expressions,
    metacognition, memory, and symbolic rules.
    """

    def __init__(self) -> None:
        self.history: List[Dict[str, Any]] = []
        self.expressions: List[ExpresionSimbolica] = []
        self.metacognition: List[Dict[str, str]] = []
        self.memory: List[Any] = []
        self.rules: List[SymbolicRule] = []
        print("[SYMBOLIC_CONTEXT] Initialized symbolic context")

    def register_metacognition(self, text: str) -> None:
        if not text or not isinstance(text, str):
            logger.warning("Metacognition text must be a non-empty string.")
            return
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        self.metacognition.append({"text": text, "timestamp": timestamp})
        print(f"[SYMBOLIC_CONTEXT] Registered metacognition: {text} @ {timestamp}")

    def load_rules(self, path: str = "data/symbolic_rule_engine_consolidated.json") -> None:
        print(f"[SYMBOLIC_CONTEXT] Loading rules from {path}")
        if not os.path.isfile(path):
            logger.warning(f"Rules file not found at: {path}")
            print(f"[SYMBOLIC_CONTEXT] File not found: {path}")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                rules_data = json.load(f)

            loaded_rules = []
            for r in rules_data:
                if isinstance(r, dict):
                    rule = SymbolicRule.from_dict(r)
                    loaded_rules.append(rule)
                    self.add_expression(getattr(rule, "text", ""))
                elif isinstance(r, SymbolicRule):
                    loaded_rules.append(r)
                    self.add_expression(getattr(r, "text", ""))
                else:
                    logger.warning(f"Skipped invalid rule entry: {r}")
                    print(f"[SYMBOLIC_CONTEXT] Skipped invalid rule entry: {r}")

            self.rules = loaded_rules
            print(f"[SYMBOLIC_CONTEXT] Loaded {len(self.rules)} rules from {path}")

        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading rules from {path}: {e}")
            print(f"[SYMBOLIC_CONTEXT] Error loading rules: {e}")

    def add_observation(self, observation: Dict[str, Any]) -> None:
        if not isinstance(observation, dict):
            logger.error("Observation must be a dictionary.")
            print("[SYMBOLIC_CONTEXT] Invalid observation format")
            return

        timestamp = observation.get("timestamp", datetime.datetime.utcnow().isoformat() + "Z")
        concept = {
            "concept": f"🌀 Observed: obs({observation.get('pos')}, "
                       f"{observation.get('visible')}, noise={observation.get('noise')}) @ {timestamp}",
            "timestamp": timestamp,
        }
        self.history.append(concept)
        print(f"[SYMBOLIC_CONTEXT] Added observation: {concept['concept']}")

    def add_expression(self, text: str) -> Optional[ExpresionSimbolica]:
        if not text or not isinstance(text, str):
            logger.warning("Expression text must be a non-empty string.")
            print("[SYMBOLIC_CONTEXT] Skipped empty expression")
            return None

        exp = ExpresionSimbolica.desde_texto(text)
        if exp:
            self.expressions.append(exp)
            print(f"[SYMBOLIC_CONTEXT] Added expression: {exp}")
            return exp

        logger.warning(f"Failed to parse expression from text: {text}")
        print(f"[SYMBOLIC_CONTEXT] Failed to parse: {text}")
        return None

    def get_active(self, context: Dict[str, str]) -> List[ExpresionSimbolica]:
        if not isinstance(context, dict):
            logger.error("Context must be a dictionary of string keys and values.")
            print("[SYMBOLIC_CONTEXT] Invalid context provided")
            return []

        active = [e for e in self.expressions if e.evaluate(context)]
        print(f"[SYMBOLIC_CONTEXT] {len(active)} active expressions for context: {context}")
        return active

    def add_concept(self, concept_str: str) -> None:
        if not concept_str or not isinstance(concept_str, str):
            logger.warning("Concept string must be a non-empty string.")
            return

        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        self.history.append({"concept": concept_str, "timestamp": timestamp})
        print(f"[SYMBOLIC_CONTEXT] Added concept: {concept_str}")

    def add_fact(self, fact: Dict[str, Any]) -> None:
        if not isinstance(fact, dict):
            raise TypeError("Fact must be a dictionary.")

        self.history.append(fact)
        print(f"[SYMBOLIC_CONTEXT] Added fact: {fact}")

    def save_context(self, filepath: str = "data/symbolic_context.json") -> None:
        state = {
            "rules": [r.to_dict() for r in self.rules],
            "memory": self.memory,
        }

        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            tmp_path = filepath + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, filepath)
            print(f"[SYMBOLIC_CONTEXT] Context saved to {filepath}")
        except (OSError, IOError) as e:
            logger.error(f"Failed to save context to {filepath}: {e}")
            print(f"[SYMBOLIC_CONTEXT] Failed to save context: {e}")

    def save_rules(self, filepath: str = "data/symbolic_rule_engine_consolidated.json") -> None:
        print(f"[SYMBOLIC_CONTEXT] Saving rules to {filepath}")
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            tmp_path = filepath + ".tmp"
            serialized_rules = [r.to_dict() for r in self.rules]
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(serialized_rules, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, filepath)
            print(f"[SYMBOLIC_CONTEXT] Rules saved to {filepath}")
        except (OSError, IOError) as e:
            logger.error(f"Failed to save symbolic rules to {filepath}: {e}")
            print(f"[SYMBOLIC_CONTEXT] Failed to save rules: {e}")

    def update(self, data: Dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise ValueError("Update data must be a dictionary.")

        history_data = data.get("history", [])
        if not all(isinstance(item, dict) for item in history_data):
            logger.warning("Some history entries are not dicts and will be skipped.")
        self.history.extend([item for item in history_data if isinstance(item, dict)])

        for expr in data.get("expressions", []):
            if isinstance(expr, str):
                self.add_expression(expr)
            else:
                logger.warning(f"Skipped non-string expression: {expr}")

        meta = data.get("metacognition", [])
        if not all(isinstance(m, dict) and "text" in m and "timestamp" in m for m in meta):
            logger.warning("Metacognition entries malformed and skipped.")
        else:
            self.metacognition.extend(meta)

        for rule_data in data.get("rules", []):
            if isinstance(rule_data, dict):
                try:
                    rule = SymbolicRule.from_dict(rule_data)
                    self.rules.append(rule)
                except Exception as e:
                    logger.error(f"Failed to load rule from dict: {e}")
                    print(f"[SYMBOLIC_CONTEXT] Failed to load rule: {e}")
            else:
                logger.warning(f"Skipped invalid rule entry: {rule_data}")

        memory_data = data.get("memory", [])
        if not isinstance(memory_data, list):
            logger.warning("Memory data is not a list and will be ignored.")
        else:
            self.memory.extend(memory_data)
        print(f"[SYMBOLIC_CONTEXT] Context updated with data keys: {list(data.keys())}")

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")

        for fact in reversed(self.history):
            if isinstance(fact, dict) and key in fact:
                print(f"[SYMBOLIC_CONTEXT] Retrieved key '{key}': {fact[key]}")
                return fact[key]

        raise KeyError(f"Key '{key}' not found in context history.")

    @property
    def values(self) -> Dict[str, Any]:
        snapshot = {
            "history": self.history.copy(),
            "expressions": [getattr(e, "text", str(e)) for e in self.expressions],
            "metacognition": self.metacognition.copy(),
            "rules": [getattr(r, "text", str(r)) for r in self.rules],
            "memory": self.memory.copy(),
        }
        print(f"[SYMBOLIC_CONTEXT] Snapshot of context requested")
        return snapshot


# Singleton instance for global use
symbolic_context = SymbolicContext()
