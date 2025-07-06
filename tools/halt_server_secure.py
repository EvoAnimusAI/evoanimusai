# tools/halt_server_secure.py
# -*- coding: utf-8 -*-
"""
Servidor HTTPS Seguro para visualizar eventos HALT — Nivel Militar

Expone los archivos HTML y métricas simbólicas HALT de forma cifrada y autenticada.
"""

from flask import Flask, send_file, jsonify, request, abort
import ssl
import json
import os
import logging

# === CONFIGURACIÓN SEGURA ===
HALT_LOG = "logs/halt_events.json"
DASHBOARD = "tools/halt_dashboard.html"
AUTH_TOKEN = "TOKEN-MILITAR-ULTRASECRETO-001"  # 🔐 Cambiar para despliegue real

# === INICIALIZACIÓN FLASK ===
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# === VERIFICACIÓN DE TOKEN ===
def validar_token(req):
    token = req.headers.get("Authorization")
    if token != f"Bearer {AUTH_TOKEN}":
        logging.warning(f"[INTENTO FALLIDO] Token no válido recibido: {token}")
        abort(403, description="🔒 Acceso denegado: Token inválido")

@app.route("/")
@app.route("/dashboard")
def dashboard():
    validar_token(request)
    if not os.path.isfile(DASHBOARD):
        abort(500, description="Dashboard no disponible")
    return send_file(DASHBOARD)

@app.route("/metrics")
def metrics():
    validar_token(request)
    if not os.path.isfile(HALT_LOG):
        return jsonify({"error": "No hay datos HALT"}), 404

    with open(HALT_LOG, "r") as f:
        eventos = json.load(f)

    total = len(eventos)
    por_ciclo = {}
    por_error = []
    max_entropia = 0
    umbral_entropia = 0.75
    alertas = []

    for e in eventos:
        ciclo = e.get("ciclo", "desconocido")
        por_ciclo[str(ciclo)] = por_ciclo.get(str(ciclo), 0) + 1
        if e.get("error_rate") is not None:
            por_error.append(e["error_rate"])
        if e.get("entropia", 0) > max_entropia:
            max_entropia = e["entropia"]
        if e.get("entropia", 0) > umbral_entropia:
            alertas.append({
                "ciclo": e["ciclo"],
                "entropia": e["entropia"],
                "mensaje": "⚠️ Entropía elevada"
            })

    return jsonify({
        "total_eventos": total,
        "por_ciclo": por_ciclo,
        "por_error": por_error,
        "max_entropia": max_entropia,
        "umbral_entropia": umbral_entropia,
        "alertas": alertas
    })

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('certs/server.crt', 'certs/server.key')
    print("🚨 HALT Dashboard HTTPS seguro disponible en:")
    print("     ➤ https://localhost:8443/dashboard")
    print("     ➤ Requiere header: Authorization: Bearer TOKEN-MILITAR-ULTRASECRETO-001")
    app.run(host="0.0.0.0", port=8443, ssl_context=context)
