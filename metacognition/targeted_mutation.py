# metacognition/targeted_mutation.py

import logging
import random
from typing import Optional, Dict, Any
from metacognition.interfaces import MutationStrategy
from symbolic_ai import symbolic_rule_engine

logger = logging.getLogger(__name__)


class TargetedMutation(MutationStrategy):
    """
    Applies context-aware symbolic mutations based on system feedback and symbolic state.
    """

    def __init__(self, rule_engine=None):
        self.rule_engine = rule_engine or symbolic_rule_engine
        self.mutation_history = []

    def analyze_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the symbolic context and determine mutation strategy.

        Args:
            context: Contains system metrics like recent rewards, entropy, and rejection counts.

        Returns:
            A dictionary with mutation intensity and type.
        """
        recent_rewards = context.get("recent_rewards", [0])
        average_reward = sum(recent_rewards) / max(len(recent_rewards), 1)
        entropy = context.get("current_entropy", 0.5)
        rejected_mutations = context.get("rejected_mutations", 0)

        intensity = 0.1
        mutation_type = "light"

        if average_reward < 0:
            intensity = 0.5
            mutation_type = "strong"
        elif rejected_mutations > 5:
            intensity = 0.3
            mutation_type = "moderate"
        elif entropy > 0.7:
            intensity = 0.4
            mutation_type = "moderate"

        return {"intensity": intensity, "type": mutation_type}

    def select_rule_to_mutate(self) -> Optional[Any]:
        """
        Select a symbolic rule to mutate, prioritizing the lowest-performing one.

        Returns:
            The rule object with the lowest reward, or None if no rules exist.
        """
        rules = self.rule_engine.get_all()
        if not rules:
            return None

        rules_sorted = sorted(rules, key=lambda r: getattr(r, "reward", 0))
        return rules_sorted[0]

    def mutate(self, context: Dict[str, Any]) -> bool:
        """
        Perform a symbolic mutation based on the system context.

        Args:
            context: Current symbolic system metrics.

        Returns:
            True if mutation was applied, False otherwise.
        """
        parameters = self.analyze_context(context)
        intensity = parameters["intensity"]
        mutation_type = parameters["type"]

        rule = self.select_rule_to_mutate()
        if rule is None:
            logger.warning("[TargetedMutation] No symbolic rules available for mutation.")
            return False

        logger.info(f"[TargetedMutation] Applying '{mutation_type}' mutation (intensity={intensity:.2f}) to rule '{getattr(rule, 'action', 'unknown')}'")

        if mutation_type == "strong":
            success = self._strong_mutation(rule)
        elif mutation_type == "moderate":
            success = self._moderate_mutation(rule)
        else:
            success = self._light_mutation(rule)

        if success:
            self.mutation_history.append((getattr(rule, "action", None), mutation_type))
            logger.info(f"[TargetedMutation] Mutation applied successfully.")
        else:
            logger.error(f"[TargetedMutation] Mutation failed.")

        return success

    def _strong_mutation(self, rule: Any) -> bool:
        """
        Perform a strong mutation by replacing the action.

        Args:
            rule: Symbolic rule object.

        Returns:
            True if mutation successful.
        """
        possible_actions = ["explore", "wait", "calm", "advance"]
        current_action = getattr(rule, "action", None)
        new_action = random.choice([a for a in possible_actions if a != current_action])

        if new_action:
            setattr(rule, "action", new_action)
            return True
        return False

    def _moderate_mutation(self, rule: Any) -> bool:
        """
        Apply moderate mutation to numerical thresholds.

        Args:
            rule: Symbolic rule object.

        Returns:
            True if mutation applied.
        """
        if hasattr(rule, "threshold"):
            delta = (random.random() - 0.5) * 0.2  # ±10%
            rule.threshold = max(0, rule.threshold + delta)
            return True
        return False

    def _light_mutation(self, rule: Any) -> bool:
        """
        Apply light mutation by tweaking weight slightly.

        Args:
            rule: Symbolic rule object.

        Returns:
            True if mutation applied.
        """
        if hasattr(rule, "weight"):
            delta = (random.random() - 0.5) * 0.05  # ±2.5%
            rule.weight = max(0, rule.weight + delta)
            return True
        return False
