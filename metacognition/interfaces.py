# metacognition/interfaces.py

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple


class StoppingStrategy(ABC):
    """
    Interface for contextual stopping strategies in symbolic AI agents.
    """

    @abstractmethod
    def should_stop(self, context: Dict[str, Any]) -> Tuple[bool, list]:
        """
        Evaluate whether the system should stop based on the given context.
        Returns:
            - stop (bool): whether execution should halt.
            - reasons (list of str): explanation of the stop condition(s).
        """
        pass


class MutationStrategy(ABC):
    """
    Interface for targeted symbolic mutation strategies.
    """

    @abstractmethod
    def mutate(self, context: Dict[str, Any]) -> bool:
        """
        Apply a mutation based on the current symbolic context.
        Returns:
            - success (bool): whether the mutation was successfully applied.
        """
        pass
