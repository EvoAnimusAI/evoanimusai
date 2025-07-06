# controlador_entropy.py :: Módulo de gestión de entropía cognitiva (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

import traceback
import datetime

print("[INIT][CONTROLADOR_ENTROPIA] >> Cargando módulo de control de entropía (nivel militar)")

class ControladorEntropia:
    def __init__(self):
        self.entropia = 0.5  # Valor base neutro
        print(f"[BOOT][CONTROLADOR_ENTROPIA] >> Controlador de entropía activado con nivel inicial: {self.entropia:.2f}")

    def ajustar(self, variacion):
        timestamp = datetime.datetime.utcnow().isoformat()
        print(f"[ADJUST][CONTROLADOR_ENTROPIA] >> Variación solicitada: {variacion}")

        if not isinstance(variacion, (int, float)):
            print("[ERROR][CONTROLADOR_ENTROPIA] >> Tipo de variación no válido")
            return {
                "entropia": self.entropia,
                "error": "variación debe ser numérica",
                "timestamp": timestamp
            }

        try:
            nueva_entropia = self.entropia + variacion
            self.entropia = max(0.0, min(1.0, nueva_entropia))

            print(f"[STATUS][CONTROLADOR_ENTROPIA] >> Nivel de entropía ajustado a: {self.entropia:.4f}")
            return {
                "entropia": self.entropia,
                "timestamp": timestamp
            }

        except Exception as e:
            print(f"[EXCEPTION][CONTROLADOR_ENTROPIA] >> Error al ajustar entropía: {str(e)}")
            traceback.print_exc()
            return {
                "entropia": self.entropia,
                "error": str(e),
                "timestamp": timestamp
            }
