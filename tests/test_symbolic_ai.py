# test_symbolic_ai.py

def test_symbolic_ai_module_import():
    try:
        from symbolic_ai import (
            SymbolicExpression,
            SymbolicInterpreter,
            SymbolicLearningEngine,
            SymbolicRule,
            SymbolicRuleEngine,
            symbolic_rule_engine,
            SymbolicContext,
            WebFilter,
            HypermutationEngine,
            evaluate_expression,
        )
    except Exception as e:
        assert False, f"Fallo al importar el módulo symbolic_ai: {e}"
