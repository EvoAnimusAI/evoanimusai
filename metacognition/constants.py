# metacognition/constants.py

"""
Constants module for EvoAI Metacognition.

This module defines immutable configuration parameters and symbolic constants used
across the metacognition subsystem. Designed for clarity, maintainability, and
strict typing compliance to satisfy governmental software standards.
"""

from typing import Final, Tuple

# Mutation intensity thresholds (0.0 - 1.0 scale)
MUTATION_INTENSITY_LIGHT: Final[float] = 0.1
MUTATION_INTENSITY_MODERATE: Final[float] = 0.4
MUTATION_INTENSITY_STRONG: Final[float] = 0.5

# Mutation rejection limits
MAX_REJECTED_MUTATIONS_BEFORE_MODERATE: Final[int] = 5

# Entropy thresholds influencing mutation strategy
ENTROPY_THRESHOLD_MODERATE: Final[float] = 0.7

# Reward thresholds
REWARD_THRESHOLD_STRONG_MUTATION: Final[float] = 0.0  # Below this triggers strong mutation

# Allowed actions for symbolic rules
ALLOWED_ACTIONS: Final[Tuple[str, ...]] = ("explore", "wait", "calm", "advance")

# Mutation adjustment deltas
STRONG_MUTATION_ACTIONS_DELTA: Final[float] = 1.0  # Not numeric, placeholder to show semantics
MODERATE_MUTATION_THRESHOLD_DELTA: Final[float] = 0.2  # ±10% adjustment
LIGHT_MUTATION_WEIGHT_DELTA: Final[float] = 0.05     # ±2.5% adjustment

# Logging configuration constants
LOGGING_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGING_LEVEL: Final[int] = 20  # INFO

# Default context keys (to avoid magic strings across codebase)
CONTEXT_KEY_RECENT_REWARDS: Final[str] = "recent_rewards"
CONTEXT_KEY_CURRENT_ENTROPY: Final[str] = "current_entropy"
CONTEXT_KEY_REJECTED_MUTATIONS: Final[str] = "rejected_mutations"
CONTEXT_KEY_CYCLES_WITHOUT_NEW_RULE: Final[str] = "cycles_without_new_rule"

# Numeric bounds for thresholds and weights
MIN_THRESHOLD_VALUE: Final[float] = 0.0
MIN_WEIGHT_VALUE: Final[float] = 0.0

# Timeouts or iteration limits
MAX_CYCLES_WITHOUT_IMPROVEMENT: Final[int] = 1000

# Exit reasons constants for AutonomousStop (example)
EXIT_REASON_ENTROPY_LOW: Final[str] = "entropy_below_threshold"
EXIT_REASON_NO_NEW_RULES: Final[str] = "no_new_rules_for_cycles"
EXIT_REASON_NEGATIVE_REWARDS: Final[str] = "negative_rewards_persistent"
