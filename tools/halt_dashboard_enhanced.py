from flask import Flask, send_file, jsonify, render_template_string
import json
import os

app = Flask(__name__)
PORT = 8090
EVENTS_FILE = "logs/halt_events.json"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>HALT Dashboard — EvoAI</title>
    <style>
        body { background-color: #111; color: #eee; font-family: monospace; padding: 20px; }
        .alerta { color: orange; font-weight: bold; }
        .critico { color: red; }
        .ok { color: lime; }
        pre { background-color: #222; padding: 10px; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>🛡️ HALT Dashboard Avanzado — <span class="ok">EvoAI</span></h1>
    <p><strong>Fuente:</strong> {{ source }}</p>

    {% if resumen %}
        <h2>📌 Resumen Ejecutivo</h2>
        <ul>
            <li><b>Total de eventos:</b> {{ resumen["total_eventos"] }}</li>
            <li><b>Máxima entropía:</b> {{ resumen["max_entropia"] }}</li>
            <li><b>Umbral crítico:</b> {{ resumen["umbral_critico"] }}</li>
            <li><b>Alertas:</b> {{ resumen["alertas"]|length }}</li>
        </ul>

        <h2>📋 Alertas registradas</h2>
        <ul>
        {% for alerta in resumen["alertas"] %}
            <li class="alerta">⚠️ Ciclo {{ alerta["ciclo"] }} — {{ alerta["mensaje"] }}</li>
        {% endfor %}
        </ul>
    {% endif %}

    <h2>🧬 JSON Completo</h2>
    <pre>{{ raw_json }}</pre>

    <hr>
    <p style="font-size: small;">EvoAI HALT Monitor — Última actualización automática.</p>
</body>
</html>
"""

def cargar_eventos(path):
    if not os.path.exists(path):
        return {"total_eventos": 0, "alertas": [], "max_entropia": 0.0, "umbral_critico": 0.75}, []
    with open(path, "r") as f:
        datos = json.load(f)

    resumen = {
        "total_eventos": len(datos),
        "alertas": [],
        "umbral_critico": 0.75,
        "max_entropia": max((e.get("entropy", 0) for e in datos), default=0.0)
    }

    for evento in datos:
        if evento.get("entropy", 0) > resumen["umbral_critico"]:
            resumen["alertas"].append({
                "ciclo": evento.get("cycle"),
                "entropia": evento.get("entropy"),
                "mensaje": "⚠️ Entropía elevada"
            })

    return resumen, datos

@app.route("/dashboard")
def dashboard():
    resumen, eventos = cargar_eventos(EVENTS_FILE)
    raw_json = json.dumps(eventos, indent=4, ensure_ascii=False)
    return render_template_string(HTML_TEMPLATE, resumen=resumen, raw_json=raw_json, source=EVENTS_FILE)

if __name__ == "__main__":
    print(f"📡 HALT Dashboard Avanzado corriendo en http://0.0.0.0:{PORT}/dashboard")
    app.run(host="0.0.0.0", port=PORT)
