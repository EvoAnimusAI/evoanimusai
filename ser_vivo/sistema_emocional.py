# sistema_emocional.py :: Módulo simbólico de emociones artificiales (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

import datetime
import traceback

print("[INIT][SISTEMA_EMOCIONAL] >> Cargando sistema emocional (nivel militar)")

class SistemaEmocional:
    def __init__(self):
        print("[BOOT][SISTEMA_EMOCIONAL] >> Sistema emocional simbólico activo")
        self.estado_emocional = {
            "confianza": 0.5,
            "curiosidad": 0.5,
            "alerta": 0.5
        }

    def impactar(self, percepcion):
        timestamp = datetime.datetime.utcnow().isoformat()
        print(f"[EMOCIONES][SISTEMA_EMOCIONAL] >> Procesando percepción: {percepcion}")

        if not isinstance(percepcion, str):
            print("[ERROR][SISTEMA_EMOCIONAL] >> Percepción inválida: se esperaba cadena de texto")
            return {
                "estado": "error",
                "detalle": "percepcion debe ser string",
                "timestamp": timestamp
            }

        try:
            percepcion = percepcion.lower()

            # Lógica simbólica simple para ajuste emocional
            if "peligro" in percepcion or "amenaza" in percepcion:
                self.estado_emocional["alerta"] = min(1.0, self.estado_emocional["alerta"] + 0.1)
                self.estado_emocional["confianza"] = max(0.0, self.estado_emocional["confianza"] - 0.1)
            elif "descubrimiento" in percepcion or "novedad" in percepcion:
                self.estado_emocional["curiosidad"] = min(1.0, self.estado_emocional["curiosidad"] + 0.1)
            elif "logro" in percepcion:
                self.estado_emocional["confianza"] = min(1.0, self.estado_emocional["confianza"] + 0.1)
            else:
                print("[INFO][SISTEMA_EMOCIONAL] >> Percepción neutra, sin ajuste emocional")

            print(f"[ESTADO][SISTEMA_EMOCIONAL] >> Estado emocional actualizado: {self.estado_emocional}")
            return {
                "estado": "ok",
                "emociones": dict(self.estado_emocional),
                "timestamp": timestamp
            }

        except Exception as e:
            print(f"[EXCEPTION][SISTEMA_EMOCIONAL] >> Error durante impacto emocional: {str(e)}")
            traceback.print_exc()
            return {
                "estado": "error",
                "detalle": str(e),
                "timestamp": timestamp
            }
