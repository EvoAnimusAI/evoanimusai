# tools/halt_server.py
# -*- coding: utf-8 -*-
"""
HaltServer — Servidor Web de Visualización de Eventos HALT
Nivel: Cibernético / Auditoría Militar / Trazabilidad Operacional
Expone endpoints HTTP para acceder a eventos HALT en tiempo real,
métricas simbólicas y dashboard visual (/dashboard).
"""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Configuración
HALT_LOG_PATH = Path("logs/halt_events.json")
DASHBOARD_PATH = Path("tools/halt_dashboard.html")
PORT = 8090  # Cambiado de 8080 para evitar conflictos

class HaltRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, code=200, content_type="application/json"):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def _load_data(self):
        if not HALT_LOG_PATH.exists():
            print("[⚠️ HALT_SERVER] Archivo de log HALT no encontrado.")
            return []
        try:
            with open(HALT_LOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"[📤 HALT_SERVER] {len(data)} eventos cargados desde {HALT_LOG_PATH}")
                return data
        except Exception as e:
            print(f"[❌ ERROR] No se pudo cargar el log HALT: {e}")
            return []

    def _generar_resumen(self, eventos):
        resumen = {
            "total_eventos": len(eventos),
            "por_ciclo": {},
            "por_error": [],
            "max_entropia": 0.0,
            "umbral_entropia": 0.75,
            "alertas": []
        }
        for ev in eventos:
            ciclo = ev.get("ciclo", "desconocido")
            resumen["por_ciclo"].setdefault(ciclo, 0)
            resumen["por_ciclo"][ciclo] += 1

            err = ev.get("error_rate", 0)
            resumen["por_error"].append(err)

            ent = ev.get("entropia", 0.0)
            if ent > resumen["max_entropia"]:
                resumen["max_entropia"] = ent
            if ent >= resumen["umbral_entropia"]:
                resumen["alertas"].append({
                    "ciclo": ciclo,
                    "entropia": ent,
                    "mensaje": "⚠️ Entropía elevada"
                })
        return resumen

    def _serve_dashboard(self):
        if DASHBOARD_PATH.exists():
            self._set_headers(200, "text/html")
            with open(DASHBOARD_PATH, "rb") as f:
                self.wfile.write(f.read())
            print("[🌐 HALT_SERVER] Dashboard HTML servido con éxito.")
        else:
            self._set_headers(404, "text/plain")
            mensaje = "Dashboard HTML no encontrado."
            self.wfile.write(mensaje.encode("utf-8"))
            print("[❌ DASHBOARD] halt_dashboard.html no disponible.")

    def do_GET(self):
        print(f"[🌐 REQUEST] Solicitud recibida: {self.path}")
        if self.path in ["/", "/index"]:
            self._set_headers(200, "text/html")
            html = """
            <html><head><title>🛑 HALT Server</title></head>
            <body>
                <h1>🛡️ HALT Server Activo</h1>
                <ul>
                    <li><a href='/halt'>/halt</a> — Eventos HALT JSON</li>
                    <li><a href='/metrics'>/metrics</a> — Métricas resumen</li>
                    <li><a href='/dashboard'>/dashboard</a> — Visualización gráfica</li>
                </ul>
            </body></html>
            """
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/halt":
            eventos = self._load_data()
            self._set_headers()
            self.wfile.write(json.dumps(eventos, indent=4).encode("utf-8"))
        elif self.path == "/metrics":
            eventos = self._load_data()
            resumen = self._generar_resumen(eventos)
            self._set_headers()
            self.wfile.write(json.dumps(resumen, indent=4).encode("utf-8"))
        elif self.path == "/dashboard":
            self._serve_dashboard()
        else:
            self._set_headers(404)
            self.wfile.write(b'{"error": "Ruta no encontrada"}')

def lanzar_servidor():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, HaltRequestHandler)
    print(f"[🌐 HALT_SERVER] Servidor web escuchando en http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("[🧨 HALT_SERVER] Interrupción recibida, cerrando servidor...")
    except Exception as e:
        print(f"[❌ ERROR] Fallo en el servidor: {e}")
    finally:
        httpd.server_close()
        print("[🧨 HALT_SERVER] Servidor detenido.")

# CLI directo
if __name__ == "__main__":
    lanzar_servidor()
