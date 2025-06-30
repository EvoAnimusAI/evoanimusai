# daemon/evoai_initializer_agent.py
# -*- coding: utf-8 -*-
"""
Inicializador del agente EvoAI.
Definición modular, segura y auditada para creación y configuración del agente central.
Cumple con estándares militares y gubernamentales de seguridad, trazabilidad y robustez.
"""

import logging
from typing import Optional
from core.agent import EvoAgent
from core.context import EvoContext

logger = logging.getLogger("EvoAI.Initializer.Agent")


def initialize_agent(name: str = "EvoAI", context: Optional[EvoContext] = None) -> EvoAgent:
    """
    Inicializa y configura el agente EvoAI principal.

    Args:
        name (str): Nombre identificador del agente.
        context (Optional[EvoContext]): Contexto operativo en el cual se inserta el agente.

    Returns:
        EvoAgent: Instancia configurada del agente EvoAI.

    Raises:
        ValueError: Si no se provee contexto válido.
        Exception: Para cualquier error en la inicialización.
    """
    if context is None:
        logger.error("[Agent Init] Contexto no proporcionado para inicialización del agente.")
        raise ValueError("El contexto operativo es obligatorio para inicializar el agente.")

    try:
        logger.info(f"[Agent Init] Inicializando agente con nombre '{name}'...")
        agent = EvoAgent(name=name, context=context)

        # Configuraciones adicionales del agente pueden incluirse aquí
        # Ejemplo: configuración de capacidades, validaciones, inicializaciones internas

        logger.info(f"[Agent Init] Agente '{name}' inicializado correctamente.")
        return agent

    except Exception as ex:
        logger.exception(f"[Agent Init] Error durante inicialización del agente: {ex}")
        raise
