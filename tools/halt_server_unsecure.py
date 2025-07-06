# -*- coding: utf-8 -*-
"""
HALT Dashboard HTTP sin seguridad — Solo para desarrollo local
"""
from flask import Flask, jsonify
import logging
import os
import json

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Ruta del archivo de historial de HALT
HALT_HISTORY_PATH = "logs/halt_history_export.json"

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if not os.path.exists(HALT_HISTORY_PATH):
        return jsonify({"error": "Archivo de historial no encontrado"}), 404
    try:
        with open(HALT_HISTORY_PATH, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        logging.error(f"[ERROR] Falló lectura de historial: {e}")
        return jsonify({"error": "Error al procesar historial"}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({"mensaje": "🛡️ HALT Dashboard disponible en /dashboard"})

if __name__ == '__main__':
    print("🚨 HALT Dashboard HTTP sin seguridad disponible en: http://0.0.0.0:8080/dashboard")
    app.run(host='0.0.0.0', port=8080)
