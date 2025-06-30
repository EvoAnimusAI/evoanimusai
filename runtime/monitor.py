import time
import os
import datetime

LOG_FILE_PATH = os.path.join("logs", "system_events.log")

class ExecutionMonitor:
    """
    Monitorea eventos generales del sistema.
    """
    def __init__(self):
        self.events = []
        self.start_time = time.time()

    def record_event(self, event_type, description, metadata=None):
        timestamp = time.time()
        self.events.append({
            "timestamp": timestamp,
            "type": event_type,
            "description": description,
            "metadata": metadata or {}
        })

    def get_summary(self):
        total_events = len(self.events)
        duration = time.time() - self.start_time
        return {
            "total_events": total_events,
            "duration": duration,
            "events": self.events[-10:]  # Últimos 10 eventos
        }

    def clear(self):
        self.events = []
        self.start_time = time.time()


class EvoAIMonitor:
    """
    Monitorea y registra el desempeño de EvoAI en cada ciclo.
    """
    def __init__(self):
        self.logs = []

    def log(self, step, observation, action, reward):
        """
        Registra los datos de una iteración del ciclo.

        Args:
            step (int): número de iteración.
            observation (any): estado observado del entorno.
            action (any): acción tomada por el agente.
            reward (float): recompensa obtenida.
        """
        entry = {
            "step": step,
            "observation": observation,
            "action": action,
            "reward": reward
        }
        self.logs.append(entry)

    def summary(self):
        """
        Retorna un resumen básico del monitoreo.
        """
        total_reward = sum(log["reward"] for log in self.logs)
        return {
            "total_steps": len(self.logs),
            "total_reward": total_reward
        }


def log_event(event_type, message, level="INFO"):
    """
    Registra un evento de sistema en archivo y consola.

    Args:
        event_type (str): Tipo del evento (por ejemplo, 'STRATEGY', 'ERROR').
        message (str): Mensaje descriptivo del evento.
        level (str): Nivel de severidad ('INFO', 'WARNING', 'ERROR').
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] [{event_type}] {message}"

    # Imprimir en consola
    print(log_entry)

    # Escribir en archivo
    try:
        os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
        with open(LOG_FILE_PATH, "a") as log_file:
            log_file.write(log_entry + "\n")
    except Exception as e:
        print(f"[ERROR] No se pudo escribir en log: {e}")
