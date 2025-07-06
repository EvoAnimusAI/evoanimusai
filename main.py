# main.py
# Ejecuta ciclo principal de EvoAnimusAI con control heurístico, metacognición y recuperación simbiótica

import time
import random
from core.engine import EvoAIEngine
from ser_vivo.modo_recuperacion import ModoRecuperacion

def generar_contexto_falso(iteracion: int) -> dict:
    """
    Genera un contexto artificial para simular la operación continua de EvoAI.
    Este contexto cambia ligeramente en cada iteración para provocar adaptaciones.
    """
    return {
        "entropy": round(random.uniform(0.0, 1.0), 3),
        "recent_rewards": [random.uniform(-1.0, 1.0) for _ in range(5)],
        "rejected_mutations": random.randint(0, 15),
        "cycles_without_new_rule": random.randint(0, 20),
        "mutation_budget": random.randint(0, 5),
        "error_rate": round(random.uniform(0.0, 1.0), 2),
        "cycle": iteracion,
    }

def main():
    print("[🔧 INIT] Iniciando EvoAnimusAI...")
    engine = EvoAIEngine()
    ciclo = 0

    try:
        while True:
            ciclo += 1
            print(f"\n🔄 [CICLO #{ciclo}] ------------------------------")
            contexto = generar_contexto_falso(ciclo)

            decision = engine.decide(contexto)

            reward = random.uniform(-1.0, 1.0)
            engine.learn(contexto, decision["action"], reward)

            metacog_context = {
                "entropy": contexto["entropy"],
                "current_entropy": contexto["entropy"],
                "recent_rewards": contexto["recent_rewards"],
                "rejected_mutations": contexto["rejected_mutations"],
                "cycles_without_new_rule": contexto["cycles_without_new_rule"],
                "mutation_budget": contexto["mutation_budget"],
                "error_rate": contexto["error_rate"],
            }

            should_stop, reasons = engine.metacog.should_stop(metacog_context)
            if should_stop:
                print(f"🛑 [ALTO] Parada simbólica activada. Razones:")
                for r in reasons:
                    print(f"   ⟶ {r}")

                print("[⚕️] Intentando recuperación simbiótica...")
                recuperador = ModoRecuperacion()
                exito = recuperador.activar_protocolo_revivir(contexto)

                if exito:
                    print("[✅] Recuperación completada. Continuando ciclo...\n")
                    continue
                else:
                    print("[❌] Recuperación no requerida o fallida. Finalizando ejecución.")
                    break

            if engine.metacog.perform_mutation(metacog_context):
                print("🧬 [MUTACIÓN] Mutación dirigida ejecutada.")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[🛑] Interrupción manual recibida. Terminando...")

if __name__ == "__main__":
    main()
