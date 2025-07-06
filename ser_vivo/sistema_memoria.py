# sistema_memoria.py :: Subsistema simbólico de memoria perceptiva (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

import datetime
import traceback

print("[INIT][SISTEMA_MEMORIA] >> Cargando sistema de memoria (nivel militar)")

class SistemaMemoria:
    def __init__(self):
        print("[BOOT][SISTEMA_MEMORIA] >> Memoria simbólica inicializada")
        self.buffer = []

    def percibir(self, entrada):
        timestamp = datetime.datetime.utcnow().isoformat()
        print(f"[PERCEPCION][SISTEMA_MEMORIA] >> Procesando entrada: {entrada}")

        if not isinstance(entrada, str):
            print("[ERROR][SISTEMA_MEMORIA] >> Entrada inválida: se esperaba cadena de texto")
            return "ERROR: entrada debe ser string"

        try:
            self.buffer.append({
                "contenido": entrada,
                "timestamp": timestamp
            })
            print(f"[BUFFER][SISTEMA_MEMORIA] >> Entrada almacenada: {entrada}")
            return entrada  # <-- DEVOLVER SOLO STRING

        except Exception as e:
            print(f"[EXCEPTION][SISTEMA_MEMORIA] >> Error al almacenar percepción: {str(e)}")
            traceback.print_exc()
            return "ERROR: excepción en almacenamiento"
