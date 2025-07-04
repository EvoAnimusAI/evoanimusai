# tests/test_agent.py
import pytest
from core.agent import EvoAgent

class DummyContext:
    """Context válido con los métodos requeridos para pruebas."""
    def __init__(self):
        self.facts = []
        self.updated = []

    def assert_fact(self, key, value):
        self.facts.append((key, value))

    def update(self, data):
        self.updated.append(data)


class NoAssertFactContext:
    """Contexto que carece de assert_fact para probar la rama de error."""
    def update(self, data):
        pass


def test_evoagent_full_coverage():
    # Inicialización y registro de identidad
    ctx = DummyContext()
    agent = EvoAgent(context=ctx, name="Tester")
    assert ("agent_name", "Tester") in ctx.facts

    # _sanitize_observation debe filtrar claves/valores inválidos
    raw_obs = {"valid": 1, 123: "bad_key", "bad_value": []}
    sanitized = agent._sanitize_observation(raw_obs)
    assert sanitized == {"valid": 1}

    # perceive integra observaciones y afirma position con valor sanitizado
    obs = {"pos": "1,2", "status": "ok"}  # Ajuste para evitar tuple (no válido)
    agent.perceive(obs)
    assert ("position", "1,2") in ctx.facts
    assert ctx.updated[-1]["status"] == "ok"

    # decide devuelve una action válida
    action = agent.decide({"foo": "bar"})
    assert action in ["explore", "wait", "calm", "advance"]

    # learn actualiza la entropy tras dos recompensas
    agent.learn({}, action, 1.0)
    agent.learn({}, action, 0.0)
    assert agent.entropy >= 0.0

    # assert_fact sin contexto no genera excepción
    agent_no_ctx = EvoAgent(context=None)
    agent_no_ctx.assert_fact("k", "v")
    agent_no_ctx.perceive({"pos": 42})

    # assert_fact con contexto sin método assert_fact
    bad_ctx = NoAssertFactContext()
    agent_bad = EvoAgent(context=bad_ctx)
    agent_bad.assert_fact("k2", "v2")

    # perceive debe rechazar tipos incorrectos
    with pytest.raises(TypeError):
        agent.perceive(["not", "a", "dict"])
