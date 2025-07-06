# analizador_semantico.py :: Módulo simbólico de análisis semántico (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

import datetime
import traceback

print("[INIT][ANALIZADOR_SEMANTICO] >> Cargando módulo de análisis semántico (nivel militar)")

class AnalizadorSemantico:
    def __init__(self):
        print("[BOOT][ANALIZADOR_SEMANTICO] >> Analizador semántico operativo (nivel militar)")

    def analizar(self, entrada):
        timestamp = datetime.datetime.utcnow().isoformat()
        print(f"[ANALISIS][ANALIZADOR_SEMANTICO] >> Entrada recibida: {entrada}")

        if not isinstance(entrada, str):
            print("[ERROR][ANALIZADOR_SEMANTICO] >> Entrada inválida: se esperaba string")
            return {
                "estado": "error",
                "detalle": "entrada debe ser string",
                "timestamp": timestamp
            }

        try:
            entrada_lower = entrada.lower()

            if any(palabra in entrada_lower for palabra in ["amenaza", "peligro", "riesgo", "hostil"]):
                conclusion = "riesgo_detectado"
            elif any(palabra in entrada_lower for palabra in ["oportunidad", "avance", "mejora"]):
                conclusion = "condicion_positiva"
            else:
                conclusion = "neutral"

            resultado = {
                "estado": "ok",
                "diagnostico": conclusion,
                "entrada_original": entrada,
                "timestamp": timestamp
            }

            print(f"[RESULTADO][ANALIZADOR_SEMANTICO] >> Diagnóstico semántico: {resultado}")
            return resultado

        except Exception as e:
            print(f"[EXCEPTION][ANALIZADOR_SEMANTICO] >> Error crítico en análisis: {str(e)}")
            traceback.print_exc()
            return {
                "estado": "error",
                "detalle": str(e),
                "timestamp": timestamp
            }
