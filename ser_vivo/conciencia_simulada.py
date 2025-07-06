# conciencia_simulada.py :: Simulación de conciencia artificial (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

import traceback
import datetime

print("[INIT][CONCIENCIA_SIMULADA] >> Cargando módulo de conciencia simulada (nivel militar)")

from .conciencia_kernel import ConcienciaKernel
from .sistema_emocional import SistemaEmocional
from .sistema_memoria import SistemaMemoria
from .razonamiento_simbolico import Razonador
from .auto_reflexion import AutoReflexion
from .funciones_dinamicas import FuncionesDinamicas
from .planificador_autonomo import PlanificadorAutonomo
from .mutacion_asistida import MutacionAsistida


class ConcienciaSimulada:
    def __init__(self):
        print("[BOOT][CONCIENCIA_SIMULADA] >> Inicializando ConcienciaSimulada")
        self.kernel = ConcienciaKernel()
        self.emociones = SistemaEmocional()
        self.memoria = SistemaMemoria()
        self.razonador = Razonador()
        self.reflexion = AutoReflexion()
        self.programador = FuncionesDinamicas()
        self.planificador = PlanificadorAutonomo()
        self.mutador = MutacionAsistida()
        self.contexto_simbólico_actual = None  # Contexto persistente interno

    def ciclo(self, entrada):
        print(f"[CICLO][CONCIENCIA_SIMULADA] >> Procesando entrada: {entrada}")
        timestamp = datetime.datetime.utcnow().isoformat()

        try:
            # Validación y fallback de entrada
            if entrada is None or not isinstance(entrada, dict):
                entrada = self.contexto_simbólico_actual
                if entrada is None:
                    print("[ERROR][CONCIENCIA_SIMULADA] >> Entrada nula y sin contexto simbólico almacenado")
                    return {
                        "estado": "error",
                        "detalle": "entrada no válida",
                        "timestamp": timestamp
                    }

            # Si la entrada contiene claves simbólicas, la almacenamos como estado actual
            if isinstance(entrada, dict) and "entropy" in entrada:
                self.contexto_simbólico_actual = entrada

            percepcion = self.memoria.percibir(entrada)
            print(f"[PERCEPCION][CONCIENCIA_SIMULADA] >> {percepcion}")

            emociones = self.emociones.impactar(percepcion)
            print(f"[EMOCIONES][CONCIENCIA_SIMULADA] >> {emociones}")

            razonamiento = self.razonador.analizar(percepcion)
            print(f"[RAZONAMIENTO][CONCIENCIA_SIMULADA] >> {razonamiento}")

            reflexion = self.reflexion.evaluar(razonamiento, emociones)
            print(f"[REFLEXION][CONCIENCIA_SIMULADA] >> {reflexion}")

            resultado_prog = self.programador.actualizar(reflexion)
            print(f"[AUTO_PROG][CONCIENCIA_SIMULADA] >> Resultado: {resultado_prog}")

            decision = self.planificador.decidir(reflexion)
            print(f"[DECISION][CONCIENCIA_SIMULADA] >> {decision}")

            # Evaluar contexto simbólico para mutación
            if not self.contexto_simbólico_actual or "entropy" not in self.contexto_simbólico_actual:
                print("[WARN][CONCIENCIA_SIMULADA] >> Contexto simbólico no definido o inválido para mutación")
                mutacion_resultado = {
                    "estado": "sin_cambio",
                    "detalle": "Contexto simbólico no disponible",
                    "timestamp": timestamp
                }
            else:
                mutacion_resultado = self.mutador.evaluar_y_mutar(self.contexto_simbólico_actual)
                print(f"[MUTACION][CONCIENCIA_SIMULADA] >> {mutacion_resultado}")

            print("[CICLO][CONCIENCIA_SIMULADA] >> Ciclo completo")

            return {
                "estado": "ok",
                "timestamp": timestamp,
                "decision": decision,
                "mutacion": mutacion_resultado
            }

        except Exception as e:
            print(f"[EXCEPTION][CONCIENCIA_SIMULADA] >> Error crítico durante el ciclo: {str(e)}")
            traceback.print_exc()
            return {
                "estado": "error",
                "detalle": str(e),
                "timestamp": timestamp
            }

    def activar(self):
        print("[ACTIVAR][CONCIENCIA_SIMULADA] >> Activando sistema de conciencia simbólica")
        return {
            "estado": "activo",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

    def procesar_entrada(self, entrada):
        print("[CALL][CONCIENCIA_SIMULADA] >> Redirigiendo a ciclo() desde procesar_entrada()")
        return self.ciclo(entrada)

    def boot(self):
        print("[BOOT][CONCIENCIA_SIMULADA] >> Ejecutando rutina boot() de ConcienciaSimulada")
        try:
            self.activar()
            self.memoria.inicializar()
            self.emociones.inicializar()
            self.kernel.inicializar()
            self.razonador.inicializar()
            self.reflexion.inicializar()
            self.programador.inicializar()
            self.planificador.inicializar()
            self.mutador.inicializar()
            print("[BOOT][CONCIENCIA_SIMULADA] >> Sistema completamente inicializado (nivel militar)")
        except Exception as e:
            print(f"[❌ ERROR][CONCIENCIA_SIMULADA] >> Fallo en boot(): {str(e)}")
            traceback.print_exc()
