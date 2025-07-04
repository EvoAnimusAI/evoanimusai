# symbolic_ai/cond_error.py
# -*- coding: utf-8 -*-
"""
CondErrorHandler — Evaluación Segura de Condiciones Simbólicas
Nivel: Militar / Gubernamental / Infraestructura Crítica

Funciones:
- Evaluación de expresiones condicionales simbólicas de forma segura.
- Aplicación de valores por defecto para variables ausentes o nulas.
- Prevención de fallos por NameError o TypeError.
- Instrumentación tipo printf: seguimiento, trazabilidad y control total.
"""

import logging
from typing import Optional, Dict

logger = logging.getLogger("CondErrorHandler")

class CondErrorHandler:
    def __init__(self, fallback_values: Optional[Dict[str, object]] = None):
        self.fallback_values = fallback_values or {}
        print("\n[🔧 INIT] CondErrorHandler inicializado.")
        print(f"[🔧 INIT] Fallbacks definidos: {self.fallback_values}")

    def safe_eval_condition(self, condition: str, context: dict) -> bool:
        print("\n" + "=" * 80)
        print(f"[🚦 STEP 1] Evaluando condición: {repr(condition)}")
        print(f"[📥 STEP 2] Contexto original recibido:")
        for k, v in context.items():
            print(f"    • {k} = {v}")

        # Copiar contexto para evitar modificación in situ
        safe_context = context.copy()

        print(f"[🔍 STEP 3] Verificando variables faltantes con fallback:")
        for var, default in self.fallback_values.items():
            if safe_context.get(var) is None:
                safe_context[var] = default
                fallback_msg = f"[🛡️ FALLBACK] Variable '{var}' no definida o es None → asignado: {default}"
                logger.warning(fallback_msg)
                print(fallback_msg)

        print(f"[📦 STEP 4] Contexto final para evaluación:")
        for k, v in safe_context.items():
            print(f"    • {k} = {v}")

        print(f"[🧪 STEP 5] Ejecutando 'eval' segura...")
        try:
            result = eval(condition, {}, safe_context)
            print(f"[✅ STEP 6] Resultado crudo: {result}")
            print(f"[🟢 STEP 7] Resultado booleano final: {bool(result)}")
            return bool(result)

        except NameError as e:
            error_msg = f"[❌ NAME ERROR] '{condition}' — {e}"
            logger.error(error_msg)
            print(error_msg)
            return False

        except TypeError as e:
            type_error_msg = f"[⚠️ TYPE ERROR] '{condition}' — {e}"
            logger.warning(type_error_msg)
            print(type_error_msg)
            return False

        except Exception as e:
            generic_msg = f"[🔥 UNEXPECTED ERROR] Evaluando '{condition}': {e}"
            logger.error(generic_msg)
            print(generic_msg)
            return False
