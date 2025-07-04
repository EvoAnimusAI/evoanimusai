import pytest
from core.context import EvoContext
from symbolic_ai.symbolic_context import SymbolicContext

def test_evo_context_inherits_symbolic_context():
    """
    Verifica que EvoContext herede de SymbolicContext.
    Esta relación es clave para la integridad del motor simbólico de EvoAI.
    """
    assert issubclass(EvoContext, SymbolicContext), (
        "EvoContext debe heredar de SymbolicContext para asegurar compatibilidad "
        "con el sistema de inferencia simbólica."
    )
