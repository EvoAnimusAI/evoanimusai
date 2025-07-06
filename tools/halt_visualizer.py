# tools/halt_visualizer.py
# -*- coding: utf-8 -*-
"""
HaltVisualizer — Visualizador y exportador de eventos HALT
Nivel: Cibernético / Auditoría Militar / Trazabilidad Visual y JSON
"""

import datetime
import json
import os
import matplotlib.pyplot as plt
from pathlib import Path
import logging

logger = logging.getLogger("HaltVisualizer")

class HaltVisualizer:
    def __init__(self, log_path="logs/halt_events.json"):
        self.historial = []
        self.log_path = Path(log_path)
        self.export_path = Path("logs/halt_history_export.json")
        os.makedirs(self.log_path.parent, exist_ok=True)
        self._cargar_log_existente()

        if self.historial:
            self.generar_graficos()

    def registrar_evento(self, contexto: dict):
        timestamp = datetime.datetime.utcnow().isoformat()
        entrada = {
            "timestamp": timestamp,
            "ciclo": contexto.get("cycle"),
            "entropia": contexto.get("entropy"),
            "error_rate": contexto.get("error_rate"),
            "razon": "HALT detectado"
        }
        self.historial.append(entrada)
        self._imprimir(entrada)
        self._guardar_log()
        self.generar_graficos()

    def _imprimir(self, entrada: dict):
        print(f"[🛑 HALT] {entrada['timestamp']} | Ciclo: {entrada['ciclo']} | "
              f"Entropía: {entrada['entropia']} | Error: {entrada['error_rate']}")

    def _guardar_log(self):
        try:
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(self.historial, f, indent=4)
            print(f"[📤 HALT_LOG] Registro actualizado: {self.log_path}")
        except Exception as e:
            print(f"[❌ HALT_LOG] Error al guardar log: {e}")

    def _cargar_log_existente(self):
        if self.log_path.exists():
            try:
                with open(self.log_path, "r", encoding="utf-8") as f:
                    self.historial = json.load(f)
                print(f"[📥 HALT_LOG] Log cargado con {len(self.historial)} eventos previos.")
            except Exception as e:
                print(f"[⚠️ HALT_LOG] Error al cargar log previo: {e}")

    def exportar_json(self, historial=None):
        datos = historial if historial is not None else self.historial
        try:
            timestamp = datetime.datetime.utcnow().isoformat()
            export_data = {
                "timestamp": timestamp,
                "eventos": datos
            }
            with open(self.export_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=4)
            print(f"[📤 HALT_EXPORT] Historial exportado: {self.export_path}")
        except Exception as e:
            print(f"[❌ HALT_EXPORT] Error al exportar JSON: {e}")

    def generar_graficos(self):
        if not self.historial:
            print("[⚠️ GRAFICOS] No hay datos para graficar.")
            return

        ciclos = [h["ciclo"] for h in self.historial if h.get("ciclo") is not None]
        entropias = [h["entropia"] for h in self.historial if h.get("entropia") is not None]
        errores = [h["error_rate"] for h in self.historial if h.get("error_rate") is not None]

        if not ciclos:
            print("[⚠️ GRAFICOS] Datos incompletos para graficar.")
            return

        os.makedirs("logs", exist_ok=True)

        # --- Entropía ---
        plt.figure(figsize=(10, 5))
        plt.plot(ciclos, entropias, marker='o', color='blue', label='Entropía')
        plt.title("Entropía en eventos HALT")
        plt.xlabel("Ciclo")
        plt.ylabel("Entropía")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig("logs/halt_entropy_plot.png")
        print("[📊 GRAFICO] Generado: logs/halt_entropy_plot.png")

        # --- Error Rate ---
        plt.figure(figsize=(10, 5))
        plt.plot(ciclos, errores, marker='x', color='red', label='Error rate')
        plt.title("Error rate en eventos HALT")
        plt.xlabel("Ciclo")
        plt.ylabel("Error rate")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig("logs/halt_error_plot.png")
        print("[📊 GRAFICO] Generado: logs/halt_error_plot.png")

        # --- Histograma HALTs por ciclo ---
        plt.figure(figsize=(10, 5))
        plt.hist(ciclos, bins=range(min(ciclos), max(ciclos) + 2), color='orange', edgecolor='black')
        plt.title("Frecuencia de HALTs por ciclo")
        plt.xlabel("Ciclo")
        plt.ylabel("Cantidad de HALTs")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.savefig("logs/halt_histogram.png")
        print("[📊 GRAFICO] Generado: logs/halt_histogram.png")
