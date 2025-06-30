# daemon/evoai_initializer_core.py
import logging
from core.context import EvoContext
from daemon.evoai_initializer_security import load_secure_key
from daemon.evoai_initializer_agent import initialize_agent
from daemon.evoai_initializer_engine import initialize_engine
from daemon.evoai_initializer_executor import initialize_executor
from daemon.evoai_initializer_tools import initialize_support_tools

logger = logging.getLogger("EvoAI.Core")

def initialize_core_components():
    logger.info("[INIT] Inicializando núcleo EvoAI...")

    # Seguridad
    daemon_key = load_secure_key()

    # Componentes base
    context = EvoContext()
    agent = initialize_agent(context=context)
    engine = initialize_engine(agent, context)
    executor = initialize_executor(agent, engine, context)
    tools = initialize_support_tools(engine, context, daemon_key)

    logger.info("[INIT] Núcleo EvoAI completamente inicializado y seguro.")

    return {
        "context": context,
        "agent": agent,
        "engine": engine,
        "executor": executor,
        **tools,
    }
