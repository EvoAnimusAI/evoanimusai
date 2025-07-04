# symbolic_ai/loop_termination_controller.py
# Clasificación: Militar / Gubernamental / Ultra-secreto
# Propósito: Control de terminación de bucles simbólicos repetitivos
# Norma: EVO-LOOP/CTRL-MIL-9941
# Unidad Responsable: Unidad de Supervisión de Ciclos Cognitivos (USCC)

import logging

logger = logging.getLogger(__name__)

class LoopTerminationController:
    """
    Supervisor de bucles simbólicos redundantes.
    Monitorea repeticiones persistentes de acciones y activa medidas de intervención
    cuando se alcanza un umbral crítico de repetición.
    """

    def __init__(self, max_repeats: int = 3):
        """
        Inicializa el controlador con un umbral estricto.

        Args:
            max_repeats (int): Número máximo de repeticiones permitidas antes de intervención.
        """
        self.last_action: str | None = None
        self.repeat_count: int = 0
        self.max_repeats: int = max_repeats

    def update(self, action: str) -> bool:
        """
        Evalúa la action actual y decide si debe forzarse una intervención.

        Args:
            action (str): Acción simbólica ejecutada en el ciclo actual.

        Returns:
            bool: True si se alcanza el límite y debe intervenirse.
        """
        if not isinstance(action, str):
            logger.error(f"[LoopController] Acción inválida recibida: {repr(action)}")
            return False

        if action == self.last_action:
            self.repeat_count += 1
            logger.debug(f"[LoopController] Acción repetida '{action}' ({self.repeat_count}/{self.max_repeats})")
        else:
            self.repeat_count = 1
            logger.debug(f"[LoopController] Nueva action detectada: '{action}'")
        
        self.last_action = action

        if self.repeat_count >= self.max_repeats:
            logger.critical(
                f"[LoopController] 🚨 Umbral de repetición excedido: '{action}' "
                f"({self.repeat_count} veces consecutivas). Activar contención simbólica."
            )
            return True

        return False

    def reset(self) -> None:
        """
        Restaura el state del controlador, útil tras una intervención.
        """
        logger.info("[LoopController] Estado de repetición reiniciado.")
        self.last_action = None
        self.repeat_count = 0
