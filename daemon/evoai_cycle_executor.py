# daemon/evoai_cycle_executor.py
# -*- coding: utf-8 -*-
"""
Ejecución principal del ciclo de vida EvoAI
Nivel: Militar / Gubernamental / Ultra-secreto
"""

import time
import json
import logging
import signal
import traceback
from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime

from core.context import EvoContext
from core.agent import EvoAgent
from core.environment import Environment
from core.engine import EvoAIEngine
from core.self_diagnostics import run_integrity_diagnostics
from core.symbolic_decision_engine import SymbolicDecisionEngine
from core.input_sanitizer import InputSanitizer
from core.heuristic_optimizer import HeuristicOptimizer
from metacognition.supervisor_metacognitivo import SupervisorMetacognitivo
from core.halt_monitor import HaltMonitor
from tools.halt_visualizer import HaltVisualizer

supervisor_metacognitivo = SupervisorMetacognitivo()
heuristic_optimizer = HeuristicOptimizer()
halt_monitor = HaltMonitor()
halt_visualizer = HaltVisualizer()

logger = logging.getLogger("EvoAIExecutor")
logging.basicConfig(level=logging.INFO)

FALLO_LOG_PATH = Path("logs/cycle_failures.json")
terminate_flag = False

try:
    from daemon.evoai_daemon import components
except ImportError:
    components = {}

def signal_handler(signum, frame):
    global terminate_flag
    logger.info(f"[🔝] Señal {signum} recibida. Terminando ciclo...")
    terminate_flag = True

def setup_signal_handlers():
    logger.info("⚙️ Configurando manejadores de señal para apagado...")
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)

def initialize_context() -> EvoContext:
    logger.info("[INIT] Inicializando núcleo EvoAI...")
    agent = EvoAgent(name="EvoAI")
    environment = Environment()
    engine = EvoAIEngine()
    context = EvoContext(agent=agent, engine=engine, environment=environment)
    if hasattr(context, "assert_fact"):
        context.assert_fact("agent_identity", agent.name)
    return context

def registrar_fallo_critico(cycle_num: int, error: Exception):
    now = datetime.utcnow().isoformat() + "Z"
    entry = {
        "timestamp": now,
        "ciclo": cycle_num,
        "error": str(error),
        "traceback": traceback.format_exc()
    }
    try:
        if FALLO_LOG_PATH.exists():
            with open(FALLO_LOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        data.append(entry)
        with open(FALLO_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[📛 LOG] Fallo crítico registrado en {FALLO_LOG_PATH}")
    except Exception as log_err:
        print(f"[❌ ERROR LOGGING] No se pudo registrar el fallo: {log_err}")

def run_cycle(context: EvoContext, cycle_num: int, sanitizer: InputSanitizer) -> Dict[str, Any]:
    logger.info(f"🤖 Iniciando ciclo #{cycle_num}")
    try:
        agent_action, symbolic_decision = context.decide()
        decision = symbolic_decision or agent_action or {"action": "wait"}

        if decision.get("action") == "explore" and cycle_num % 5 == 0:
            logger.warning(f"[DUPLICATION WARNING] Acción 'explore' repetida en ciclo #{cycle_num}")

        if isinstance(decision, dict) and "priority" in decision:
            decision["priority"] = round(decision["priority"] * 1.092, 4)
            logger.info(f"[Mutate] Acción '{decision['action']}' ➔ prioridad: {decision['priority']}")
        else:
            logger.info(f"[Action] Acción decidida: {decision}")

        if hasattr(context, "assert_fact"):
            context.assert_fact("last_action", decision)

        raw_observation = context.environment.observe()
        clean_observation = sanitizer.sanitize(raw_observation)
        context.update(clean_observation)

        return context.as_dict()

    except Exception as e:
        logger.error(f"[CRITICAL] Fallo en el ciclo #{cycle_num}: {e}", exc_info=True)
        registrar_fallo_critico(cycle_num, e)
        return {"error": str(e), "cycle": cycle_num}

def run_cycle_loop(test_mode: bool = False, components: Optional[Dict] = None):
    setup_signal_handlers()
    context = initialize_context()
    context.symbolic_engine = SymbolicDecisionEngine(context)
    sanitizer = InputSanitizer()

    logger.info("[INIT] Sistema simbólico inicializado.")
    if not run_integrity_diagnostics(context):
        logger.error("💨 Fallo en diagnóstico. Abortando ciclo.")
        return

    if components is None:
        logger.warning("[⚠️ COMPONENTES] 'components' no definido. Inicializando vacío.")
        components = {}

    cycle_num = 0
    while not terminate_flag:
        contexto_actual = run_cycle(context, cycle_num, sanitizer)

        resultado_heuristico = heuristic_optimizer.evaluar_condiciones_globales(contexto_actual)
        if resultado_heuristico.get("alerta"):
            print(f"[⚠️ OPTIMIZADOR ALERTA] Condición heurística crítica detectada.")
            print(f"[🔎 DETALLES] {resultado_heuristico['detalles']}")
            correccion = heuristic_optimizer.corregir_estado(contexto_actual)
            print(f"[⚙️ CORRECCIÓN] Acciones correctivas aplicadas: {correccion['correcciones']}")

        halt_monitor.registrar_ciclo(contexto_actual)
        if halt_monitor.detectar_halt_critico():
            print(f"[🛑 HALT DETECTADO] Condiciones acumulativas críticas detectadas.")
            contexto_actual["halt_detectado"] = True

        try:
            evolucionador = components.get("evolucionador_simbolico", None)
            if evolucionador:
                print(f"[🧬 CYCLE-{cycle_num}] Ejecutando evolución simbólica...")
                evolucionador.evolucionar(contexto_actual)
        except Exception as e:
            logger.warning(f"[⚠️ EVOLUCIÓN ERROR] Falla: {e}")
            registrar_fallo_critico(cycle_num, e)

        try:
            conciencia = components.get("conciencia_simulada", None)
            if conciencia:
                resultado_conciencia = conciencia.ciclo(contexto_actual)
                print(f"[🧠 CYCLE-{cycle_num}] Resultado conciencia: {resultado_conciencia}")
                if resultado_conciencia.get("accion") == "reiniciar_loop_aprendizaje":
                    print("[🧠] Solicitud de reinicio de ciclo de aprendizaje detectada.")
        except Exception as e:
            logger.warning(f"[⚠️ CONCIENCIA ERROR] Falla: {e}")
            registrar_fallo_critico(cycle_num, e)

        resultado_supervision = supervisor_metacognitivo.evaluar(contexto_actual)
        if resultado_supervision.get("status") == "recovered":
            print("[🛠️ RECOVERY] Supervisor ejecutó recuperación simbólica correctamente.")

        cycle_num += 1
        time.sleep(0.1 if test_mode else 0.2)

    logger.info("[🔝] Ciclo terminado manualmente.")
    try:
        if hasattr(halt_monitor, "obtener_historial_ciclos"):
            halt_visualizer.exportar_json(halt_monitor.obtener_historial_ciclos())
        else:
            logger.warning("[⚠️ EXPORT] HaltMonitor no implementa 'obtener_historial_ciclos'.")
    except Exception as e:
        logger.error(f"[❌ EXPORT] Fallo al exportar historial HALT: {e}", exc_info=True)

if __name__ == "__main__":
    run_cycle_loop(components=components)
