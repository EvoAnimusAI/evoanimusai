import pytest
from daemon.evoai_initializer_executor import initialize_executor
from core.agent import EvoAgent
from core.engine import EvoAIEngine
from core.context import EvoContext

class DummyAgent(EvoAgent):
    def __init__(self):
        pass  # Mínima implementación para instanciar

class DummyEngine(EvoAIEngine):
    def __init__(self):
        pass  # Mínima implementación para instanciar

class DummyContext(EvoContext):
    def __init__(self):
        self.name = "test_context"

def test_initialize_executor_success():
    agent = DummyAgent()
    engine = DummyEngine()
    context = DummyContext()

    executor = initialize_executor(agent, engine, context)
    assert executor is not None
    assert executor.agent == agent
    assert executor.engine == engine
    assert executor.context == context

def test_initialize_executor_missing_agent():
    engine = DummyEngine()
    context = DummyContext()

    with pytest.raises(ValueError, match="El agente es obligatorio"):
        initialize_executor(None, engine, context)

def test_initialize_executor_missing_engine():
    agent = DummyAgent()
    context = DummyContext()

    with pytest.raises(ValueError, match="El motor es obligatorio"):
        initialize_executor(agent, None, context)

def test_initialize_executor_missing_context():
    agent = DummyAgent()
    engine = DummyEngine()

    with pytest.raises(ValueError, match="El contexto operativo es obligatorio"):
        initialize_executor(agent, engine, None)
