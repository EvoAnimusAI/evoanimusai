# symbolic_ai/redundancy_guard.py
# Clasificación: Militar / Gubernamental / Ultra-secreto
# Propósito: Detección avanzada de redundancia simbólica
# Norma aplicada: EVO-SEC/LOOP-CTRL-2201
# Unidad responsable: Centro de Control de Redundancia Cognitiva (CCRC)

from collections import deque
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class RedundancyGuard:
    """
    Sistema de vigilancia simbólica diseñado para detectar patrones redundantes
    y activar respuestas anticipadas ante comportamientos repetitivos no productivos.
    """

    def __init__(self, window_size: int = 5, threshold: int = 4, intervention_enabled: bool = True):
        """
        Inicializa el guardián de redundancia con parámetros estrictos.

        Args:
            window_size (int): Número de acciones a observar.
            threshold (int): Número mínimo de repeticiones para activar alerta.
            intervention_enabled (bool): Habilita sugerencias de contramedidas.
        """
        self.history: deque[str] = deque(maxlen=window_size)
        self.threshold = threshold
        self.intervention_enabled = intervention_enabled

    def record(self, action: str) -> bool:
        """
        Registra una action simbólica y evalúa su redundancia.

        Args:
            action (str): Acción simbólica ejecutada.

        Returns:
            bool: Verdadero si se detecta patrón redundante.
        """
        self.history.append(action)
        repeated_count = sum(1 for a in self.history if a == action)

        if repeated_count >= self.threshold:
            logger.warning(f"[RedundancyGuard] 🚨 Redundancia detectada: '{action}' repetido {repeated_count} veces.")
            if self.intervention_enabled:
                self._suggest_intervention(action)
            return True

        logger.debug(f"[RedundancyGuard] Acción registrada: '{action}'. Historial: {list(self.history)}")
        return False

    def _suggest_intervention(self, action: str) -> None:
        """
        Sugiere contramedidas ante redundancia simbólica.

        Args:
            action (str): Acción redundante detectada.
        """
        logger.critical(
            f"[RedundancyGuard] Intervención sugerida por repetición de '{action}': "
            "⚠️ Considerar: mutate aleatorio, penalización, cambio forzado de state, "
            "reconfiguración parcial o reseteo simbólico."
        )

    def get_history(self) -> List[str]:
        """
        Expone historial reciente de acciones.

        Returns:
            List[str]: Lista de acciones registradas.
        """
        return list(self.history)

    def reset(self) -> None:
        """
        Limpia el historial de decisiones, útil tras intervención.
        """
        logger.info("[RedundancyGuard] Historial de redundancia reiniciado.")
        self.history.clear()
