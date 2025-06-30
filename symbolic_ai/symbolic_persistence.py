"""
symbolic_ai.symbolic_persistence

Módulo para registrar, persistir y recuperar funciones mutadas simbólicas
en EvoAI. Maneja almacenamiento local en formato JSON con control
de versiones y manejo de errores robusto.

Author: Daniel Santiago Ospina Velasquez
"""

import json
import logging
from pathlib import Path
from threading import Lock
from typing import Optional, Dict

logger = logging.getLogger("evoai.symbolic_persistence")
logger.setLevel(logging.INFO)


class MutatedFunctionRegistry:
    """
    Registro y persistencia de funciones mutadas simbólicas.

    Almacena funciones en memoria y sincroniza con disco con
    control de concurrencia para evitar corrupciones.
    """

    def __init__(self, persistence_path: Path = Path("data/mutated_functions.json")):
        self._registry: Dict[str, str] = {}
        self.persistence_path = persistence_path
        self._lock = Lock()
        self._load_from_disk()

    def register(self, func_id: str, func_source: str) -> None:
        """
        Registra una función mutada en memoria y persiste a disco.

        Args:
            func_id (str): Identificador único de la función.
            func_source (str): Código fuente o representación serializada.
        """
        if not func_id or not func_source:
            logger.warning("[symbolic_persistence] ID o fuente vacíos, registro omitido.")
            return

        with self._lock:
            self._registry[func_id] = func_source
            logger.info(f"[symbolic_persistence] Registrada función mutada: {func_id}")
            self._save_to_disk()

    def get(self, func_id: str) -> Optional[str]:
        """
        Recupera el código fuente de una función mutada por ID.

        Args:
            func_id (str): Identificador único de la función.

        Returns:
            Optional[str]: Código fuente si existe, None si no.
        """
        with self._lock:
            return self._registry.get(func_id)

    def _save_to_disk(self) -> None:
        """Guarda el registro completo en archivo JSON."""
        try:
            self.persistence_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.persistence_path, "w", encoding="utf-8") as f:
                json.dump(self._registry, f, ensure_ascii=False, indent=4)
            logger.info(f"[symbolic_persistence] Guardado registro en {self.persistence_path}")
        except Exception as e:
            logger.error(f"[symbolic_persistence] Error guardando registro: {e}")

    def _load_from_disk(self) -> None:
        """Carga el registro desde disco si existe."""
        if not self.persistence_path.exists():
            logger.info(f"[symbolic_persistence] Archivo no encontrado: {self.persistence_path}, iniciando vacío.")
            return
        try:
            with open(self.persistence_path, "r", encoding="utf-8") as f:
                self._registry = json.load(f)
            logger.info(f"[symbolic_persistence] Registro cargado desde {self.persistence_path}")
        except Exception as e:
            logger.error(f"[symbolic_persistence] Error cargando registro: {e}")
            self._registry = {}


# Singleton global para uso en EvoAI
register_mutated_function = MutatedFunctionRegistry()
