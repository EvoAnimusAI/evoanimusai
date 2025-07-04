# evoai_network_learning.py
# -*- coding: utf-8 -*-
"""
Módulo para aprendizaje simbólico en red y adquisición de conceptos desde la web.
Diseñado bajo estándares de trazabilidad y seguridad informacional.
"""

import os
import logging
from datetime import datetime
from symbolic_ai.web_filter import extract_symbolic_concepts
from symbolic_ai.symbolic_logger import log_concept, log_synthesis

logger = logging.getLogger("EvoAI.NetworkLearning")

def learn_from_web(consciousness, net, topic: str, url: str, context, cycle: int):
    """
    Extrae conocimiento desde la red, lo resume y lo convierte en conceptos simbólicos.
    Efectúa registro trazado de síntesis y conceptos en almacenamiento y logs.

    :param consciousness: Núcleo de consciencia con evaluación de integridad.
    :param net: Módulo de red que permite extraction y síntesis.
    :param topic: Tópico objetivo del aprendizaje.
    :param url: Fuente URL validada.
    :param context: Módulo contextual para integración simbólica.
    :param cycle: Número de ciclo para trazabilidad.
    :return: Resumen generado o None en caso de error.
    """
    try:
        # Validación previa del núcleo consciente
        consciousness.evaluate_integrity()
        logger.info(f"🌐 Aprendiendo sobre '{topic}' desde: {url}")

        # Aprendizaje y síntesis del conocimiento
        net.learn_from_url(url, topic)
        summary = net.summarize_topic(topic)

        # Registro formal de la síntesis y almacenamiento
        log_synthesis(f"📚 Resumen '{topic}':\n{summary}")
        save_topic_summary(topic, summary, cycle)

        # Extraction y registro de conceptos simbólicos
        for concept in extract_symbolic_concepts(summary):
            context.add_concept(concept, source=f"wiki:{topic}")
            log_concept(concept, source=f"wiki:{topic}")

        return summary

    except Exception as e:
        logger.error(f"❌ Error al aprender desde red: {e}", exc_info=True)
        return None


def save_topic_summary(topic: str, summary: str, cycle: int):
    """
    Guarda en disco el resumen textual del conocimiento aprendido para auditoría.

    :param topic: Tema del resumen.
    :param summary: Texto sintetizado.
    :param cycle: Ciclo para nombramiento controlado.
    """
    os.makedirs("knowledge_logs", exist_ok=True)
    filename = f"knowledge_logs/cycle_{cycle}_{topic.replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary)
