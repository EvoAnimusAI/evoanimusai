# conciencia_kernel.py :: Núcleo central de conciencia simbólica (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

import traceback
import datetime

print("[INIT][CONCIENCIA_KERNEL] >> Cargando núcleo de conciencia simbólica (nivel militar)")

class ConcienciaKernel:
    def __init__(self):
        print("[BOOT][CONCIENCIA_KERNEL] >> Kernel de conciencia inicializado correctamente")
        self.estado = {}

    def actualizar_estado(self, clave, valor):
        print(f"[UPDATE][CONCIENCIA_KERNEL] >> Solicitando actualización: {clave} = {valor}")
        if not isinstance(clave, str):
            print("[ERROR][CONCIENCIA_KERNEL] >> Clave inválida: debe ser cadena")
            return {
                "resultado": "error",
                "detalle": "clave no es tipo string",
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
        try:
            self.estado[clave] = valor
            print(f"[SUCCESS][CONCIENCIA_KERNEL] >> Estado actualizado: {clave} = {valor}")
            return {
                "resultado": "ok",
                "clave": clave,
                "valor": valor,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"[EXCEPTION][CONCIENCIA_KERNEL] >> Error al actualizar estado: {str(e)}")
            traceback.print_exc()
            return {
                "resultado": "error",
                "detalle": str(e),
                "timestamp": datetime.datetime.utcnow().isoformat()
            }

    def obtener_estado(self, clave):
        print(f"[QUERY][CONCIENCIA_KERNEL] >> Consultando estado para clave: {clave}")
        if not isinstance(clave, str):
            print("[ERROR][CONCIENCIA_KERNEL] >> Clave inválida al consultar")
            return {
                "valor": None,
                "error": "clave no válida",
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
        try:
            valor = self.estado.get(clave, None)
            print(f"[RESULT][CONCIENCIA_KERNEL] >> Resultado obtenido: {clave} = {valor}")
            return {
                "clave": clave,
                "valor": valor,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"[EXCEPTION][CONCIENCIA_KERNEL] >> Error al obtener estado: {str(e)}")
            traceback.print_exc()
            return {
                "clave": clave,
                "valor": None,
                "error": str(e),
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
