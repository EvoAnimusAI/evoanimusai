# symbolic_ai/mutation_trigger.py
# -*- coding: utf-8 -*-
"""
Módulo de activación automática de mutaciones simbólicas en EvoAnimusAI.
Clasificación: Militar / Gubernamental / Ultra-secreto

Responsabilidades:
- Ejecutar mutaciones simbólicas seguras.
- Validar condiciones críticas (entropy, ciclos, anomalías).
- Registrar auditoría de mutación.
- Reutilizable desde cualquier subsistema.
"""

import logging
from core.context import EvoContext
from symbolic_ai.hypermutator import mutate_complete_function

logger = logging.getLogger("EvoAI.MutationTrigger")

class MutationTrigger:
    """
    Activador automático de mutaciones simbólicas controladas.
    Permite evaluación condicional, disparo forzado y trazabilidad total.
    """

    def __init__(self, threshold_entropy: float = 0.85, max_idle_cycles: int = 5):
        self.threshold_entropy = threshold_entropy
        self.max_idle_cycles = max_idle_cycles

    def trigger(self, context: EvoContext, reason: str = "auto", force: bool = False) -> bool:
        """
        Ejecuta mutación automática segura si se cumplen condiciones críticas o si se fuerza.

        Args:
            context (EvoContext): contexto simbólico completo del sistema.
            reason (str): razón por la cual se solicita la mutación.
            force (bool): si es True, ejecuta sin validaciones.

        Returns:
            bool: True si se mutó exitosamente, False en caso contrario.
        """
        if not force and not self._should_trigger(context):
            logger.debug(f"[MutationTrigger] ❎ Condiciones no cumplen para mutación automática. Razón: {reason}")
            return False

        try:
            success = mutate_complete_function(context)
            if success:
                logger.info(f"[MutationTrigger] ✅ Mutación simbólica activada automáticamente. Razón: {reason}")
            else:
                logger.warning(f"[MutationTrigger] ⚠️ Mutación ejecutada pero sin cambios funcionales.")
            return success
        except Exception as e:
            logger.critical(f"[MutationTrigger] 🛑 Error crítico en mutación automática: {e}", exc_info=True)
            return False

    def _should_trigger(self, context: EvoContext) -> bool:
        """
        Evalúa si se deben activar mutaciones simbólicas automáticamente.

        Criterios (configurables):
        - Entropía simbólica elevada.
        - Número de ciclos sin avance (idle).

        Returns:
            bool: True si deben activarse mutaciones.
        """
        entropy = context.get("entropy", 0.0)
        idle_cycles = context.get("idle_cycles", 0)

        if entropy >= self.threshold_entropy:
            logger.info(f"[MutationTrigger] Entropía alta detectada: {entropy}")
            return True

        if idle_cycles >= self.max_idle_cycles:
            logger.info(f"[MutationTrigger] Ciclos inactivos excedidos: {idle_cycles}")
            return True

        return False
