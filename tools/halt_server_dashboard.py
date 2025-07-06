# -*- coding: utf-8 -*-
"""
EvoAnimusAI - COMANDO CENTRAL DE VIGILANCIA
Sistema de monitoreo táctico con métricas avanzadas y análisis de amenazas en tiempo real.
"""

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
logging.basicConfig(filename="logs/evoanimusai_command.log", level=logging.INFO)

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
    "last_update": datetime.now(),
    "threat_level": "VERDE",
    "combat_readiness": 95,
    "neural_integrity": 100
}

TRUSTED_IPS = {"127.0.0.1", "::1"}

def check_auth(username, password):
    return username == 'commander' and password == 'EvoAnimus2025'

def authenticate():
    return Response(
        "🔐 ACCESO RESTRINGIDO - AUTORIZACIÓN REQUERIDA\n",
        401,
        {'WWW-Authenticate': 'Basic realm="EvoAnimusAI Command Center"'}
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

        with open(HALT_JSON_PATH, 'r') as f:  # FIXED: Removed extra space
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

def calcular_nivel_amenaza(halt_count, error_count):
    if halt_count > 50 or error_count > 100:
        return "ROJO"
    elif halt_count > 20 or error_count > 50:
        return "AMARILLO"
    else:
        return "VERDE"

def leer_archivo_json(ruta):
    if not os.path.exists(ruta):
        return f"[ERROR] Archivo inexistente: {ruta}"
    try:
        with open(ruta, 'r') as f:
            contenido = json.load(f)
            return json.dumps(contenido, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"[ERROR] Error leyendo JSON: {str(e)}"

def leer_ultimas_lineas(ruta, n=40):
    if not os.path.exists(ruta):
        return f"[ERROR] Archivo inexistente: {ruta}"
    try:
        with open(ruta, 'r') as f:
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

            # Calcular métricas militares
            threat_level = calcular_nivel_amenaza(halt_data["count"], sum(log_analysis["contadores"].values()))
            combat_readiness = max(100 - halt_data["count"], 50)
            neural_integrity = max(100 - log_analysis["contadores"].get("CRITICAL", 0) * 10, 60)

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
                'last_update': datetime.now(),
                'threat_level': threat_level,
                'combat_readiness': combat_readiness,
                'neural_integrity': neural_integrity
            })

            logging.info("✅ COMANDO CENTRAL: Cache actualizado correctamente")

        except Exception as e:
            logging.error(f"❌ COMANDO CENTRAL: Error actualizando cache: {str(e)}")

        time.sleep(UPDATE_INTERVAL)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>⚡ EvoAnimusAI - COMANDO CENTRAL</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #00ff00;
            margin: 0;
            padding: 20px;
            background-attachment: fixed;
        }
        
        .header {
            text-align: center;
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff00;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
        }
        
        .header h1 {
            color: #ff4444;
            font-size: 2.5em;
            text-shadow: 0 0 10px #ff4444;
            margin: 0;
        }
        
        .header h2 {
            color: #00ff00;
            font-size: 1.2em;
            margin: 5px 0;
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .status-card {
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid #00ff00;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
        }
        
        .status-card h3 {
            color: #ffff00;
            margin-top: 0;
            font-size: 1.1em;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #00ff00;
            text-shadow: 0 0 5px #00ff00;
        }
        
        .threat-level {
            font-size: 1.5em;
            font-weight: bold;
            padding: 5px 10px;
            border-radius: 5px;
            text-align: center;
        }
        
        .threat-verde { background-color: #004400; color: #00ff00; }
        .threat-amarillo { background-color: #444400; color: #ffff00; }
        .threat-rojo { background-color: #440000; color: #ff0000; }
        
        .chart-container {
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid #00ff00;
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
        }
        
        .chart-title {
            color: #ffff00;
            font-size: 1.3em;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .log-section {
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff00;
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
        }
        
        .log-section h3 {
            color: #ff4444;
            margin-top: 0;
            font-size: 1.2em;
        }
        
        .log-content {
            background: #000000;
            color: #00ff00;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #333;
        }
        
        .copy-btn {
            background: #ff4444;
            color: #ffffff;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            margin-left: 10px;
        }
        
        .copy-btn:hover {
            background: #ff6666;
        }
        
        .progress-bar {
            background: #333;
            border-radius: 10px;
            padding: 3px;
            margin: 5px 0;
        }
        
        .progress-fill {
            background: linear-gradient(90deg, #00ff00, #ffff00);
            height: 20px;
            border-radius: 7px;
            transition: width 0.5s ease;
        }
        
        .blink {
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0.3; }
        }
    </style>
    <script>
        function copiarContenido() {
            const contenido = document.getElementById('halt_json').innerText;
            navigator.clipboard.writeText(contenido).then(() => {
                alert("📋 DATOS COPIADOS AL PORTAPAPELES");
            }).catch(err => {
                alert("ERROR AL COPIAR: " + err);
            });
        }
        
        // Auto-refresh cada 10 segundos
        setTimeout(() => { location.reload(); }, 10000);
    </script>
</head>
<body>
    <div class="header">
        <h1>⚡ EvoAnimusAI ⚡</h1>
        <h2>COMANDO CENTRAL DE VIGILANCIA NEURAL</h2>
        <div class="blink">🔴 SISTEMA OPERATIVO - MONITOREO ACTIVO</div>
    </div>
    
    <div class="status-grid">
        <div class="status-card">
            <h3>🎯 NIVEL DE AMENAZA</h3>
            <div class="threat-level threat-{{ threat_level.lower() }}">
                {{ threat_level }}
            </div>
        </div>
        
        <div class="status-card">
            <h3>⚔️ PREPARACIÓN COMBATE</h3>
            <div class="metric-value">{{ combat_readiness }}%</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {{ combat_readiness }}%"></div>
            </div>
        </div>
        
        <div class="status-card">
            <h3>🧠 INTEGRIDAD NEURAL</h3>
            <div class="metric-value">{{ neural_integrity }}%</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {{ neural_integrity }}%"></div>
            </div>
        </div>
        
        <div class="status-card">
            <h3>📊 EVENTOS HALT</h3>
            <div class="metric-value">{{ halt_count }}</div>
            <small>Errores: {{ error_count }}</small>
        </div>
    </div>
    
    <div class="chart-container">
        <div class="chart-title">📈 ANÁLISIS TÁCTICO DE SEVERIDAD</div>
        <canvas id="haltChart" width="800" height="300"></canvas>
    </div>
    
    <div class="chart-container">
        <div class="chart-title">🔥 DISTRIBUCIÓN DE AMENAZAS</div>
        <canvas id="threatChart" width="800" height="300"></canvas>
    </div>
    
    <div class="chart-container">
        <div class="chart-title">⏰ ACTIVIDAD HORARIA</div>
        <canvas id="activityChart" width="800" height="300"></canvas>
    </div>
    
    <div class="log-section">
        <h3>📡 LOGS DE SISTEMA</h3>
        <div class="log-content">{{ last_logs }}</div>
    </div>
    
    <div class="log-section">
        <h3>🔮 ANÁLISIS SIMBÓLICO</h3>
        <div class="log-content">{{ symbolic_log }}</div>
    </div>
    
    <div class="log-section">
        <h3>🧬 ESTADO METACOGNITIVO</h3>
        <div class="log-content">{{ metacognition }}</div>
    </div>
    
    <div class="log-section">
        <h3>💾 DATOS HALT JSON <button class="copy-btn" onclick="copiarContenido()">📋 COPIAR</button></h3>
        <div class="log-content" id="halt_json">{{ halt_info }}</div>
    </div>
    
    <div style="text-align: center; margin-top: 30px; color: #666;">
        <p>🕐 Última actualización: {{ last_update }}</p>
        <p>⚡ EvoAnimusAI v2.0 - Sistema de Comando Neural</p>
    </div>

    <script>
        // Gráfico de Severidad HALT
        const ctx1 = document.getElementById('haltChart').getContext('2d');
        new Chart(ctx1, {
            type: 'line',
            data: {
                labels: {{ timeline.labels | safe }},
                datasets: [{
                    label: 'Severidad HALT',
                    data: {{ timeline.data | safe }},
                    borderColor: '#ff4444',
                    backgroundColor: 'rgba(255, 68, 68, 0.2)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#ff4444',
                    pointBorderColor: '#ffffff',
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#00ff00' } }
                },
                scales: {
                    y: { 
                        beginAtZero: true, 
                        max: 10,
                        ticks: { color: '#00ff00' },
                        grid: { color: '#333' }
                    },
                    x: { 
                        ticks: { color: '#00ff00' },
                        grid: { color: '#333' }
                    }
                }
            }
        });
        
        // Gráfico de Distribución de Amenazas
        const ctx2 = document.getElementById('threatChart').getContext('2d');
        new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: ['CRÍTICO', 'ERROR', 'WARNING', 'INFO'],
                datasets: [{
                    data: {{ error_distribution | safe }},
                    backgroundColor: ['#ff0000', '#ff4444', '#ffff00', '#00ff00'],
                    borderColor: '#ffffff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#00ff00' } }
                }
            }
        });
        
        // Gráfico de Actividad Horaria
        const ctx3 = document.getElementById('activityChart').getContext('2d');
        new Chart(ctx3, {
            type: 'bar',
            data: {
                labels: Array.from({length: 24}, (_, i) => i.toString().padStart(2, '0') + ':00'),
                datasets: [{
                    label: 'Actividad',
                    data: {{ hourly_activity | safe }},
                    backgroundColor: 'rgba(0, 255, 0, 0.6)',
                    borderColor: '#00ff00',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#00ff00' } }
                },
                scales: {
                    y: { 
                        ticks: { color: '#00ff00' },
                        grid: { color: '#333' }
                    },
                    x: { 
                        ticks: { color: '#00ff00' },
                        grid: { color: '#333' }
                    }
                }
            }
        });
    </script>
</body>
</html>
"""

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
            error_count=data_cache.get('error_count', 0),
            threat_level=data_cache.get('threat_level', 'VERDE'),
            combat_readiness=data_cache.get('combat_readiness', 95),
            neural_integrity=data_cache.get('neural_integrity', 100),
            uptime=uptime,
            last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            timeline=data_cache.get('timeline', {}),
            error_distribution=data_cache.get('error_distribution', [0, 0, 0, 0]),
            hourly_activity=data_cache.get('hourly_activity', [0] * 24)
        )
    except Exception as e:
        logging.error(f"Error en dashboard: {str(e)}")
        return f"<h1>ERROR EN COMANDO CENTRAL: {str(e)}</h1>"

@app.route("/api/data")
def api_data():
    return jsonify(data_cache)

@app.route("/api/status")
def api_status():
    return jsonify({
        "system": "EvoAnimusAI",
        "status": "OPERATIVO",
        "threat_level": data_cache.get('threat_level', 'VERDE'),
        "combat_readiness": data_cache.get('combat_readiness', 95),
        "neural_integrity": data_cache.get('neural_integrity', 100),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    print("🚀 INICIANDO EvoAnimusAI - COMANDO CENTRAL")
    print("🔥 Sistema de Vigilancia Neural Activado")
    print("⚡ Acceso: http://localhost:8080")
    print("🔐 Usuario: commander | Contraseña: EvoAnimus2025")
    
    threading.Thread(target=actualizar_cache, daemon=True).start()
    app.run(host="0.0.0.0", port=8080, debug=False)
