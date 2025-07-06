# ser_vivo/evolucionador_simbolico.py
# -*- coding: utf-8 -*-
"""
Evolucionador Simbólico - Nivel militar / estándar gubernamental
Permite mutación, evaluación y selección adaptativa de reglas simbólicas
dentro del sistema EvoAI.
"""

import random
import logging
import hashlib
from copy import deepcopy
from datetime import datetime

from symbolic_ai.symbolic_rule import SymbolicRule
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine
from symbolic_ai.secure_expression_evaluator import SecureExpressionEvaluator

# Configurar logger
logger = logging.getLogger("EvolucionadorSimbolico")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("logs/evolution_audit.log")
formatter = logging.Formatter('%(asctime)s [%(levelname)s] :: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Clave interna para activar evolución simbólica
EVOLUTION_KEY = "EVOLVE-ALPHA-4096"

class EvolucionadorSimbolico:
    def __init__(self, rule_engine: SymbolicRuleEngine, key: str):
        self.rule_engine = rule_engine
        self.evaluator = SecureExpressionEvaluator()
        self.enabled = (key == EVOLUTION_KEY)
        self.generacion = 0
        if self.enabled:
            print("[🧬 EVO-ENGINE] Activado con clave segura.")
            logger.info("Motor de evolución simbólica ACTIVADO.")
        else:
            print("[🛑 EVO-ENGINE] Clave incorrecta. Módulo inactivo.")
            logger.warning("Intento de activación fallido.")

    def _mutar_condicion(self, condicion: str) -> str:
        try:
            if ">=" in condicion:
                return condicion.replace(">=", "<=")
            elif "<=" in condicion:
                return condicion.replace("<=", ">=")
            elif "==" in condicion:
                return condicion.replace("==", "!=")
            elif "!=" in condicion:
                return condicion.replace("!=", "==")
            elif ">" in condicion:
                return condicion.replace(">", "<")
            elif "<" in condicion:
                return condicion.replace("<", ">")
        except Exception as e:
            logger.error(f"[❌ MUTACIÓN] Fallo al mutar condición: {e}")
        return condicion

    def _evaluar_regla(self, regla: SymbolicRule, contexto: dict) -> float:
        try:
            resultado = self.evaluator.evaluar(regla.condicion, contexto)
            fitness = 1.0 if resultado else 0.0
            logger.info(f"[🔍 EVAL] Condición: '{regla.condicion}' => resultado: {resultado}")
            return fitness
        except Exception as e:
            logger.error(f"[❌ EVAL] Fallo al evaluar regla: {e}")
            return 0.0

    def _generar_id_regla(self, regla: SymbolicRule) -> str:
        raw = f"{regla.trigger}|{regla.action}|{regla.condicion}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def evolucionar(self, contexto_actual: dict) -> None:
        if not self.enabled:
            return

        print("[⚙️ EVOLUCIÓN] Iniciando ciclo evolutivo...")
        logger.info("Ciclo de evolución simbólica iniciado.")

        reglas_actuales = self.rule_engine.obtener_reglas()
        nuevas_reglas = []
        self.generacion += 1

        for regla in reglas_actuales:
            nueva = deepcopy(regla)
            nueva.condicion = self._mutar_condicion(nueva.condicion)
            nueva_id = self._generar_id_regla(nueva)

            fitness_original = self._evaluar_regla(regla, contexto_actual)
            fitness_mutada = self._evaluar_regla(nueva, contexto_actual)

            if fitness_mutada >= fitness_original:
                nuevas_reglas.append(nueva)
                print(f"[✅ SELECCIÓN] Regla mutada adoptada: {nueva_id}")
                logger.info(f"[EVOLUCION] Generación {self.generacion}: Adoptada regla mutada: {nueva_id}")
            else:
                print(f"[❌ RECHAZO] Regla mutada descartada: {nueva_id}")
                logger.info(f"[DESCARTE] Generación {self.generacion}: Descartada mutación.")

        if nuevas_reglas:
            self.rule_engine.reemplazar_reglas(nuevas_reglas)
            print(f"[🔄 ACTUALIZACIÓN] {len(nuevas_reglas)} reglas simbólicas reemplazadas.")
            logger.info(f"{len(nuevas_reglas)} reglas reemplazadas por versiones mutadas.")
        else:
            print("[⚠️ SIN CAMBIOS] No se generaron mutaciones efectivas.")
            logger.warning("No se aplicaron cambios evolutivos.")
