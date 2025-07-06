# gestor_emergencias.py :: Gestor de eventos críticos y emergencias (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

import datetime
import traceback

print("[INIT][GESTOR_EMERGENCIAS] >> Cargando módulo de gestión de emergencias (nivel militar)")

class GestorEmergencias:
    def __init__(self):
        self.estado_alerta = False
        print("[BOOT][GESTOR_EMERGENCIAS] >> Gestor de emergencias operativo")

    def analizar_evento(self, evento):
        timestamp = datetime.datetime.utcnow().isoformat()
        print(f"[ANALISIS][GESTOR_EMERGENCIAS] >> Analizando evento recibido: {evento}")

        if not isinstance(evento, str):
            print("[ERROR][GESTOR_EMERGENCIAS] >> Evento inválido: se esperaba texto")
            return {
                "estado": "error",
                "detalle": "evento no es una cadena de texto",
                "timestamp": timestamp
            }

        try:
            evento_procesado = evento.lower()

            if "halt" in evento_procesado or "crítico" in evento_procesado or "fallo" in evento_procesado:
                self.estado_alerta = True
                print("[EMERG][GESTOR_EMERGENCIAS] >> Emergencia detectada, activando protocolo")
                return {
                    "estado": "protocolo_emergencia",
                    "alerta": True,
                    "evento": evento,
                    "timestamp": timestamp
                }

            print("[OK][GESTOR_EMERGENCIAS] >> Evento controlado, sin activar emergencia")
            return {
                "estado": "normal",
                "alerta": False,
                "evento": evento,
                "timestamp": timestamp
            }

        except Exception as e:
            print(f"[EXCEPTION][GESTOR_EMERGENCIAS] >> Error durante análisis de emergencia: {str(e)}")
            traceback.print_exc()
            return {
                "estado": "error",
                "detalle": str(e),
                "timestamp": timestamp
            }
