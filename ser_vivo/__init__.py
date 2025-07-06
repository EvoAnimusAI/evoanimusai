# __init__.py :: Núcleo simbiótico de integración (nivel militar)
# Autoriza la carga e inicialización de todos los subsistemas SER_VIVO de EvoAI

import traceback

print("[INIT][SER_VIVO] >> Activando paquete simbiótico SER_VIVO (modo militar)")

try:
    from .conciencia_simulada import ConcienciaSimulada
    from .conciencia_kernel import ConcienciaKernel
    from .sistema_emocional import SistemaEmocional
    from .sistema_memoria import SistemaMemoria
    from .razonamiento_simbolico import Razonador
    from .planificador_autonomo import PlanificadorAutonomo
    from .auto_reflexion import AutoReflexion
    from .funciones_dinamicas import FuncionesDinamicas
    from .evaluador_existencial import EvaluadorExistencial
    from .autoproteccion import AutoProteccion
    from .controlador_entropy import ControladorEntropia
    from .reconstruccion_simbolica import ReconstruccionSimbolica
    from .nucleo_metainteligente import NucleoMetainteligente
    from .gestor_emergencias import GestorEmergencias
    from .generador_pensamiento import GeneradorPensamiento

    print("[OK][SER_VIVO] >> Todos los subsistemas han sido cargados correctamente")

except Exception as e:
    print(f"[ERROR][SER_VIVO] >> Error crítico durante carga de módulos: {str(e)}")
    traceback.print_exc()
    raise RuntimeError("[HALT][SER_VIVO] >> Falla estructural en el subsistema cognitivo")
