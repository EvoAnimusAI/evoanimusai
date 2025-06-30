"""
Controller for metacognition operations: autonomous stopping and targeted mutation.

This component coordinates evaluation of stop conditions and
application of targeted mutations based on system context.
"""

from typing import Dict, Tuple, List
from .autonomous_stop import evaluate_contextual_stop
from .targeted_mutation import TargetedMutation


class MetacognitionController:
    """
    Orchestrates autonomous stop evaluation and targeted mutation execution.
    """

    def __init__(self, mutation_engine: TargetedMutation = None):
        self.mutation_engine = mutation_engine or TargetedMutation()

    def should_stop(self, context: Dict) -> Tuple[bool, List[str]]:
        """
        Evaluate if EvoAI should stop based on symbolic context.

        Args:
            context (Dict): Current symbolic context with metrics.

        Returns:
            Tuple[bool, List[str]]: (stop_flag, reasons)
        """
        try:
            stop_flag, reasons = evaluate_contextual_stop(context)
            return stop_flag, reasons
        except Exception as e:
            # Log or handle exception if a logging framework is present
            return False, [f"Error during stop evaluation: {e}"]

    def perform_mutation(self, context: Dict) -> bool:
        """
        Perform a targeted mutation based on current context.

        Args:
            context (Dict): Current symbolic context with metrics.

        Returns:
            bool: True if mutation was successful, False otherwise.
        """
        try:
            return self.mutation_engine.mutate(context)
        except Exception as e:
            # Log or handle exception if a logging framework is present
            return False
