# nucleo_metainteligente.py :: Núcleo de metainteligencia simbólica (nivel militar)
# Parte del subsistema SER_VIVO de EvoAI

import datetime
import traceback
import hashlib

print("[INIT][NUCLEO_METAINTELIGENTE] >> Cargando núcleo metainteligente (nivel militar)")

class NucleoMetainteligente:
    def __init__(self):
        print("[BOOT][NUCLEO_METAINTELIGENTE] >> Núcleo metainteligente inicializado correctamente")

    def generar_checksum(self, datos: str) -> str:
        checksum = hashlib.sha256(datos.encode("utf-8")).hexdigest()
        print(f"[CHECKSUM][NUCLEO_METAINTELIGENTE] >> Checksum generado: {checksum[:10]}...")
        return checksum

    def firmar_evento(self, reflexion: str, plan: str) -> str:
        timestamp = datetime.datetime.utcnow().isoformat()
        firma = f"{timestamp}|{reflexion}|{plan}"
        return self.generar_checksum(firma)

    def clasificar_estrategia(self, plan: str) -> str:
        plan = plan.lower()
        if any(k in plan for k in ["anticipar", "prevenir", "explorar", "expansión"]):
            print("[STRATEGY][PROACTIVA] >> Plan clasificado como estrategia proactiva")
            return "proactiva"
        elif any(k in plan for k in ["responder", "contener", "mitigar", "defensa"]):
            print("[STRATEGY][REACTIVA] >> Plan clasificado como estrategia reactiva")
            return "reactiva"
        else:
            print("[STRATEGY][DESCONOCIDA] >> Estrategia no clasificada")
            return "desconocida"

    def detectar_contradicciones(self, reflexion: str, plan: str) -> bool:
        reflexion_lower = reflexion.lower()
        plan_lower = plan.lower()
        if "detener" in reflexion_lower and "expansión" in plan_lower:
            print("[CONFLICTO] >> Contradicción detectada: reflexión pide detener, plan propone expansión")
            return True
        if "riesgo" in reflexion_lower and "avanzar" in plan_lower:
            print("[CONFLICTO] >> Contradicción detectada: riesgo detectado pero el plan avanza")
            return True
        print("[CHECK] >> No se detectan contradicciones entre reflexión y plan")
        return False

    def coordinar(self, reflexion, plan):
        timestamp = datetime.datetime.utcnow().isoformat()
        print("[COORD][NUCLEO_METAINTELIGENTE] >> Evaluando coordinación entre reflexión y plan")

        if not isinstance(reflexion, str) or not isinstance(plan, str):
            print("[ERROR][NUCLEO_METAINTELIGENTE] >> Entradas inválidas: se esperaban cadenas de texto")
            return {
                "estado": "error",
                "detalle": "reflexion y plan deben ser strings",
                "timestamp": timestamp
            }

        try:
            firma = self.firmar_evento(reflexion, plan)
            tipo_estrategia = self.clasificar_estrategia(plan)
            conflicto = self.detectar_contradicciones(reflexion, plan)
            if conflicto:
                return {
                    "estado": "conflicto_detectado",
                    "detalle": "Contradicción lógica entre reflexión y plan",
                    "reflexion": reflexion,
                    "plan": plan,
                    "estrategia": tipo_estrategia,
                    "firma": firma,
                    "timestamp": timestamp
                }

            if "mejora" in reflexion.lower() and "adaptacion" in plan.lower():
                print("[STRATEGY][ADAPTATIVA] >> Activando protocolo de mejora adaptativa")
                return {
                    "estado": "plan_mejora_adaptativa_activado",
                    "reflexion": reflexion,
                    "plan": plan,
                    "estrategia": tipo_estrategia,
                    "firma": firma,
                    "timestamp": timestamp
                }

            if "mejora" in reflexion.lower():
                print("[STRATEGY][MEJORA] >> Planeando acciones de mejora continua")
                return {
                    "estado": "plan_mejora_activado",
                    "reflexion": reflexion,
                    "plan": plan,
                    "estrategia": tipo_estrategia,
                    "firma": firma,
                    "timestamp": timestamp
                }

            print("[HOLD][NUCLEO_METAINTELIGENTE] >> No se requiere ajuste cognitivo")
            return {
                "estado": "sin_accion",
                "reflexion": reflexion,
                "plan": plan,
                "estrategia": tipo_estrategia,
                "firma": firma,
                "timestamp": timestamp
            }

        except Exception as e:
            print(f"[EXCEPTION][NUCLEO_METAINTELIGENTE] >> Error durante coordinación: {str(e)}")
            traceback.print_exc()
            return {
                "estado": "error",
                "detalle": str(e),
                "timestamp": timestamp
            }

    def reinicializar(self, datos: dict) -> dict:
        timestamp = datetime.datetime.utcnow().isoformat()
        print(f"[REBOOT][NUCLEO_METAINTELIGENTE] >> Reinicializando entorno cognitivo con datos: {datos}")

        try:
            evento = datos.get("evento", "desconocido")
            ciclo = datos.get("ciclo", -1)
            entropia = datos.get("entropy", 0.0)
            recompensa_promedio = datos.get("avg_reward", 0.0)

            print(f"[REBOOT][NUCLEO_METAINTELIGENTE] >> Evento: {evento} | Ciclo: {ciclo} | Entropía: {entropia} | Avg Recompensa: {recompensa_promedio}")

            if "HALT" in evento and "stagnation" in evento.lower():
                print("[DETECCION] >> Estancamiento evolutivo detectado.")
                if entropia < 0.6 and recompensa_promedio < 0.2:
                    nueva_regla = {
                        "role": "contexto",
                        "value": "anómalo",
                        "action": "explorar",
                        "condition": "entropy < 0.6 and error_rate > 0.5",
                        "priority": 0.9
                    }
                    print(f"[MUTACION][NUCLEO_METAINTELIGENTE] >> Generando regla exploratoria: {nueva_regla}")
                    return {
                        "estado": "mutacion_activada",
                        "evento": evento,
                        "ciclo": ciclo,
                        "nueva_regla": nueva_regla,
                        "timestamp": timestamp
                    }

            return {
                "estado": "reinicializado",
                "evento": evento,
                "ciclo": ciclo,
                "timestamp": timestamp
            }

        except Exception as e:
            print(f"[EXCEPTION][NUCLEO_METAINTELIGENTE] >> Fallo durante reinicialización: {e}")
            return {
                "estado": "error",
                "detalle": str(e),
                "timestamp": timestamp
            }
