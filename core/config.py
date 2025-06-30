# core/config.py
# -*- coding: utf-8 -*-
"""
Subsistema de configuración de EvoAI.
Carga segura, validación estricta y soporte de override mediante variables de entorno.
Estructura inmutable tipo singleton. Nivel de trazabilidad gubernamental.
"""

import json
import os
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, ClassVar

logger = logging.getLogger("EvoAI.Config")

@dataclass(frozen=True)
class Config:
    """
    Configuración inmutable de EvoAI cargada desde archivo JSON.
    Permite override seguro vía variables de entorno.
    """

    # Parámetros configurables
    app_name: str
    version: str
    debug: bool = False
    database_url: str = field(default="sqlite:///default.db")
    max_workers: int = field(default=4)
    timeout_seconds: int = field(default=30)

    # Singleton interno
    _instance: ClassVar[Optional["Config"]] = None

    @classmethod
    def load_from_file(cls, path: str) -> "Config":
        """
        Carga y valida la configuración desde archivo JSON.

        Args:
            path (str): Ruta al archivo de configuración.

        Returns:
            Config: Instancia singleton cargada y validada.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw_data: Dict[str, Any] = json.load(f)
        except FileNotFoundError:
            logger.critical(f"[CONFIG] Archivo de configuración no encontrado: {path}")
            raise
        except json.JSONDecodeError as e:
            logger.critical(f"[CONFIG] JSON inválido en archivo {path}: {e}")
            raise

        raw_data = cls._apply_env_overrides(raw_data)
        instance = cls._create_and_validate(raw_data)
        cls._instance = instance

        logger.info(f"[CONFIG] Configuración cargada correctamente desde {path}")
        return instance

    @classmethod
    def get_instance(cls) -> "Config":
        """
        Retorna la instancia cargada del singleton.

        Raises:
            RuntimeError: Si no se ha cargado previamente.
        """
        if cls._instance is None:
            raise RuntimeError("[CONFIG] Configuración no inicializada. Ejecutar load_from_file().")
        return cls._instance

    @staticmethod
    def _apply_env_overrides(config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aplica overrides desde variables de entorno.

        Args:
            config_data (dict): Diccionario base cargado desde archivo.

        Returns:
            dict: Diccionario con valores actualizados desde el entorno.
        """
        result = config_data.copy()
        for key, value in config_data.items():
            env_key = key.upper()
            env_val = os.getenv(env_key)
            if env_val is not None:
                original_type = type(value)
                try:
                    if original_type is bool:
                        env_val = env_val.strip().lower() in {"1", "true", "yes", "on"}
                    elif original_type is int:
                        env_val = int(env_val)
                    elif original_type is float:
                        env_val = float(env_val)
                    elif original_type is str:
                        env_val = str(env_val)
                    else:
                        continue
                    result[key] = env_val
                    logger.debug(f"[CONFIG] Override {key} <- ENV[{env_key}] = {env_val}")
                except Exception as e:
                    logger.warning(f"[CONFIG] Variable de entorno inválida {env_key}: {e}")
        return result

    @classmethod
    def _create_and_validate(cls, data: Dict[str, Any]) -> "Config":
        """
        Crea la instancia de configuración y valida campos críticos.

        Raises:
            ValueError: Si faltan campos obligatorios o tipos inválidos.
        """
        required = {"app_name", "version"}
        missing = required - data.keys()
        if missing:
            raise ValueError(f"[CONFIG] Campos obligatorios ausentes: {missing}")

        if not isinstance(data["app_name"], str) or not data["app_name"].strip():
            raise ValueError("[CONFIG] 'app_name' debe ser una cadena no vacía.")
        if not isinstance(data["version"], str) or not data["version"].strip():
            raise ValueError("[CONFIG] 'version' debe ser una cadena no vacía.")

        if "debug" in data and not isinstance(data["debug"], bool):
            raise ValueError("[CONFIG] 'debug' debe ser booleano.")
        if "max_workers" in data and (not isinstance(data["max_workers"], int) or data["max_workers"] < 1):
            raise ValueError("[CONFIG] 'max_workers' debe ser un entero ≥ 1.")
        if "timeout_seconds" in data and (not isinstance(data["timeout_seconds"], int) or data["timeout_seconds"] < 1):
            raise ValueError("[CONFIG] 'timeout_seconds' debe ser un entero ≥ 1.")
        if "database_url" in data and not isinstance(data["database_url"], str):
            raise ValueError("[CONFIG] 'database_url' debe ser una cadena válida.")

        return cls(**data)
