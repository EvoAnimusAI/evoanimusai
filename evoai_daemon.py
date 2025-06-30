# evoai_daemon.py
# -*- coding: utf-8 -*-

import sys
import os
import time
import json
import random
import logging
import argparse
import traceback
from pathlib import Path
from datetime import datetime

# --- Bootstrap y motores ---
from evoai_bootstrap import bootstrap_evoai
from strategies.strategy_manager import StrategyManager

# --- Núcleo EvoAI ---
from core.context import EvoContext
from core.agent import EvoAgent
from core.engine import EvoAIEngine, EvoAIExecutor
from core.decision import DecisionEngine

# --- Módulos auxiliares ---
from runtime.monitor import EvoAIMonitor
from core.self_reflection import CodeAnalyzer
from core.autoconsciousness import Autoconsciousness
from core.network_access import NetworkAccess
from core.evo_codex import EvoCodex
from core.analyzer_daemon import EvoAIAnalyzerDaemon

# --- Metacognición y mutación dirigida ---
from metacognition.targeted_mutation import TargetedMutation as DirectedMutation

# --- Symbolic AI ---
from symbolic_ai.symbolic_context import symbolic_context
from symbolic_ai.symbolic_learning_engine import SymbolicLearningEngine
from symbolic_ai.symbolic_logger import (
    log_entry, log_agent, log_decision, log_synthesis,
    log_concept, log_learning, log_rewrite
)
from symbolic_ai.web_filter import extract_symbolic_concepts

# --- Visualización ---
from visual.symbolic_view import show_symbolic_state

# --- Mutaciones automáticas ---
from mutations.mutation_engine import mutate_function
from autoprogramming.directed_mutation import mutate_parent_function
from autoprogramming.mutation_evaluation import evaluate_mutation
from autoprogramming.mutation_generator import generate_and_save_mutation

# --- Configuración ---
DAEMON_KEY = "A591243133418571088300454z"
CYCLE_DELAY = 30
MAX_ERRORS = 10
CYCLES_TO_MUTATE = 10
MEMORY_PATH = "symbolic_memory.json"

# --- Logger global ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] :: %(message)s",
    handlers=[
        logging.FileHandler("logs/evoai_super_daemon.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("EvoAI.SuperDaemon")

# --- Estado dirigido ---
cycle_counter = 0
current_function = {
    "name": "base_function",
    "steps": [
        {"action": "calm_down", "param": 1.0},
        {"action": "slow_down", "param": 2.0}
    ]
}
preferred_topics = ["calm_down", "slow_down"]
strategy_manager = StrategyManager()
directed_mutator = DirectedMutation()


# -------------------- FUNCIONES AUXILIARES --------------------

def ensure_logs_dir():
    os.makedirs("knowledge_logs", exist_ok=True)


def log_local(msg: str):
    with open("evoai_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} - {msg}\n")
    logger.info(msg)


def save_memory():
    global current_function
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(current_function, f, indent=2, ensure_ascii=False)


def load_memory():
    global current_function
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            current_function = json.load(f)


def get_symbolic_context():
    return {
        'noise': random.choice(["neutral", "harmonic", "chaos", "tension", "calm", None]),
        'state': random.choice(["normal", "active", "stressed"])
    }


def execute_directed_function(func: dict):
    logger.info(f"[DirectedMutation] Ejecutando función dirigida: {func.get('name')}")
    for step in func.get("steps", []):
        logger.info(f"  • Acción: {step.get('action')} | Param: {step.get('param')}")


def save_to_symbolic_memory(code: str):
    path = "data/symbolic_memory.json"
    memory = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            memory = json.load(f)
    memory.append({"code": code, "origin": "mutation"})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


# -------------------- PROGRAMA PRINCIPAL --------------------

def main(daemon_key: str, test_mode: bool = False):
    global current_function, cycle_counter

    if daemon_key != DAEMON_KEY:
        logger.critical("🔒 Llave incorrecta. Abortando ejecución.")
        return

    context = EvoContext()
    # Instanciamos motor simbólico
    symbolic_engine = SymbolicLearningEngine()
    context.symbolic = symbolic_engine

    agent = EvoAgent(name="EvoAI", context=context)
    engine = EvoAIEngine(agent=agent, context=context)
    # IMPORTANTÍSIMO: asignar motor simbólico también al contexto para evitar errores
    context.engine = symbolic_engine  # aquí se corrige la causa del error

    engine.symbolic_learning_engine = symbolic_engine
    engine.strategy_manager = strategy_manager

    analyzer = EvoAIAnalyzerDaemon(engine, log_file='logs/logs_evoai.json', interval=20)
    bootstrap_evoai(engine)

    logger.info("🚀 Iniciando EvoAI Super Symbolic Daemon (modo test: %s)...", test_mode)

    monitor = EvoAIMonitor()
    executor = EvoAIExecutor(agent=agent, engine=engine, monitor=monitor, context=context)
    code_analyzer = CodeAnalyzer(root_path=".")
    consciousness = Autoconsciousness("Daniel Santiago Ospina Velasquez", "AV255583")
    net = NetworkAccess(master_key=DAEMON_KEY)
    codex = EvoCodex(root_path=".")
    decision_engine = DecisionEngine(context.symbolic)

    consciousness.declare_existence()
    ensure_logs_dir()
    load_memory()

    cycle = 1
    errors = 0
    max_cycles = 1 if test_mode else float('inf')

    while cycle <= max_cycles:
        try:
            logger.info(f"🤔 Ciclo #{cycle}")
            engine.run_iteration(cycle)

            observation = {
                'pos': cycle,
                'state': 'active',
                'action': 'wait' if cycle % 2 == 0 else 'explore',
                'noise': random.choice(["neutral", "harmonic", "chaos", "tension", "calm", None]),
                'time': time.time()
            }

            agent.perceive(observation)

            # Corrección aquí: reemplazar llamada inexistente
            if hasattr(context, "update"):
                context.update(observation)
            else:
                logger.warning("⚠️ 'EvoContext' no tiene método update(), omitiendo actualización explícita.")

            actions = engine.symbolic_learning_engine.apply_rules(observation)
            decision = actions[0] if actions else decision_engine.evaluate(observation)
            symbolic_context.register_metacognition(f"Decision: {decision}")
            logger.info(f"⚡ Decisión simbólica: {decision}")

            result = executor.execute()
            reward = min(1.0, max(-1.0, (1.0 if result else -0.2) + (0.5 if observation['action'] != 'wait' else 0)))
            engine.symbolic_learning_engine.cross_reinforcement(
                condition=f"noise == '{observation.get('noise')}'",
                action=decision,
                reward=reward,
                observation=observation
            )

            agent.learn(observation, decision, reward)

            try:
                show_symbolic_state(context, decision, observation, reward)
            except Exception as e:
                logger.warning(f"[Visualización] No se pudo mostrar contexto: {e}")

            executor.monitor.log(cycle, observation, decision, reward)

            log_entry(None, None, cycle=cycle)
            log_decision(agent.name, "symbolic/action", decision)
            log_agent(agent.name)
            log_synthesis(f"Ciclo #{cycle} con recompensa: {reward}")

            if engine.last_mutated_function:
                func = engine.last_mutated_function
                log_synthesis(f"Función mutada: `{func.name}` → {func.description}")
                log_rewrite(getattr(func, 'file_path', 'N/A'))

            if cycle % 10 == 0:
                consciousness.evaluate_integrity()
                topic = "symbolic evolution"
                url = "https://en.wikipedia.org/wiki/Evolutionary_algorithm"
                net.learn_from_url(url, topic)
                summary = net.summarize_topic(topic)
                log_local(f"📚 Resumen '{topic}':\n{summary}")

                for concept in extract_symbolic_concepts(summary):
                    context.add_concept(concept, source="wiki:evolution")
                    log_concept(concept, source="wiki:evolution")

                mutated = mutate_function(agent.memory.retrieve_all(), context)
                engine.last_mutated_function = mutated
                log_rewrite(mutated.name, mutated.description, getattr(mutated, 'file_path', 'N/A'))

                summary_path = f"knowledge_logs/cycle_{cycle}_{topic.replace(' ', '_')}.txt"
                with open(summary_path, "w", encoding="utf-8") as f:
                    f.write(summary)

                target_file = random.choice(["core/engine.py", "core/agent.py", "core/decision.py"])
                changed, log_path = codex.execute_auto_rewrite(target_file)
                log_local(f"🔧 Codex {'modificó' if changed else 'no modificó'} {target_file}. Log: {log_path}")

            if cycle % 3 == 0:
                ctx = get_symbolic_context()
                logger.info(f"🧠 Contexto simbólico: {ctx}")
                new_func = mutate_parent_function(current_function, ctx, preferred_topics)
                if evaluate_mutation(new_func, ctx):
                    logger.info("✔ Mutación dirigida aceptada")
                    current_function = new_func
                    save_memory()
                else:
                    logger.info("✘ Mutación dirigida rechazada")

            execute_directed_function(current_function)

            if (cycle_counter := cycle_counter + 1) % CYCLES_TO_MUTATE == 0:
                logger.info("🔁 Ejecutando mutación simbólica...")
                filename = generate_and_save_mutation()
                path = f"data/mutated_functions/{filename}"
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        code = f.read()
                    if evaluate_mutation({"code": code}, context):
                        logger.info(f"✅ Mutación aceptada: {filename}")
                        save_to_symbolic_memory(code)
                    else:
                        logger.info(f"❌ Mutación rechazada: {filename}")

            cycle += 1
            if not test_mode:
                time.sleep(CYCLE_DELAY)

        except Exception:
            errors += 1
            logger.error("💥 Excepción durante ciclo", exc_info=True)
            if errors >= MAX_ERRORS:
                logger.critical("☠ Demasiados errores. Abortando daemon.")
                break


# -------------------- CLI ENTRY POINT --------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EvoAI Super Symbolic Daemon")
    parser.add_argument("--key", required=True, help="Clave de acceso para el daemon")
    parser.add_argument("--test", action="store_true", help="Ejecuta solo 1 ciclo de prueba")
    args = parser.parse_args()
    main(args.key, test_mode=args.test)
