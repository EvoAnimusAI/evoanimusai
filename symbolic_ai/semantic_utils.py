# symbolic_ai/semantic_utils.py
# -*- coding: utf-8 -*-
"""
Utilidades semánticas y de normalización para EvoAI
-------------------------------------------------------------------------------
Responsabilidad:
- Traducción de claves desde idioma natural a representaciones simbólicas.
- Limpieza y validación estructural del contexto.
- Compatibilidad defensiva con motores simbólicos de inferencia.

Nivel: MILITAR / GUBERNAMENTAL / CRÍTICO
"""

import logging
from typing import Dict, Any

logger = logging.getLogger("SemanticUtils")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# 🔑 Diccionario canónico de claves
clave_map = {
    "noise": "noise",
    "entropy": "entropy",
    "temperatura": "temperature",
    "presión": "pressure",
    "luminosidad": "luminosity",
    "velocidad": "speed",
    "ciclo": "cycle",
    "tasa_error": "error_rate",
    "presupuesto_mutacion": "mutation_budget",
    "rechazos": "rejected_mutations",
    "recompensas": "recent_rewards",
    # Puedes ampliar esto según el dominio simbólico
}

def normalizar_observacion(observacion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Traduce claves naturales a simbólicas y limpia la observación.
    Filtra valores no serializables o estructuras ilegales.
    """
    print(f"[🧹 NORMALIZAR] Iniciando proceso sobre: {observacion}")
    resultado = {}

    for k, v in observacion.items():
        clave = clave_map.get(k, k)
        if isinstance(v, (int, float, str, bool)):
            resultado[clave] = v
        elif isinstance(v, (list, tuple)):
            resultado[clave] = [x for x in v if isinstance(x, (int, float, str, bool))]
        else:
            logger.debug(f"[⚠️ FILTRADO] Clave '{clave}' con tipo inválido: {type(v).__name__}")
    
    print(f"[✅ NORMALIZAR] Resultado: {resultado}")
    logger.info("[Normalizar] Observación normalizada: %s", resultado)
    return resultado
