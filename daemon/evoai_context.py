# daemon/evoai_context.py
# -*- coding: utf-8 -*-
"""
Contexto operativo central de EvoAI.
Provee un marco simbólico, memoria, estado y configuración,
con trazabilidad exhaustiva para auditoría y monitoreo.
Cumple estándares gubernamentales de seguridad y control.
"""

import datetime
import logging
from typing import Optional, Dict, Any

from symbolic_ai.symbolic_learning_engine import SymbolicLearningEngine
from core.memory import AgentMemory
from core.config import Config
from core.state_manager import StateManager

logger = logging.getLogger("EvoAI.Context")

def normalizar_observacion(observacion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Traduce claves de observaciones desde español (u otros alias)
    a los términos esperados en inglés, especialmente 'entropy'.
    """
    traducciones = {
        'entropy': 'entropy',
        'noise': 'noise',
        'state': 'state',
        'ultima_accion': 'last_action',
        'last_action': 'last_action',
    }

    normalizada = {traducciones.get(k, k): v for k, v in observacion.items()}

    print(f"[🛠️ NORMALIZACIÓN] Original: {observacion}")
    print(f"[✅ NORMALIZADA] Resultante: {normalizada}")

    return normalizada

class EvoAIContext:
    """
    Contexto global para la ejecución del agente EvoAI.
    Componentes:
    - Motor simbólico (SymbolicLearningEngine o compatible)
    - Memoria (AgentMemory)
    - Estado (StateManager)
    - Configuración (Config)
    
    Funcionalidades:
    - Actualización del contexto con validación y trazabilidad
    - Registro explícito de conceptos simbólicos
    - Exposición de estado para auditoría
    """

    def __init__(
        self,
        symbolic_engine: Optional[Any] = None,
        app_name: str = "EvoAI",
        version: str = "1.0.0"
    ):
        print(f"[🧠 INIT] Inicializando EvoAIContext...")
        self.symbolic: SymbolicLearningEngine = symbolic_engine if symbolic_engine else SymbolicLearningEngine()
        self.memory: AgentMemory = AgentMemory()
        self.state: StateManager = StateManager()
        self.config: Config = Config(app_name=app_name, version=version)
        self.engine: Optional[Any] = None  # Motor externo si aplica

        logger.info(f"🔧 EvoAIContext inicializado [{datetime.datetime.utcnow().isoformat()}]")
        print(f"[✅ INIT] EvoAIContext activo — Versión: {version}")

    def update(self, observation: Dict[str, Any]) -> None:
        """
        Actualiza el contexto con una nueva observación.
        Valida y registra la observación, propagándola internamente.
        """
        if not isinstance(observation, dict):
            logger.error(f"Observación inválida (no dict): {observation}")
            raise TypeError("La observación debe ser un diccionario válido.")

        try:
            observacion_normalizada = normalizar_observacion(observation)

            if "last_action" in observacion_normalizada:
                print(f"[🔁 INFO] Última acción reportada: {observacion_normalizada['last_action']}")

            print(f"[📡 CONTEXTO::OBSERVE] Enviando al motor simbólico: {observacion_normalizada}")

            if self.symbolic:
                self.symbolic.observe(observacion_normalizada)

            if self.state:
                self.state.update(observation)

            logger.info(f"[Context] Observación registrada: {observation}")
            print(f"[✅ CONTEXTO ACTUALIZADO] con {list(observacion_normalizada.keys())}")

        except Exception as ex:
            logger.exception(f"Error al actualizar contexto con la observación: {ex}")
            print(f"[❌ ERROR::UPDATE CONTEXT] {ex}")
            raise

    def add_concept(self, concept: str, source: str = "unknown") -> None:
        """
        Agrega un concepto simbólico al motor simbólico con trazabilidad.
        """
        if not isinstance(concept, str) or not concept.strip():
            logger.error(f"Concepto inválido para agregar: '{concept}'")
            raise ValueError("Concepto debe ser una cadena no vacía.")

        if self.symbolic:
            try:
                if hasattr(self.symbolic, "register_concept"):
                    self.symbolic.register_concept(concept.strip(), source)
                    logger.info(f"[Context] Concepto agregado: '{concept}' (fuente: {source})")
                    print(f"[➕ CONCEPTO] '{concept}' agregado desde '{source}'")
                else:
                    logger.warning("[Context] register_concept no implementado en SymbolicLearningEngine")
                    print(f"[⚠️ WARNING] register_concept no soportado en el motor simbólico")
            except Exception as ex:
                logger.exception(f"Error al agregar concepto '{concept}': {ex}")
                print(f"[❌ ERROR::ADD CONCEPT] {ex}")
                raise

    def get_state_snapshot(self) -> Dict[str, Any]:
        """
        Obtiene una instantánea del estado interno del contexto.
        Incluye memoria, estado simbólico, configuración y timestamp.
        """
        try:
            snapshot = {
                "timestamp_utc": datetime.datetime.utcnow().isoformat(),
                "symbolic_state": self.symbolic.export_state() if self.symbolic else None,
                "memory_summary": self.memory.summary() if self.memory else None,
                "state_status": self.state.status() if self.state and hasattr(self.state, "status") else None,
                "config_version": getattr(self.config, "version", "unknown"),
            }

            logger.debug(f"[Context] Snapshot state: {snapshot}")
            print(f"[📸 SNAPSHOT] {snapshot}")
            return snapshot

        except Exception as ex:
            logger.exception(f"Error al obtener snapshot del state: {ex}")
            print(f"[❌ ERROR::SNAPSHOT] {ex}")
            raise
