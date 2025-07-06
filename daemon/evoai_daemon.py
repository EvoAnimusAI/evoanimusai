# -*- coding: utf-8 -*-
"""
EvoAI Daemon Principal — Nivel gubernamental
Punto de entrada del sistema simbólico-cognitivo EvoAI.
"""
import sys
import argparse
import logging
import os
import atexit
import base64
from pathlib import Path
from dotenv import load_dotenv, set_key
from cryptography.fernet import Fernet
from utils.tee import Tee

# ===================== 🔐 MANEJO DE CLAVE ESTADO ===================== #
env_path = Path(".env")
load_dotenv(dotenv_path=env_path)

sys.stdout = Tee('logs/symbolic_log.txt', 'a', sys.stdout)

def generate_fernet_key():
    return base64.urlsafe_b64encode(os.urandom(32)).decode()

def ensure_valid_fernet_key():
    key = os.getenv("EVOAI_STATE_KEY")
    try:
        Fernet(key.encode())
        print("[🔐 LOADED] Clave EVOAI_STATE_KEY válida cargada desde entorno o .env")
    except Exception:
        new_key = generate_fernet_key()
        set_key(str(env_path), "EVOAI_STATE_KEY", new_key)
        os.environ["EVOAI_STATE_KEY"] = new_key
        print("[🔐 AUTOSET] Clave EVOAI_STATE_KEY inválida o ausente. Generada y guardada automáticamente.")

ensure_valid_fernet_key()
# ===================================================================== #

from daemon.evoai_initializer_core import initialize_core_components
from daemon.evoai_cycle_executor import run_cycle_loop
from daemon.evoai_initializer_security import load_secure_key
from daemon.evoai_shutdown_manager import setup_signal_handlers
from core.self_diagnostics import SelfDiagnostics
from core.state_persistence import load_state, save_state

# === 🧠 Integración con núcleo simbiótico `ser_vivo` ===
try:
    from ser_vivo.conciencia_simulada import ConcienciaSimulada
    conciencia_simulada = ConcienciaSimulada()
    conciencia_simulada.boot()
    print("[🧠 BOOT] ConcienciaSimulada activada correctamente desde daemon.")
except Exception as e:
    conciencia_simulada = None
    print(f"[❌ ERROR] No se pudo activar ConcienciaSimulada: {e}")

try:
    from ser_vivo.evolucionador_simbolico import EvolucionadorSimbolico
    evolucionador_simbolico = EvolucionadorSimbolico(rule_engine=None, key="EVOLVE-ALPHA-4096")
    print("[🧬 BOOT] EvolucionadorSimbolico inicializado.")
except Exception as e:
    evolucionador_simbolico = None
    print(f"[❌ ERROR] Fallo al inicializar EvolucionadorSimbolico: {e}")

# Submódulos SER_VIVO integrados
from ser_vivo.generador_pensamiento import GeneradorPensamiento
from ser_vivo.gestor_emergencias import GestorEmergencias
from ser_vivo.nucleo_metainteligente import NucleoMetainteligente
from ser_vivo.planificador_autonomo import PlanificadorAutonomo
from ser_vivo.razonamiento_simbolico import Razonador
from ser_vivo.reconstruccion_simbolica import ReconstruccionSimbolica
from ser_vivo.sistema_emocional import SistemaEmocional
from ser_vivo.sistema_memoria import SistemaMemoria
from ser_vivo.funciones_dinamicas import FuncionesDinamicas
from ser_vivo.evaluador_existencial import EvaluadorExistencial
from ser_vivo.controlador_entropy import ControladorEntropia
from ser_vivo.conciencia_kernel import ConcienciaKernel
from ser_vivo.autoproteccion import AutoProteccion
from ser_vivo.auto_reflexion import AutoReflexion
from ser_vivo.analizador_semantico import AnalizadorSemantico

# 🔧 Módulo de recuperación metacognitiva
from metacognition.metacognitive_recovery_manager import protocolo_de_emergencia
from metacognition.supervisor_metacognitivo import SupervisorMetacognitivo
supervisor_metacognitivo = SupervisorMetacognitivo()

# === 🌐 Servidor web de visualización HALT ===
from tools.halt_server import lanzar_servidor
import threading

# Logger raíz
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] :: %(message)s",
    handlers=[
        logging.FileHandler("logs/evoai_super_daemon.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("EvoAI.Daemon")
DAEMON_KEY_FALLBACK = "A591243133418571088300454z"

# 🔒 Componentes globales
components = None

def persist_final_state():
    global components
    if components is None:
        return
    try:
        context = components.get("context", None)
        if context is not None and hasattr(context, "state"):
            save_state(context.state, encrypt=True)
            print("[📂 SAVE] Estado final guardado exitosamente (atexit).")
            logger.info("[SAVE] Estado guardado exitosamente al finalizar daemon (atexit).")
    except Exception as e:
        print(f"[❌ SAVE ERROR] Fallo al guardar estado (atexit): {e}")
        logger.error(f"[SAVE ERROR] {e}")

atexit.register(persist_final_state)

def main(daemon_key: str, test_mode: bool = False, resume: bool = False):
    global components
    setup_signal_handlers()

    if daemon_key != DAEMON_KEY_FALLBACK and daemon_key != load_secure_key():
        logger.critical("🔒 Clave inválida. Acceso denegado.")
        print("[❌ ACCESS] Clave inválida. Finalizando daemon.")
        return

    logger.info("🔑 Clave aceptada. Iniciando EvoAI...")
    print("[🔑 ACCESS] Clave validada correctamente. Arrancando núcleo...")

    initial_state = {}
    if resume:
        try:
            initial_state = load_state(decrypt=True)
            logger.info("[🔁 RESUME] Estado cargado correctamente desde disco.")
            print("[🔁 RESUME] Estado restaurado desde archivo persistente.")
        except Exception as e:
            logger.warning(f"[⚠️ RESUME ERROR] No se pudo cargar estado previo: {e}")
            print(f"[⚠️ RESUME ERROR] Fallo al cargar estado anterior: {e}")

    components = initialize_core_components(initial_state=initial_state)

    if conciencia_simulada:
        components["conciencia_simulada"] = conciencia_simulada
        print("[✅ LINK] ConcienciaSimulada integrada al sistema EvoAI.")
        logger.info("[LINK] ConcienciaSimulada integrada a los componentes principales.")

    if evolucionador_simbolico and components.get("rule_engine"):
        evolucionador_simbolico.rule_engine = components["rule_engine"]
        components["evolucionador_simbolico"] = evolucionador_simbolico
        print("[🧬 LINK] EvolucionadorSimbolico vinculado al motor de reglas.")
        logger.info("[LINK] EvolucionadorSimbolico conectado correctamente.")

    # Integrar subsistema SER_VIVO
    components["generador_pensamiento"] = GeneradorPensamiento()
    components["gestor_emergencias"] = GestorEmergencias()
    components["nucleo_metainteligente"] = NucleoMetainteligente()
    components["planificador_autonomo"] = PlanificadorAutonomo()
    components["razonador"] = Razonador()
    components["reconstruccion_simbolica"] = ReconstruccionSimbolica()
    components["sistema_emocional"] = SistemaEmocional()
    components["sistema_memoria"] = SistemaMemoria()
    components["funciones_dinamicas"] = FuncionesDinamicas()
    components["evaluador_existencial"] = EvaluadorExistencial()
    components["controlador_entropy"] = ControladorEntropia()
    components["conciencia_kernel"] = ConcienciaKernel()
    components["autoproteccion"] = AutoProteccion()
    components["auto_reflexion"] = AutoReflexion()
    components["analizador_semantico"] = AnalizadorSemantico()

    diagnostics = SelfDiagnostics(components)
    if not diagnostics.run_preflight_check(daemon_key):
        logger.critical("🚨 Diagnóstico fallido. Abortando daemon.")
        print("[❌ DIAG] Diagnóstico fallido. Abortando arranque.")
        return

    # === 🔍 Revisión metacognitiva previa al ciclo principal ===
    context_obj = components.get("context", None)
    if context_obj and hasattr(context_obj, "state"):
        contexto_critico = context_obj.state
    else:
        contexto_critico = {}

    resultado_supervision = supervisor_metacognitivo.evaluar(contexto_critico)
    if resultado_supervision.get("status") == "recovered":
        print("[🛠️ RECOVERY] Supervisor ejecutó recuperación simbólica correctamente.")
        logger.info("[SUPERVISION] Recuperación simbólica activada por SupervisorMetacognitivo.")

    # === 🌐 Iniciar servidor web HALTVisualizer en segundo plano ===
    try:
        threading.Thread(target=lanzar_servidor, daemon=True).start()
        print("[🌐 HALT SERVER] Visualizador HALT web activo en http://localhost:8080")
        logger.info("[HALT SERVER] Visualizador iniciado correctamente.")
    except Exception as e:
        print(f"[❌ ERROR] No se pudo iniciar el servidor HALTVisualizer: {e}")
        logger.warning(f"[HALT SERVER ERROR] {e}")

    try:
        run_cycle_loop(test_mode=test_mode)
    finally:
        persist_final_state()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EvoAI Super Symbolic Daemon")
    parser.add_argument("--key", required=False, help="Clave de acceso para el daemon")
    parser.add_argument("--test", action="store_true", help="Ejecutar en modo prueba (test_mode)")
    parser.add_argument("--resume", action="store_true", help="Reanudar estado desde disco (state resume)")
    args = parser.parse_args()
    daemon_key = args.key if args.key else load_secure_key()
    main(daemon_key, test_mode=args.test, resume=args.resume)
