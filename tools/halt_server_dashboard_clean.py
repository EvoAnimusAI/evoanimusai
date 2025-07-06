# -*- coding: utf-8 -*-
""" Dashboard HALT EvoAI - Visualizador web con métricas simbólicas, gráficas dinámicas y herramientas de análisis. """

from flask import Flask, request, Response, jsonify, render_template_string
from datetime import datetime
import json
import os
import logging
import time
import threading
import re
import random

app = Flask(__name__)
logging.basicConfig(filename="logs/halt_dashboard.log", level=logging.INFO)

HALT_JSON_PATH = "logs/halt_events.json"
LOG_PATH = "logs/evoai.log"
SYMBOLIC_LOG_PATH = "logs/symbolic_log.txt"
METACOGNITION_PATH = "logs/system_reset.log"
UPDATE_INTERVAL = 5  # segundos

data_cache = {
    "halt_events": [],
    "halt_count": 0,
    "error_count": 0,
    "system_metrics": [0, 0, 0, 0],
    "timeline": {"labels": [], "data": []},
    "error_distribution": [0, 0, 0, 0],
    "hourly_activity": [0] * 24,
    "last_update": datetime.now()
}

TRUSTED_IPS = {"127.0.0.1", "::1"}

def check_auth(username, password):
    return username == 'admin' and password == 'evoAI2025'

def authenticate():
    return Response(
        "🔐 Autenticación requerida\n",
        401,
        {'WWW-Authenticate': 'Basic realm="EvoAI Halt Dashboard"'}
    )

@app.before_request
def auth_handler():
    ip = request.remote_addr
    if ip not in TRUSTED_IPS:
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()

def procesar_datos_halt():
    try:
        if not os.path.exists(HALT_JSON_PATH):
            return {"eventos": [], "count": 0, "timeline": []}

        with open(HALT_JSON_PATH, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        timeline_data = []
        for evento in datos[-50:]:
            if 'timestamp' in evento and 'entropia' in evento:
                timestamp = evento['timestamp']
                severidad = min(max(round(evento['entropia'] * 10), 1), 10)
                evento['severidad'] = severidad
                timeline_data.append({
                    'timestamp': timestamp,
                    'tipo': evento.get('tipo', 'HALT'),
                    'severidad': severidad
                })

        return {
            "eventos": datos if isinstance(datos, list) else [],
            "count": len(datos) if isinstance(datos, list) else 0,
            "timeline": timeline_data
        }
    except Exception as e:
        logging.error(f"Error procesando datos HALT: {str(e)}")
        return {"eventos": [], "count": 0, "timeline": []}

def analizar_logs():
    try:
        if not os.path.exists(LOG_PATH):
            return {"contadores": {}, "actividad_por_hora": [0]*24, "total_logs": 0}

        with open(LOG_PATH, 'r') as f:
            logs = f.readlines()

        contadores = {"ERROR": 0, "WARNING": 0, "INFO": 0, "CRITICAL": 0}
        actividad_por_hora = [0] * 24

        for linea in logs[-1000:]:
            for nivel in contadores:
                if f"[{nivel}]" in linea:
                    contadores[nivel] += 1
            match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2})', linea)
            if match:
                try:
                    hora = int(match.group(1).split(' ')[1])
                    actividad_por_hora[hora] += 1
                except:
                    pass

        return {
            "contadores": contadores,
            "actividad_por_hora": actividad_por_hora,
            "total_logs": len(logs)
        }
    except Exception as e:
        logging.error(f"Error analizando logs: {str(e)}")
        return {"contadores": {}, "actividad_por_hora": [0]*24, "total_logs": 0}

def generar_metricas_sistema():
    return [random.randint(20, 80), random.randint(30, 90), random.randint(10, 50), random.randint(5, 25)]

def leer_archivo_json(ruta):
    if not os.path.exists(ruta):
        return f"[ERROR] Archivo inexistente: {ruta}"
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = json.load(f)
            return json.dumps(contenido, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"[ERROR] Error leyendo JSON: {str(e)}"

def leer_ultimas_lineas(ruta, n=40):
    if not os.path.exists(ruta):
        return f"[ERROR] Archivo inexistente: {ruta}"
    try:
        with open(ruta, 'r', encoding='utf-8', errors='replace') as f:
            lineas = f.readlines()
            return ''.join(lineas[-n:])
    except Exception as e:
        return f"[ERROR] Error leyendo archivo: {str(e)}"

def actualizar_cache():
    while True:
        try:
            halt_data = procesar_datos_halt()
            log_analysis = analizar_logs()

            timeline_labels = []
            timeline_data = []

            for evento in halt_data["timeline"][-20:]:
                try:
                    timestamp = datetime.fromisoformat(evento['timestamp'].replace('Z', '+00:00'))
                    timeline_labels.append(timestamp.strftime('%H:%M'))
                    timeline_data.append(evento['severidad'])
                except:
                    pass

            data_cache.update({
                'halt_events': halt_data["eventos"],
                'halt_count': halt_data["count"],
                'system_metrics': generar_metricas_sistema(),
                'timeline': {
                    'labels': timeline_labels,
                    'data': timeline_data
                },
                'error_distribution': [
                    log_analysis["contadores"].get("CRITICAL", 0),
                    log_analysis["contadores"].get("ERROR", 0),
                    log_analysis["contadores"].get("WARNING", 0),
                    log_analysis["contadores"].get("INFO", 0)
                ],
                'hourly_activity': log_analysis["actividad_por_hora"],
                'error_count': sum(log_analysis["contadores"].values()),
                'last_update': datetime.now()
            })

            logging.info("✅ Cache actualizado correctamente")

        except Exception as e:
            logging.error(f"❌ Error actualizando cache: {str(e)}")

        time.sleep(UPDATE_INTERVAL)

HTML_TEMPLATE = """[HTML CORREGIDO — ya incluido anteriormente]"""

@app.route("/")
def dashboard():
    try:
        halt_info = leer_archivo_json(HALT_JSON_PATH)
        symbolic_log = leer_ultimas_lineas(SYMBOLIC_LOG_PATH, 30)
        last_logs = leer_ultimas_lineas(LOG_PATH, 30)
        metacognition = leer_ultimas_lineas(METACOGNITION_PATH, 40)
        uptime = f"{int((datetime.now() - data_cache['last_update']).total_seconds() / 3600)}h"

        return render_template_string(HTML_TEMPLATE,
            halt_info=halt_info,
            symbolic_log=symbolic_log,
            last_logs=last_logs,
            metacognition=metacognition,
            halt_count=data_cache.get('halt_count', 0),
            system_status="🟢 OK",
            error_count=data_cache.get('error_count', 0),
            uptime=uptime,
            last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            timeline=data_cache.get('timeline', {})
        )
    except Exception as e:
        logging.error(f"Error en dashboard: {str(e)}")
        return f"<h1>Error en dashboard: {str(e)}</h1>"

@app.route("/api/data")
def api_data():
    return jsonify(data_cache)

if __name__ == "__main__":
    threading.Thread(target=actualizar_cache, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
