# symbolic_ai/function_evaluator.py

import logging
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

def evaluate_mutated_function(
    function: Callable[..., Any],
    context: Optional[dict] = None
) -> Any:
    """
    Evaluates a mutated function within an optional context.

    Args:
        function (Callable): The mutated function to evaluate.
        context (Optional[dict]): Optional context to pass to the function.

    Returns:
        Any: The result of the function evaluation, or None if an error occurred.

    Logs detailed info for auditability and debugging.
    """
    logger.info(f"Evaluating mutated function: {function}")

    try:
        if context is not None:
            result = function(context)
        else:
            result = function()
        logger.info(f"Evaluation successful. Result: {result}")
        return result

    except Exception as e:
        logger.error(f"Error while evaluating function: {e}", exc_info=True)
        return None
