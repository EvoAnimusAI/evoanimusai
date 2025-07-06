# mutacion_asistida.py :: Módulo de mutación asistida simbólica (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

import datetime
import random

from .nucleo_metainteligente import NucleoMetainteligente
from symbolic_ai.symbolic_logger import log_event

print("[INIT][MUTACION_ASISTIDA] >> Cargando módulo de mutación asistida simbólica")

class MutacionAsistida:
    def __init__(self):
        self.nucleo = NucleoMetainteligente()
        print("[BOOT][MUTACION_ASISTIDA] >> Módulo operativo")
        log_event({
            "event": "INIT_MUTACION_ASISTIDA",
            "status": "ready",
            "time": datetime.datetime.utcnow().isoformat()
        })

    def evaluar_y_mutar(self, contexto: dict) -> dict:
        print(f"[EVAL][MUTACION_ASISTIDA] >> Evaluando contexto crítico: {contexto}")
        timestamp = datetime.datetime.utcnow().isoformat()

        # Validación defensiva del contexto
        if not isinstance(contexto, dict) or "entropy" not in contexto:
            print("[❌ ERROR][MUTACION_ASISTIDA] >> Contexto inválido o sin datos esenciales")
            return {
                "estado": "error",
                "detalle": "Contexto no válido o incompleto",
                "timestamp": timestamp
            }

        try:
            # Extracción segura de métricas
            entropy = float(contexto.get("entropy", 1.0))
            recent_rewards = contexto.get("recent_rewards", [])
            avg_reward = sum(recent_rewards) / max(1, len(recent_rewards))
            error_rate = float(contexto.get("error_rate", 0.0))
            sin_reglas = int(contexto.get("cycles_without_new_rule", 0))
            mutation_budget = int(contexto.get("mutation_budget", 0))

            # Recuperación de presupuesto si hay estancamiento crítico
            if sin_reglas >= 20 and mutation_budget == 0:
                contexto["mutation_budget"] = 5
                print("[RECOVERY][MUTACION_ASISTIDA] >> Presupuesto restaurado a 5 tras estancamiento crítico")
                log_event({
                    "event": "RECOVERY_BUDGET_RESTORED",
                    "details": f"Restaurado budget=5 por estancamiento (cycles_without_new_rule={sin_reglas})",
                    "time": timestamp
                })

            # Criterios de activación de mutación emergente
            if entropy < 0.5 and avg_reward < 0.1 and error_rate > 0.5 and sin_reglas >= 15:
                print("[TRIGGER][MUTACION_ASISTIDA] >> Criterios cumplidos para mutación emergente")

                nueva_regla = {
                    "rol": "heuristic",
                    "valor": "recuperar_estabilidad",
                    "condicion": f"entropy < {round(entropy + 0.05, 3)} and error_rate > {round(error_rate - 0.1, 3)}",
                    "accion": "reiniciar_loop_aprendizaje",
                    "prioridad": round(random.uniform(0.3, 0.7), 3),
                    "timestamp": timestamp
                }

                reflexion = (
                    f"Entropía baja ({entropy}), recompensa promedio pobre ({avg_reward}), "
                    f"error elevado ({error_rate})"
                )
                plan = "Realizar mutación exploratoria para estabilizar evolución cognitiva"
                firma = self.nucleo.firmar_evento(reflexion, plan)

                resultado = {
                    "estado": "mutacion_activada",
                    "reflexion": reflexion,
                    "plan": plan,
                    "nueva_regla": nueva_regla,
                    "firma": firma,
                    "timestamp": timestamp
                }

                print(f"[✅ MUTACION][MUTACION_ASISTIDA] >> Regla generada: {nueva_regla}")
                log_event({"event": "MUTATION_TRIGGERED", "resultado": resultado})
                return resultado

            # Caso sin cambio
            print("[SKIP][MUTACION_ASISTIDA] >> No se cumplen condiciones para mutación")
            return {
                "estado": "sin_cambio",
                "detalle": "Condiciones no suficientes para mutar",
                "timestamp": timestamp
            }

        except Exception as e:
            print(f"[EXCEPTION][MUTACION_ASISTIDA] >> Error durante evaluación: {str(e)}")
            return {
                "estado": "error",
                "detalle": str(e),
                "timestamp": timestamp
            }
