# behavior/action_registry.py

from typing import List, Dict, Optional


class ActionRegistry:
    """
    ActionRegistry gestiona un conjunto de acciones semánticas
    que pueden ser invocadas por un agente autónomo en un entorno.
    """

    def __init__(self):
        self._actions: Dict[str, Dict[str, object]] = {
            'explore': self._make_action(
                description="Explore the environment",
                priority=0.9,
                alias=['investigate', 'examine']
            ),
            'wait': self._make_action(
                description="Pause and collect data",
                priority=0.4,
                alias=['pause', 'stop']
            ),
            'calm': self._make_action(
                description="Reduce noise or entropy",
                priority=0.6,
                alias=['relax', 'soothe']
            ),
            'advance': self._make_action(
                description="Move forward deliberately",
                priority=0.7,
                alias=['progress', 'proceed']
            ),
            'move_forward': self._make_action(
                description="Move forward in the environment",
                priority=0.8,
                alias=['go_ahead', 'step_forward']
            ),
        }
        self._protected = set(self._actions.keys())

    def _make_action(self, description: str, priority: float, alias: List[str]) -> Dict[str, object]:
        return {
            'desc': description,
            'priority': priority,
            'alias': alias,
            'usage_count': 0
        }

    def is_valid(self, action: str) -> bool:
        """Retorna True si la acción existe directa o como alias."""
        return any(
            action == name or action in data['alias']
            for name, data in self._actions.items()
        )

    def get_description(self, action: str) -> str:
        """Devuelve la descripción de una acción o 'Unknown action'."""
        for name, data in self._actions.items():
            if action == name or action in data['alias']:
                return data['desc']
        return "Unknown action"

    def all_actions(self) -> List[str]:
        """Lista de todas las acciones registradas."""
        return list(self._actions.keys())

    def register(self, name: str, description: str, priority: float = 0.5, alias: Optional[List[str]] = None) -> None:
        """
        Registra una nueva acción. Las acciones protegidas no se pueden sobrescribir.
        """
        if not name.isidentifier():
            raise ValueError(f"Invalid action name: '{name}'")

        if name in self._protected:
            raise ValueError(f"Action '{name}' is protected and cannot be overwritten.")

        if name in self._actions:
            raise ValueError(f"Action '{name}' already exists.")

        self._actions[name] = self._make_action(description, priority, alias or [])

    def use_action(self, action: str) -> bool:
        """Incrementa el contador de uso de una acción válida."""
        for name, data in self._actions.items():
            if action == name or action in data['alias']:
                data['usage_count'] += 1
                return True
        return False

    def export_actions(self) -> Dict[str, Dict[str, object]]:
        """Exporta el diccionario completo de acciones."""
        return self._actions.copy()
