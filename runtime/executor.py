# -*- coding: utf-8 -*-
"""
Executor principal de EvoAnimusAI. Gestiona acciones, decisiones, mutaciones
y adaptación simbólica con control de entropy y seguridad estructural.
"""

import ast
import random
import time
import traceback
from typing import Optional

from behavior.action_registry import ActionRegistry
from metacognition.autonomous_stop import evaluate_contextual_stop
from symbolic_ai.hypermutation import hypermutation
from symbolic_ai.hypermutator import mutate_complete_function
from symbolic_ai.function_evaluator import evaluate_mutated_function
from symbolic_ai.symbolic_rule_engine import symbolic_rule_engine as symbolic_engine_instance
from runtime.rule_adaptation import adapt_rules, fallback_adapt_rules
from utils import evo_logging as logging
from utils.observer import SymbioticObserver

# Integración militar/gubernamental de activación automática de mutaciones
from symbolic_ai.mutation_trigger import MutationTrigger


class Executor:
    HYPERMUTATION_PROBABILITY = 0.02
    ENTROPY_THRESHOLD = 0.7
    RULE_MUTATION_PROBABILITY = 0.05
    FUNCTION_MUTATION_PROBABILITY = 0.03
    ACTION_REPEAT_LIMIT = 5
    SYMBOLIC_PERSISTENCE_INTERVAL = 10

    def __init__(
        self,
        agent,
        context: Optional[dict] = None,
        engine=None,
        environment=None,
        monitor=None,
    ) -> None:
        self.agent = agent
        self.context = context or {}
        self.engine = engine or symbolic_engine_instance
        self.environment = environment
        self.monitor = monitor

        self.action_registry = ActionRegistry()
        self.observer = SymbioticObserver()

        self._symbolic_step = 0
        self._previous_action: Optional[str] = None
        self._action_repeats: int = 0
        self._force_explore: bool = False

        # Instancia única de MutationTrigger para activar mutaciones automáticas
        self.mutation_trigger = MutationTrigger()

    def run(self, steps: int = 100) -> None:
        try:
            for step in range(1, steps + 1):
                logging.log("EXECUTOR", f"Step {step}/{steps} started.", level="DEBUG")
                print(f"[DEBUG] Step {step}/{steps} started.")

                if self.environment:
                    if not self._run_environment_step(step):
                        logging.log("EXECUTOR", "Execution terminated by environment.", level="INFO")
                        print("[INFO] Execution terminated by environment.")
                        break
                else:
                    self._run_symbolic_step(step)

        except KeyboardInterrupt:
            logging.log("EXECUTOR", "Execution manually interrupted.", level="WARNING")
            print("[WARNING] Execution manually interrupted.")
            self.stop()
        except StopIteration as si:
            logging.log("EXECUTOR", f"Autonomous stop triggered: {si}", level="INFO")
            print(f"[INFO] Autonomous stop triggered: {si}")
            self.stop()
        except Exception as exc:
            logging.log("EXECUTOR", f"Unexpected error: {exc}", level="ERROR")
            logging.log("TRACEBACK", traceback.format_exc(), level="ERROR")
            print(f"[ERROR] Unexpected error: {exc}")
            self.stop()

    def _run_symbolic_step(self, step: int) -> None:
        context = self._ensure_valid_context(self.context)
        decision = self.engine.decide(context)
        print(f"[DECISION] Step {step}: {decision}")
        result = self._execute_action_with_logging(decision)

        self.observer.record_event("decision", step=step, action=decision, result=result)

        self._try_rule_mutation()
        self._try_function_mutation()

        try:
            entropy = getattr(self.agent, "entropy", 0.0)
            if entropy >= self.ENTROPY_THRESHOLD or self._detect_stagnation():
                logging.log("EXECUTOR", f"Triggering automatic mutation due to entropy {entropy:.2f} or stagnation.", level="INFO")
                print(f"[MUTATION] Triggered due to entropy={entropy:.2f} or stagnation.")
                self.mutation_trigger.trigger(context, reason="auto_entropy_stagnation")
        except Exception as e:
            logging.log("EXECUTOR", f"Error triggering automatic mutation: {e}", level="ERROR")
            print(f"[ERROR] Triggering mutation failed: {e}")

        self._try_controlled_hypermutation()

        self._symbolic_step += 1
        if self._symbolic_step % self.SYMBOLIC_PERSISTENCE_INTERVAL == 0:
            if hasattr(self.engine, "save_rules"):
                logging.log("EXECUTOR", "Persisting symbolic rules...", level="INFO")
                print("[INFO] Persisting symbolic rules...")
                self.engine.save_rules()

    def _detect_stagnation(self) -> bool:
        recent_rewards = getattr(self.agent, "rewards", [])
        if len(recent_rewards) < 5:
            return False
        if all(r <= 0 for r in recent_rewards[-5:]):
            return True
        return False

    def stop(self) -> None:
        logging.log("EXECUTOR", "Executor stopped.", level="INFO")
        print("[INFO] Executor stopped.")

    # TODO: Define _execute_action_with_logging, _try_rule_mutation, _try_function_mutation,
    # _try_controlled_hypermutation, _ensure_valid_context si aún no están implementados.
