# symbolic_ai/rule_adaptation.py

import random
from utils.logging import log_event

def adapt_rules(engine, context: dict) -> bool:
    """
    Attempt to adapt symbolic rules via mutation if conditions allow.
    
    Args:
        engine: The symbolic engine object that may implement mutate_rules().
        context: Dictionary holding adaptation context, including 'mutation_chance'.

    Returns:
        bool: True if mutation was performed, False otherwise.
    """
    log_event("ENGINE", "Initiating symbolic rule adaptation...", level="INFO")

    mutation_chance = context.get("mutation_chance", 0.1)
    if random.random() < mutation_chance:
        if hasattr(engine, "mutate_rules") and callable(engine.mutate_rules):
            try:
                engine.mutate_rules()
                log_event("ENGINE", "Mutation performed during adaptation.", level="INFO")
                return True
            except Exception as e:
                log_event("ENGINE", f"Mutation failed: {e}", level="ERROR")
                return False
        else:
            log_event("ENGINE", "No valid mutate_rules() method found.", level="WARNING")
    else:
        log_event("ENGINE", f"No mutation: chance {mutation_chance:.2f} not met.", level="DEBUG")

    return False


def fallback_adapt_rules(engine, context: dict) -> None:
    """
    Fallback strategy when no primary adaptation occurs.
    
    Args:
        engine: The symbolic engine object (may or may not be used).
        context: Dictionary tracking fallback metrics.
    """
    log_event("ENGINE", "Executing fallback adaptation...", level="INFO")
    context["fallback_adapt_counter"] = context.get("fallback_adapt_counter", 0) + 1
