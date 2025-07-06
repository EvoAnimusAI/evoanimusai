# planificador_autonomo.py :: Módulo de planificación simbólica autónoma (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

import datetime
import traceback

print("[INIT][PLANIFICADOR_AUTONOMO] >> Cargando planificador autónomo (nivel militar)")

class PlanificadorAutonomo:
    def __init__(self):
        print("[BOOT][PLANIFICADOR_AUTONOMO] >> Planificador en modo autónomo activo")

    def decidir(self, reflexion):
        timestamp = datetime.datetime.utcnow().isoformat()
        print(f"[DECISION][PLANIFICADOR_AUTONOMO] >> Tomando decisión basada en reflexión: {reflexion}")

        if not isinstance(reflexion, dict):
            print("[ERROR][PLANIFICADOR_AUTONOMO] >> Reflexión inválida: se esperaba dict")
            return {
                "estado": "error",
                "detalle": "reflexion debe ser un diccionario simbólico",
                "timestamp": timestamp
            }

        try:
            contenido = reflexion.get("reflexion", "").lower()

            if "estabilidad" in contenido:
                print("[ACTION][PLANIFICADOR_AUTONOMO] >> Priorizando estabilidad cognitiva")
                return {
                    "estado": "accion_estabilidad",
                    "accion": "mantener_estado_actual",
                    "timestamp": timestamp
                }

            if "adaptacion" in contenido or "cambio" in contenido:
                print("[ACTION][PLANIFICADOR_AUTONOMO] >> Activando plan de adaptación")
                return {
                    "estado": "accion_adaptativa",
                    "accion": "reconfigurar_sistema",
                    "timestamp": timestamp
                }

            print("[DEFAULT][PLANIFICADOR_AUTONOMO] >> Reflexión no crítica, manteniendo curso")
            return {
                "estado": "sin_cambio",
                "accion": "continuar",
                "timestamp": timestamp
            }

        except Exception as e:
            print(f"[EXCEPTION][PLANIFICADOR_AUTONOMO] >> Error durante decisión: {str(e)}")
            traceback.print_exc()
            return {
                "estado": "error",
                "detalle": str(e),
                "timestamp": timestamp
            }
