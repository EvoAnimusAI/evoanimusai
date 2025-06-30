# daemon/evoai_initializer_executor.py
# -*- coding: utf-8 -*-
"""
Inicializador del ejecutor EvoAI.
Implementación modular, segura y con trazabilidad para la creación
y configuración del componente ejecutor central.
Cumple estándares militares y gubernamentales.
"""

import logging
from typing import Optional
from core.context import EvoContext
from core.agent import EvoAgent
from core.engine import EvoAIEngine
from runtime.executor import Executor as EvoAIExecutor
from runtime.monitor import EvoAIMonitor

logger = logging.getLogger("EvoAI.Initializer.Executor")

def initialize_executor(agent: EvoAgent, engine: EvoAIEngine, context: Optional[EvoContext] = None) -> EvoAIExecutor:
    """
    Inicializa y configura el ejecutor EvoAI principal.

    Args:
        agent (EvoAgent): Agente para asignar al ejecutor.
        engine (EvoAIEngine): Motor asociado.
        context (Optional[EvoContext]): Contexto operativo asociado.

    Returns:
        EvoAIExecutor: Instancia configurada del ejecutor.

    Raises:
        ValueError: Si faltan parámetros esenciales.
        Exception: Para errores durante la inicialización.
    """
    if agent is None:
        logger.error("[Executor Init] Agente no proporcionado.")
        raise ValueError("El agente es obligatorio para inicializar el ejecutor.")
    if engine is None:
        logger.error("[Executor Init] Motor no proporcionado.")
        raise ValueError("El motor es obligatorio para inicializar el ejecutor.")
    if context is None:
        logger.error("[Executor Init] Contexto no proporcionado.")
        raise ValueError("El contexto operativo es obligatorio para inicializar el ejecutor.")

    try:
        logger.info("[Executor Init] Inicializando ejecutor EvoAI...")
        monitor = EvoAIMonitor()
        executor = EvoAIExecutor(agent=agent, engine=engine, monitor=monitor, context=context)
        logger.info("[Executor Init] Ejecutor EvoAI inicializado correctamente.")
        return executor
    except Exception as ex:
        logger.exception(f"[Executor Init] Error durante inicialización del ejecutor: {ex}")
        raise
