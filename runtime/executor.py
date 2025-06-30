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
from utils.logger import log_event
from utils.observer import SymbioticObserver


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

    def run(self, steps: int = 100) -> None:
        try:
            for step in range(1, steps + 1):
                log_event("EXECUTOR", f"Step {step}/{steps} started.", level="DEBUG")

                if self.environment:
                    if not self._run_environment_step(step):
                        log_event("EXECUTOR", "Execution terminated by environment.", level="INFO")
                        break
                else:
                    self._run_symbolic_step(step)

        except KeyboardInterrupt:
            log_event("EXECUTOR", "Execution manually interrupted.", level="WARNING")
            self.stop()
        except StopIteration as si:
            log_event("EXECUTOR", f"Autonomous stop triggered: {si}", level="INFO")
            self.stop()
        except Exception as exc:
            log_event("EXECUTOR", f"Unexpected error: {exc}", level="ERROR")
            log_event("TRACEBACK", traceback.format_exc(), level="ERROR")
            self.stop()

    def execute(self, steps: int = 100) -> None:
        self.run(steps)

    def stop(self) -> None:
        if self.engine and hasattr(self.engine, "save_rules"):
            log_event("EXECUTOR", "Saving symbolic rules...", level="INFO")
            self.engine.save_rules()
        else:
            log_event("EXECUTOR", "Symbolic engine not available or rules not savable.", level="WARNING")

    def _run_environment_step(self, step: int) -> bool:
        observation = self.environment.observe()
        action = self.agent.decide()
        reward, done = self.environment.act(action)
        self.agent.learn(observation, action, reward)

        self.observer.record_event("environment", action=action, reward=reward)

        if self.monitor:
            self.monitor.log(step, observation, action, reward)

        return not done

    def _run_symbolic_step(self, step: int) -> None:
        decision = self.engine.decide(self.context)
        result = self._execute_action_with_logging(decision)

        self.observer.record_event("decision", step=step, action=decision, result=result)

        self._try_rule_mutation()
        self._try_function_mutation()
        self._try_controlled_hypermutation()

        self._symbolic_step += 1
        if self._symbolic_step % self.SYMBOLIC_PERSISTENCE_INTERVAL == 0:
            if hasattr(self.engine, "save_rules"):
                log_event("EXECUTOR", "Persisting symbolic rules...", level="INFO")
                self.engine.save_rules()

    def _try_rule_mutation(self) -> None:
        if random.random() < self.RULE_MUTATION_PROBABILITY and hasattr(self.engine, "mutate_rules"):
            log_event("EXECUTOR", "Triggering rule mutation...", level="DEBUG")
            self.engine.mutate_rules()
            log_event("rule_mutation", status="executed")

    def _try_function_mutation(self) -> None:
        if random.random() < self.FUNCTION_MUTATION_PROBABILITY:
            log_event("EXECUTOR", "Evaluating function mutation...", level="DEBUG")
            evaluate_mutated_function(self.agent)
            log_event("function_mutation", status="evaluated")

    def _try_controlled_hypermutation(self) -> None:
        entropy = getattr(self.agent, "entropy", 0.0)
        if entropy >= self.ENTROPY_THRESHOLD and random.random() < self.HYPERMUTATION_PROBABILITY:
            log_event("EXECUTOR", f"High entropy ({entropy:.2f}) — triggering hypermutation...", level="INFO")
            try:
                mutated = mutate_complete_function(self.agent.decide)
                if callable(mutated):
                    self.agent.decide = mutated
                    log_event("EXECUTOR", "Hypermutation applied to 'decide'.", level="INFO")
                    log_event("hypermutation", status="completed")
            except Exception as e:
                log_event("EXECUTOR", f"Hypermutation error: {e}", level="ERROR")
                log_event("hypermutation", status="error", detail=str(e))
        else:
            log_event("EXECUTOR", f"Entropy ({entropy:.2f}) below threshold. No hypermutation.", level="DEBUG")

    def _execute_action_with_logging(self, decision: str) -> bool:
        context = {
            "recent_rewards": getattr(self.agent, "rewards", [])[-10:],
            "observed_states": getattr(self.agent, "states", [])[-10:],
            "rejected_mutations": getattr(self.agent, "rejected_mutations", 0),
            "cycles_without_new_rule": getattr(self.agent, "cycles_without_new_rule", 0),
            "current_entropy": getattr(self.agent, "entropy", 0.5),
        }

        should_stop, reasons = evaluate_contextual_stop(context)
        if should_stop:
            log_event("EXECUTOR", f"Contextual stop triggered: {reasons}", level="INFO")
            decision = "wait"

        if decision == self._previous_action:
            self._action_repeats += 1
        else:
            self._previous_action = decision
            self._action_repeats = 1
            self._force_explore = False

        if self._action_repeats >= self.ACTION_REPEAT_LIMIT and not self._force_explore:
            log_event("EXECUTOR", f"Repeated action '{decision}' — forcing exploration.", level="INFO")
            self._force_explore = True
            decision = "explore"
            self._action_repeats = 0

        if self._force_explore:
            log_event("EXECUTOR", "Forced exploration mode active.", level="INFO")
            decision = "explore"

        if self.action_registry.is_valid(decision):
            desc = self.action_registry.get_description(decision)
            log_event("EXECUTOR", f"Executing action: {decision} — {desc}", level="INFO")
            self.action_registry.use_action(decision)
        else:
            log_event("EXECUTOR", f"Unknown symbolic action: {decision}", level="WARNING")

        result = self._execute_action(decision)
        reward = 1.0 if result else -1.0

        rule = self.engine.get_rule_by_action(decision)
        if rule and hasattr(self.engine, "update_rule"):
            self.engine.update_rule(rule, reward)
            log_event("EXECUTOR", f"Updated rule: {rule} with reward={reward}", level="DEBUG")
        elif not rule:
            log_event("EXECUTOR", f"No matching rule for action '{decision}'", level="DEBUG")
        else:
            log_event("EXECUTOR", "Engine missing 'update_rule' method.", level="WARNING")

        return result

    def _execute_action(self, decision: str) -> bool:
        actions = {
            "explore": self._explore,
            "wait": self._wait,
            "calm": self._calm,
            "advance": self._advance,
        }
        if decision in actions:
            actions[decision]()
            return True
        log_event("EXECUTOR", f"Action '{decision}' not implemented.", level="WARNING")
        return False

    def _explore(self) -> None:
        log_event("EXECUTOR", "Exploring symbolic space...", level="INFO")

    def _wait(self) -> None:
        log_event("EXECUTOR", "Waiting for symbolic signals...", level="INFO")
        time.sleep(1)

    def _calm(self) -> None:
        log_event("EXECUTOR", "Reducing internal noise...", level="INFO")

    def _advance(self) -> None:
        log_event("EXECUTOR", "Advancing symbiotically...", level="INFO")
        progress = self.context.get("symbiotic_progress", 0)
        self.context["symbiotic_progress"] = progress + 1

        if self.context["symbiotic_progress"] >= 10:
            log_event("EXECUTOR", "Symbiotic threshold reached. Triggering adaptation.", level="INFO")
            self._trigger_adaptation()
            self.context["symbiotic_progress"] = 0

    def _trigger_adaptation(self) -> None:
        try:
            log_event("ENGINE", "Initiating symbolic rule adaptation...", level="INFO")
            success = adapt_rules(self.engine, self.context)
            if success:
                log_event("EXECUTOR", "Adaptation executed successfully.", level="INFO")
                log_event("ENGINE", "Symbolic engine adapted rules successfully.")  # ← LÍNEA CRUCIAL
            else:
                log_event("EXECUTOR", "Adaptation returned no changes. Triggering fallback.", level="WARNING")
                self._fallback_adaptation()
        except Exception as e:
            log_event("EXECUTOR", f"Adaptation failed: {e}", level="ERROR")
            self._fallback_adaptation()

    def _fallback_adaptation(self) -> None:
        try:
            fallback_adapt_rules(self.engine, self.context)
            log_event("EXECUTOR", "Fallback adaptation completed.", level="INFO")
        except Exception as e:
            log_event("EXECUTOR", f"Fallback adaptation failed: {e}", level="ERROR")
