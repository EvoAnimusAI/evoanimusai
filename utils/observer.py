# utils/observer.py

from utils.logger import log_event

class SymbioticObserver:
    def __init__(self):
        self.state = {}
        self.events = []

    def record_event(self, event_type, **kwargs):
        event = {"type": event_type, "details": kwargs}
        self.events.append(event)
        print(f"[🧠 Observer] Event recorded: {event}")

    def observe(self, environment, agent):
        # Symbiotic observation of environment and agent
        environment_state = environment.get_state() if hasattr(environment, "get_state") else {}
        last_action = getattr(agent, "last_action", None)
        memory = getattr(agent, "memory", [])

        self.state = {
            "environment": environment_state,
            "agent": {
                "last_action": last_action,
                "memory": memory
            }
        }

        # Automatic logging
        log_event("observation", observation=self.state)

        return self.state
