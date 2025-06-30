# evoai_cycle_executor.py
# -*- coding: utf-8 -*-
"""
Gestión de ciclos de EvoAI: percepción, decisión, ejecución, mutación y registro.
"""
import time
import random
import logging
import os
import json
from symbolic_ai.symbolic_context import symbolic_context
from symbolic_ai.symbolic_logger import (
    log_entry, log_agent, log_decision, log_synthesis,
    log_concept, log_rewrite
)
from visual.symbolic_view import show_symbolic_state
from autoprogramming.directed_mutation import mutate_parent_function
from autoprogramming.mutation_evaluation import evaluate_mutation
from autoprogramming.mutation_generator import generate_and_save_mutation
from symbolic_ai.web_filter import extract_symbolic_concepts
from mutations.mutation_engine import mutate_function

logger = logging.getLogger("EvoAI.CycleExecutor")


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
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if not isinstance(loaded, list):
                    logger.warning(f"[SECURITY] Memoria simbólica corrupta o malformada en '{path}', reiniciando lista.")
                    memory = []
                else:
                    memory = loaded
        memory.append({"code": code, "origin": "mutation"})
        with open(path, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
        logger.info(f"[SECURITY] Memoria simbólica actualizada correctamente en '{path}'.")
    except (json.JSONDecodeError, IOError, OSError) as e:
        logger.error(f"[CRITICAL] Error crítico al actualizar memoria simbólica en '{path}': {e}")
        raise RuntimeError(f"Fallo crítico en memoria simbólica: {e}")


def run_cycle(cycle, context, engine, agent, executor, decision_engine,
              consciousness, codex, current_function, preferred_topics):
    logger.info(f"🤖 Iniciando ciclo #{cycle}")

    engine.run_iteration(cycle)

    observation = {
        'pos': cycle,
        'state': 'active',
        'action': 'wait' if cycle % 2 == 0 else 'explore',
        'noise': random.choice(["neutral", "harmonic", "chaos", "tension", "calm", None]),
        'time': time.time()
    }

    agent.perceive(observation)

    if hasattr(context, "update"):
        context.update(observation)

    actions = engine.symbolic_learning_engine.apply_rules(observation)
    decision = actions[0] if actions else decision_engine.evaluate(observation)
    print(f"[DEBUG] Decision tomada: {decision}")
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
        logger.warning(f"[Visualización] Falló: {e}")

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
        codex.network.learn_from_url(url, topic)
        summary = codex.network.summarize_topic(topic)
        logger.info(f"📚 Resumen adquirido: {summary}")

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
        logger.info(f"🔧 Codex {'modificó' if changed else 'no modificó'} {target_file}. Log: {log_path}")

    # Ahora condicionamos la mutación dirigida a la decisión "mutate_parent"
    if decision == "mutate_parent":
        ctx = get_symbolic_context()
        logger.info(f"🧠 Contexto simbólico: {ctx}")
        new_func = mutate_parent_function(current_function, ctx, preferred_topics)
        if evaluate_mutation(new_func, ctx):
            logger.info("✔ Mutación dirigida aceptada")
            current_function.clear()
            current_function.update(new_func)
            with open("symbolic_memory.json", "w", encoding="utf-8") as f:
                json.dump(current_function, f, indent=2, ensure_ascii=False)
        else:
            logger.info("✘ Mutación dirigida rechazada")

    execute_directed_function(current_function)

    if cycle % 10 == 0:
        logger.info("🔁 Ejecutando mutación simbólica...")
        filename = generate_and_save_mutation()
        path = f"data/mutated_functions/{filename}"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            if evaluate_mutation({"code": code}, context):
                logger.info(f"✅ Mutación simbólica aceptada: {filename}")
                save_to_symbolic_memory(code)
            else:
                logger.info(f"❌ Mutación simbólica rechazada: {filename}")


def run_cycle_loop(components: dict, test_mode: bool = False):
    """
    Bucle principal de ejecución cíclica de EvoAI.

    Args:
        components (dict): Diccionario con instancias del sistema (agent, engine, context, etc.).
        test_mode (bool): Si es True, se ejecuta un número limitado de ciclos para pruebas.
    """
    cycle = 0
    current_function = {"name": "init", "steps": []}
    preferred_topics = ["evolution", "symbolic reasoning", "metacognition"]

    try:
        while True:
            run_cycle(
                cycle=cycle,
                context=components["context"],
                engine=components["engine"],
                agent=components["agent"],
                executor=components["executor"],
                decision_engine=components["decision"],
                consciousness=components["consciousness"],
                codex=components["codex"],
                current_function=current_function,
                preferred_topics=preferred_topics
            )
            cycle += 1
            if test_mode and cycle >= 5:
                logger.info("[TEST_MODE] Ciclos completados con éxito.")
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.warning("🚨 Ciclo abortado por el usuario.")
    except Exception as e:
        logger.error(f"[CRITICAL] Error durante el ciclo: {e}", exc_info=True)
