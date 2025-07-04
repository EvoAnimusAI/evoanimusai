# utils/observer.py
# Observador simbiótico con trazabilidad visible en consola

from utils import evo_logging as logging
import datetime


class SymbioticObserver:
    def __init__(self):
        self.state = {}
        self.events = []

    def record_event(self, event_type, **kwargs):
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        event = {"timestamp": timestamp, "type": event_type, "details": kwargs}
        self.events.append(event)

        logging.log("OBSERVER", f"[{event_type.upper()}] {kwargs}", level="INFO")
        print(f"[🧠 Observer] [{timestamp}] Event recorded: {event_type.upper()} -> {kwargs}")

    def observe(self, environment, agent):
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

        logging.log("OBSERVER", "Environment and agent observed.", level="INFO")
        print(f"[🧠 Observer] Observation recorded → last_action={last_action}, memory_len={len(memory)}")
        return self.state
