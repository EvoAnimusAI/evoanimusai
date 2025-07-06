# razonamiento_simbolico.py :: Módulo de razonamiento simbólico (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

print("[INIT][RAZONAMIENTO_SIMBOLICO] >> Cargando módulo de razonamiento simbólico (nivel militar)")

class Razonador:
    def __init__(self):
        print("[BOOT][RAZONADOR] >> Razonador simbólico inicializado")

    def analizar(self, entrada):
        print(f"[ANALISIS][RAZONADOR] >> Analizando entrada: {entrada}")
        if not isinstance(entrada, str):
            print("[ERROR][RAZONADOR] >> Tipo de percepción no válida (se esperaba string)")
            return {
                "estado": "error",
                "detalle": "percepcion no es string"
            }

        if "amenaza" in entrada.lower():
            conclusion = "riesgo_detectado"
        elif "error" in entrada.lower():
            conclusion = "anomalía_detectada"
        elif "oportunidad" in entrada.lower():
            conclusion = "oportunidad_detectada"
        else:
            conclusion = "sin_riesgo"

        resultado = {
            "estado": "ok",
            "conclusion": conclusion,
            "entrada": entrada
        }

        print(f"[RESULTADO][RAZONADOR] >> Conclusión: {conclusion}")
        return resultado
