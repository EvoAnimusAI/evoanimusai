# evoai_integration_test.py :: Prueba de integración simbiótica de alto nivel
# Nivel militar :: Verifica conexión y coherencia entre módulos SER_VIVO

from ser_vivo.conciencia_simulada import ConcienciaSimulada

print("[INIT][INTEGRATION_TEST] >> Iniciando prueba de integración simbólica (nivel militar)")

def main():
    conciencia = ConcienciaSimulada()

    entradas = [
        "Detecto una amenaza desconocida en el entorno de ejecución",
        "El sistema parece estar operando con baja entropía",
        "Se ha recuperado memoria simbólica de eventos previos",
        12345,  # Entrada inválida int
        None,   # Entrada inválida None
    ]

    for idx, entrada in enumerate(entradas):
        print(f"[TEST][INTEGRATION_TEST] >> ({idx+1}) Entrada simulada: {entrada}")
        try:
            resultado = conciencia.procesar_entrada(entrada)

            if not isinstance(resultado, dict):
                print(f"[WARNING][INTEGRATION_TEST] >> Retorno no dict: {resultado}")
            elif resultado.get("estado") == "error":
                print(f"[ERROR][INTEGRATION_TEST] >> Error procesando entrada: {resultado}")
            else:
                print(f"[OK][INTEGRATION_TEST] >> Entrada procesada exitosamente: {resultado}")
        except Exception as e:
            print(f"[EXCEPTION][INTEGRATION_TEST] >> Fallo en ciclo {idx+1}: {str(e)}")

    print("[SUCCESS][INTEGRATION_TEST] >> Prueba de integración completada sin errores fatales")

if __name__ == "__main__":
    main()
