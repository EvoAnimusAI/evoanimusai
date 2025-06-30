# metacognition/autonomous_stop.py

import logging
from typing import Tuple, List, Dict, Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def evaluate_contextual_stop(context: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Determines whether EvoAI should halt the execution cycle based on symbolic context indicators.

    Parameters:
        context (dict): A dictionary containing symbolic AI state metrics. Expected keys include:
            - "recent_rewards": List[float]
            - "rejected_mutations": int
            - "cycles_without_new_rule": int
            - "current_entropy": float

    Returns:
        Tuple[bool, List[str]]: A tuple where the first element indicates whether execution should stop,
        and the second element contains the reasons for stopping, if any.
    """
    reasons: List[str] = []

    # Check recent rewards
    recent_rewards = context.get("recent_rewards", [])
    if isinstance(recent_rewards, list) and len(recent_rewards) >= 5:
        if all(isinstance(r, (int, float)) and r < 0 for r in recent_rewards[-5:]):
            reasons.append("Too many recent negative rewards.")
            logger.info("Contextual stop reason: consecutive negative rewards.")

    # Check excessive rejected mutations
    rejected_mutations = context.get("rejected_mutations")
    if isinstance(rejected_mutations, int) and rejected_mutations > 10:
        reasons.append("Excessive number of rejected mutations.")
        logger.info("Contextual stop reason: rejected mutations = %d", rejected_mutations)

    # Check stagnation in symbolic evolution
    stagnant_cycles = context.get("cycles_without_new_rule")
    if isinstance(stagnant_cycles, int) and stagnant_cycles > 15:
        reasons.append("Symbolic stagnation detected.")
        logger.info("Contextual stop reason: stagnation = %d cycles", stagnant_cycles)

    # Check entropy level
    entropy = context.get("current_entropy")
    if isinstance(entropy, (int, float)) and entropy > 0.95:
        reasons.append("High entropy detected — system behaving chaotically.")
        logger.info("Contextual stop reason: entropy = %.3f", entropy)

    if reasons:
        logger.warning("Execution halt triggered. Reasons: %s", reasons)
        return True, reasons

    return False, []
