"""
entropy_injector.py ▸ Módulo de rescate simbólico para EvoAI
Función: Inyecta entropía artificial progresiva ante estancamiento simbólico.
Nivel: Seguridad militar / trazabilidad completa / listo para producción.
"""

import datetime
import logging
import sys

# Logger local
logger = logging.getLogger("EntropyInjector")
if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] [EntropyInjector] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

# Configuración
ENTROPY_TRIGGER_ITERATION = 20        # Umbral de ciclos para iniciar inyección
ENTROPY_STEP = 0.05                   # Incremento de entropía por ciclo estancado
MAX_ENTROPY = 1.0                     # Límite superior absoluto

def inject_entropy(context: dict, iteration: int) -> dict:
    """
    Inyecta entropía artificial al contexto si detecta estancamiento.

    Parámetros:
        context (dict): Contexto simbólico observado.
        iteration (int): Número de iteración simbólica actual.

    Retorna:
        dict: Contexto posiblemente modificado.
    """
    try:
        if not isinstance(context, dict):
            logger.error("Tipo de contexto inválido. Se esperaba dict, se recibió: %s", type(context))
            return context

        entropy = context.get("entropy", 0.0)

        print(f"[🧪 CHECK] Iteración: {iteration} | Entropía actual: {entropy}")

        if entropy == 0.0 and iteration >= ENTROPY_TRIGGER_ITERATION:
            step_count = iteration - ENTROPY_TRIGGER_ITERATION + 1
            injected = round(min(MAX_ENTROPY, ENTROPY_STEP * step_count), 4)

            logger.warning("Entropía 0.0 detectada tras %d ciclos. Inyectando %.4f", step_count, injected)
            print(f"[⚠️ INJECT] Entropía artificial inyectada: {injected} (iter #{iteration})")

            context["entropy"] = injected
            context["__entropy_injected"] = True
            context["__entropy_level"] = injected

        else:
            print("[✅ OK] No se requiere inyección de entropía en este ciclo.")

        return context

    except Exception as ex:
        logger.exception("Fallo crítico durante la inyección de entropía: %s", ex)
        print(f"[❌ CRASH] Excepción en inject_entropy(): {ex}")
        return context
