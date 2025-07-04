import pytest
from utils.observer import SymbioticObserver

class MockEnvironment:
    def get_state(self):
        return {"weather": "sunny", "temperature": 23}

class MockAgent:
    last_action = "move_forward"
    memory = [{"state": "initial"}, {"state": "moved"}]

def test_record_event(capsys):
    observer = SymbioticObserver()
    observer.record_event("test_event", detail="value", level=1)
    captured = capsys.readouterr()
    assert "[🧠 Observer] Event recorded" in captured.out
    assert observer.events[0]["type"] == "test_event"
    assert observer.events[0]["details"]["detail"] == "value"

def test_observe_sets_state_and_logs(caplog):
    env = MockEnvironment()
    agent = MockAgent()
    observer = SymbioticObserver()

    with caplog.at_level("INFO"):
        state = observer.observe(env, agent)

    # Verifica state estructurado
    assert "environment" in state
    assert "agent" in state
    assert state["agent"]["last_action"] == "move_forward"
    assert isinstance(state["agent"]["memory"], list)

    # Verifica que el log contiene la observación
    assert any("Evento: observation" in m for m in caplog.text.splitlines())
