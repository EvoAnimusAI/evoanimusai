"""
symbolic_ai.__init__

Módulo de inteligencia simbólica para EvoAI.
Expone las interfaces principales del sistema de interpretación y aprendizaje simbólico.

Author: Daniel Santiago Ospina Velasquez
"""

import logging

logger = logging.getLogger(__name__)

try:
    from .symbolic_expression import SymbolicExpression
    from .symbolic_interpreter import SymbolicInterpreter
    from .symbolic_learning_engine import SymbolicLearningEngine
    from .symbolic_rule import SymbolicRule
    from .symbolic_rule_engine import symbolic_rule_engine, SymbolicRuleEngine
    from .symbolic_context import SymbolicContext
except ImportError as e:
    logger.error(f"Error importing core symbolic_ai modules: {e}")
    raise

# Import optional or less stable modules with graceful fallback
try:
    from .web_filter import WebFilter
except ImportError as e:
    logger.warning(f"Optional module 'web_filter' could not be imported: {e}")
    WebFilter = None

try:
    from .hypermutation import HypermutationEngine
except ImportError as e:
    logger.warning(f"Optional module 'hypermutation' could not be imported: {e}")
    HypermutationEngine = None

try:
    from .function_evaluator import evaluate_expression
except ImportError as e:
    logger.warning(f"Optional module 'function_evaluator' could not be imported: {e}")
    evaluate_expression = None

__all__ = [
    "SymbolicExpression",
    "SymbolicInterpreter",
    "SymbolicLearningEngine",
    "SymbolicRule",
    "SymbolicRuleEngine",
    "symbolic_rule_engine",
    "SymbolicContext",
    "WebFilter",
    "HypermutationEngine",
    "evaluate_expression",
]
