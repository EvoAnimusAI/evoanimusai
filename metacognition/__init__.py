"""
Metacognition module for EvoAI.

Provides components for autonomous control and targeted mutation
based on symbolic context and reinforcement learning.
"""

from .autonomous_stop import evaluate_contextual_stop
from .targeted_mutation import TargetedMutation

__all__ = [
    "evaluate_contextual_stop",
    "TargetedMutation",
]
