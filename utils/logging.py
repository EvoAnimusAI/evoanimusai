import logging
from typing import Any, Union

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S%z'
)

logger = logging.getLogger("evoai.utils.logging")

def log_event(event_name: str, details: Any = None, level: Union[int, str] = logging.INFO) -> None:
    """
    Registra un evento estructurado con nombre y detalles opcionales.

    Args:
        event_name (str): Nombre identificativo del evento.
        details (Any, opcional): Información adicional relevante para auditoría.
        level (int | str, opcional): Nivel de severidad del evento. Puede ser int (logging.INFO) o str ("INFO").

    Uso:
        log_event("user_login", {"user_id": 123}, level="WARNING")
        log_event("update_ok", {}, level=logging.DEBUG)
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    if details is None:
        details = {}

    message = f"Evento: {event_name} | Detalles: {details}"
    logger.log(level, message)
