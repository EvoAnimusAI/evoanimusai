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

    def register_metacognition(self, text: str) -> None:
        """
        Registers a metacognitive insight with timestamp.
        """
        if not text or not isinstance(text, str):
            logger.warning("Metacognition text must be a non-empty string.")
            return
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        self.metacognition.append({"text": text, "timestamp": timestamp})
        logger.info(f"Metacognition recorded: {text} @ {timestamp}")

    def load_rules(self, path: str = "data/symbolic_rule_engine.json") -> None:
        """
        Loads symbolic rules from a JSON file into the context.
        """
        if not os.path.isfile(path):
            logger.warning(f"Rules file not found at: {path}")
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

            self.rules = loaded_rules
            logger.info(f"Rules successfully loaded from {path}")

        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading rules from {path}: {e}")

    def add_observation(self, observation: Dict[str, Any]) -> None:
        """
        Adds a new observation concept to the history with timestamp.
        """
        if not isinstance(observation, dict):
            logger.error("Observation must be a dictionary.")
            return

        timestamp = observation.get("timestamp", datetime.datetime.utcnow().isoformat() + "Z")
        concept = {
            "concept": f"🌀 Observed: obs({observation.get('pos')}, "
                       f"{observation.get('visible')}, noise={observation.get('ruido')}) @ {timestamp}",
            "timestamp": timestamp,
        }
        self.history.append(concept)
        logger.debug(f"Concept added to history: {concept['concept']}")

    def add_expression(self, text: str) -> Optional[ExpresionSimbolica]:
        """
        Adds a symbolic expression parsed from text if valid.
        """
        if not text or not isinstance(text, str):
            logger.warning("Expression text must be a non-empty string.")
            return None

        exp = ExpresionSimbolica.desde_texto(text)
        if exp:
            self.expressions.append(exp)
            logger.info(f"Expression added: {exp}")
            return exp

        logger.warning(f"Failed to parse expression from text: {text}")
        return None

    def get_active(self, context: Dict[str, str]) -> List[ExpresionSimbolica]:
        """
        Returns expressions active under given context.
        """
        if not isinstance(context, dict):
            logger.error("Context must be a dictionary of string keys and values.")
            return []

        active = [e for e in self.expressions if e.evaluate(context)]
        logger.debug(f"{len(active)} expressions activated.")
        return active

    def add_concept(self, concept_str: str) -> None:
        """
        Adds a new concept to the history.
        """
        if not concept_str or not isinstance(concept_str, str):
            logger.warning("Concept string must be a non-empty string.")
            return

        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        self.history.append({"concept": concept_str, "timestamp": timestamp})
        logger.debug(f"Concept added: {concept_str}")

    def add_fact(self, fact: Dict[str, Any]) -> None:
        """
        Adds a fact to the history after validation.
        """
        if not isinstance(fact, dict):
            raise TypeError("Fact must be a dictionary.")

        self.history.append(fact)
        logger.debug(f"Fact added: {fact}")

    def save_context(self, filepath: str = "data/symbolic_context.json") -> None:
        """
        Saves the current context state (rules and memory) to JSON.
        Uses atomic write to prevent corruption.
        """
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
            logger.info(f"Context saved successfully to {filepath}")
        except (OSError, IOError) as e:
            logger.error(f"Failed to save context to {filepath}: {e}")

    def save_rules(self, filepath: str = "data/symbolic_rule_engine.json") -> None:
        """
        Saves the symbolic rules to a JSON file with atomic write.
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            tmp_path = filepath + ".tmp"
            serialized_rules = [r.to_dict() for r in self.rules]
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(serialized_rules, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, filepath)
            logger.info(f"Symbolic rules saved successfully to {filepath}")
        except (OSError, IOError) as e:
            logger.error(f"Failed to save symbolic rules to {filepath}: {e}")

    def update(self, data: Dict[str, Any]) -> None:
        """
        Updates context from a dictionary, validating inputs.
        """
        if not isinstance(data, dict):
            raise ValueError("Update data must be a dictionary.")

        # Validate and extend history
        history_data = data.get("history", [])
        if not all(isinstance(item, dict) for item in history_data):
            logger.warning("Some history entries are not dicts and will be skipped.")
        self.history.extend([item for item in history_data if isinstance(item, dict)])

        # Add expressions
        for expr in data.get("expressions", []):
            if isinstance(expr, str):
                self.add_expression(expr)
            else:
                logger.warning(f"Skipped non-string expression: {expr}")

        # Extend metacognition if valid
        meta = data.get("metacognition", [])
        if not all(isinstance(m, dict) and "text" in m and "timestamp" in m for m in meta):
            logger.warning("Metacognition entries malformed and skipped.")
        else:
            self.metacognition.extend(meta)

        # Add rules
        for rule_data in data.get("rules", []):
            if isinstance(rule_data, dict):
                try:
                    rule = SymbolicRule.from_dict(rule_data)
                    self.rules.append(rule)
                except Exception as e:
                    logger.error(f"Failed to load rule from dict: {e}")
            else:
                logger.warning(f"Skipped invalid rule entry: {rule_data}")

        # Extend memory
        memory_data = data.get("memory", [])
        if not isinstance(memory_data, list):
            logger.warning("Memory data is not a list and will be ignored.")
        else:
            self.memory.extend(memory_data)

    def __getitem__(self, key: str) -> Any:
        """
        Retrieves the most recent fact value by key from history.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")

        for fact in reversed(self.history):
            if isinstance(fact, dict) and key in fact:
                return fact[key]

        raise KeyError(f"Key '{key}' not found in context history.")

    @property
    def values(self) -> Dict[str, Any]:
        """
        Returns a serializable snapshot of current context.
        """
        return {
            "history": self.history.copy(),
            "expressions": [getattr(e, "text", str(e)) for e in self.expressions],
            "metacognition": self.metacognition.copy(),
            "rules": [getattr(r, "text", str(r)) for r in self.rules],
            "memory": self.memory.copy(),
        }


# Singleton instance for global use
symbolic_context = SymbolicContext()
