# autoproteccion.py :: Módulo de autoprotección simbólica (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

import traceback
import datetime

print("[INIT][AUTOPROTECCION] >> Cargando módulo de autoprotección (nivel militar)")

class AutoProteccion:
    def __init__(self):
        print("[BOOT][AUTOPROTECCION] >> Inicializando sistema de autoprotección")

    def evaluar_riesgo(self, entrada):
        print(f"[EVAL][AUTOPROTECCION] >> Evaluando posible riesgo en entrada: {entrada}")
        
        if not isinstance(entrada, str):
            print("[ERROR][AUTOPROTECCION] >> Entrada inválida: se esperaba string")
            return {
                "estado": "error",
                "detalle": "entrada no es una cadena de texto",
                "timestamp": datetime.datetime.utcnow().isoformat()
            }

        try:
            entrada_procesada = entrada.lower()
            print(f"[DATA][AUTOPROTECCION] >> Entrada procesada: {entrada_procesada}")

            if "error" in entrada_procesada or "amenaza" in entrada_procesada or "intrusion" in entrada_procesada:
                print("[ALERT][AUTOPROTECCION] >> Riesgo detectado: activando defensa simbólica")
                return {
                    "estado": "defensa_activada",
                    "nivel": "alto",
                    "timestamp": datetime.datetime.utcnow().isoformat()
                }

            print("[OK][AUTOPROTECCION] >> Evaluación completada: sin amenaza detectada")
            return {
                "estado": "sin_amenaza",
                "nivel": "bajo",
                "timestamp": datetime.datetime.utcnow().isoformat()
            }

        except Exception as e:
            print(f"[EXCEPTION][AUTOPROTECCION] >> Error en la evaluación de riesgo: {str(e)}")
            traceback.print_exc()
            return {
                "estado": "error",
                "detalle": str(e),
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
