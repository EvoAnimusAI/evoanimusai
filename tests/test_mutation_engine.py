# tests/test_mutation_engine.py

import pytest
from mutations.mutation_engine import mutate_function, MutatedFunction


class DummySymbolic:
    def get_recent_concepts(self):
        return [{"concept": "velocity"}, {"concept": "mass"}]


class DummyContext:
    symbolic = DummySymbolic()


def test_mutate_function_success():
    agent_knowledge = {"energy": 100}
    context = DummyContext()

    mutated = mutate_function(agent_knowledge, context)

    assert isinstance(mutated, MutatedFunction)
    assert callable(mutated.callable)
    assert "def" in mutated.code
    assert "mutation_strategy" in mutated.metadata
    assert mutated(5) == 10


def test_mutate_function_no_concepts():
    agent_knowledge = {}

    class EmptySymbolic:
        def get_recent_concepts(self):
            return []

    class Context:
        symbolic = EmptySymbolic()

    with pytest.raises(ValueError, match="No se encontraron conceptos simbólicos recientes"):
        mutate_function(agent_knowledge, Context())


def test_mutate_function_malformed_concepts():
    agent_knowledge = {}

    class MalformedSymbolic:
        def get_recent_concepts(self):
            raise Exception("Simulated error")

    class Context:
        symbolic = MalformedSymbolic()

    with pytest.raises(ValueError, match="Error obteniendo conceptos simbólicos"):
        mutate_function(agent_knowledge, Context())
