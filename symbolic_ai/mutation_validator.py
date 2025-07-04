# -*- coding: utf-8 -*-
"""
Módulo de validación de mutaciones simbólicas para EvoAnimusAI.
Asegura que las funciones mutadas sean seguras, trazables y compatibles
con el entorno de ejecución simbólico de alta seguridad.

Nivel: MILITAR / GUBERNAMENTAL / ULTRA-SECRETO
"""

import types
import inspect
import logging
import traceback

logger = logging.getLogger("MutationValidator")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def is_valid_callable(obj) -> bool:
    """
    Verifica si el objeto es una función segura, ejecutable y auditable.

    Requisitos:
    - Debe ser callable
    - No debe ser clase
    - Debe tener firma válida (acepta argumentos)
    """
    if not callable(obj):
        logger.warning(f"[Rechazado] Objeto no callable detectado: {type(obj).__name__}")
        return False

    if isinstance(obj, type):
        logger.warning(f"[Rechazado] Clase recibida como función mutada: {obj.__name__}")
        return False

    try:
        sig = inspect.signature(obj)
        logger.debug(f"[Validación] Firma aceptada: {sig}")
        return True
    except (ValueError, TypeError) as e:
        logger.error(f"[Error de Firma] Objeto inválido: {repr(obj)} | Excepción: {str(e)}")
        return False

def is_valid_symbolic_rule(obj) -> bool:
    """
    Verifica si la regla simbólica es una cadena segura y compatible.
    Se usa cuando se espera una regla tipo str generada simbólicamente.
    """
    if isinstance(obj, str) and "⇒" in obj and "::" in obj:
        logger.debug(f"[Validación] Regla simbólica reconocida: {obj}")
        return True
    logger.warning(f"[Rechazado] Regla simbólica inválida o malformada: {repr(obj)}")
    return False

def log_invalid_mutation(obj):
    """
    Registro forense y de auditoría estructural.
    Se puede integrar con SIEM u observabilidad avanzada.
    """
    try:
        logger.error(f"[MUTACIÓN INVÁLIDA] Tipo: {type(obj).__name__} | Repr: {repr(obj)}")
        logger.debug("[StackTrace Mutación]:\n" + "".join(traceback.format_stack()))
    except Exception as e:
        logger.critical(f"[ERROR DE AUDITORÍA] {e}")

def safe_wrap(obj):
    """
    Encapsulamiento seguro de objetos mutados inválidos.
    Devuelve un callable que no ejecuta el objeto mutado directamente.
    """
    def safe_callable_wrapper(*args, **kwargs):
        logger.warning(
            f"[Envoltorio Activado] Objeto mutado no ejecutable fue encapsulado: {repr(obj)}"
        )
        return {
            "status": "unsafe_mutation",
            "original_type": type(obj).__name__,
            "payload": repr(obj)
        }
    return safe_callable_wrapper

def validate_and_prepare(obj):
    """
    Validación completa y preparación segura para funciones mutadas.
    Si la función es inválida o es una regla simbólica en string,
    se procesa adecuadamente. Si no pasa validación, se encapsula.
    """
    if is_valid_callable(obj):
        logger.info(f"[Mutación Aprobada] Objeto validado y listo para ejecución: {repr(obj)}")
        return obj

    if is_valid_symbolic_rule(obj):
        logger.info(f"[Mutación Aprobada] Regla simbólica válida como string: {repr(obj)}")
        return obj

    log_invalid_mutation(obj)
    return safe_wrap(obj)
