# symbolic_ai/rule_adaptation.py

import random
from utils import evo_logging as logging

def adapt_rules(engine, context: dict) -> bool:
    """
    Attempt to adapt symbolic rules via mutation if conditions allow.

    Args:
        engine: The symbolic engine object that may implement mutate_rules().
        context: Dictionary holding adaptation context, including 'mutation_chance'.

    Returns:
        bool: True if mutation was performed, False otherwise.
    """
    print("[ADAPT] Starting symbolic rule adaptation...")
    logging.log("ENGINE", "Initiating symbolic rule adaptation...", level="INFO")

    mutation_chance = context.get("mutation_chance", 0.1)
    if random.random() < mutation_chance:
        if hasattr(engine, "mutate_rules") and callable(engine.mutate_rules):
            try:
                engine.mutate_rules()
                print("[ADAPT] Mutation executed.")
                logging.log("ENGINE", "Mutation performed during adaptation.", level="INFO")
                return True
            except Exception as e:
                print(f"[ADAPT][ERROR] Mutation failed: {e}")
                logging.log("ENGINE", f"Mutation failed: {e}", level="ERROR")
                return False
        else:
            print("[ADAPT][WARNING] mutate_rules() not available.")
            logging.log("ENGINE", "No valid mutate_rules() method found.", level="WARNING")
    else:
        print(f"[ADAPT] Mutation skipped (chance: {mutation_chance:.2f})")
        logging.log("ENGINE", f"No mutation: chance {mutation_chance:.2f} not met.", level="DEBUG")

    return False


def fallback_adapt_rules(engine, context: dict) -> None:
    """
    Fallback strategy when no primary adaptation occurs.

    Args:
        engine: The symbolic engine object (may or may not be used).
        context: Dictionary tracking fallback metrics.
    """
    print("[ADAPT][FALLBACK] Executing fallback adaptation.")
    logging.log("ENGINE", "Executing fallback adaptation...", level="INFO")
    context["fallback_adapt_counter"] = context.get("fallback_adapt_counter", 0) + 1
