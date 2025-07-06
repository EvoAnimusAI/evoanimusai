def obtener_metricas_halt():
    return {
        "total_eventos": 1,
        "max_entropia": 0.89,
        "por_error": [0.7],
        "por_ciclo": {44: 1},
        "alertas": [{"ciclo": 44, "entropia": 0.89, "mensaje": "⚠️ Entropía elevada"}],
        "umbral_entropia": 0.75
    }
