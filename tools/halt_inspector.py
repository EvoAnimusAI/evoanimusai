# -*- coding: utf-8 -*-
"""
HaltInspector - Auditoría y Diagnóstico de eventos HALT con estándares gubernamentales y militares.
Analiza, clasifica, exporta y reporta eventos HALT críticos del sistema EvoAI.
"""

import json
import os
from datetime import datetime
from collections import Counter
import hashlib
import logging

HALT_JSON_PATH = "logs/halt_events.json"
EXPORT_PATH = "logs/halt_diagnostics_report.json"
LOG_PATH = "logs/halt_inspector_audit.log"

SEVERITY_THRESHOLDS = {
    "LOW": 1,
    "MEDIUM": 5,
    "HIGH": 7,
    "CRITICAL": 9
}

logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                    format="%(asctime)s [HALT_INSPECTOR] %(levelname)s - %(message)s")


def cargar_eventos(path=HALT_JSON_PATH):
    if not os.path.exists(path):
        logging.warning("Archivo de eventos HALT no encontrado.")
        return []
    try:
        with open(path, "r") as f:
            eventos = json.load(f)
            logging.info(f"✅ {len(eventos)} eventos HALT cargados.")
            return eventos
    except Exception as e:
        logging.error(f"❌ Error al leer archivo: {e}")
        return []


def clasificar_evento(evento):
    sev = evento.get("severidad", 0)
    if sev >= SEVERITY_THRESHOLDS["CRITICAL"]:
        return "CRITICAL"
    elif sev >= SEVERITY_THRESHOLDS["HIGH"]:
        return "HIGH"
    elif sev >= SEVERITY_THRESHOLDS["MEDIUM"]:
        return "MEDIUM"
    else:
        return "LOW"


def generar_reporte(eventos):
    total = len(eventos)
    severidades = Counter([clasificar_evento(e) for e in eventos])
    razones = Counter([e.get("razon", "Desconocida") for e in eventos])
    tipos = Counter([e.get("tipo", "sin_tipo") for e in eventos])

    ultimos_10 = eventos[-10:] if total >= 10 else eventos

    severidad_prom = round(sum([e.get("severidad", 0) for e in eventos]) / total, 2) if total else 0

    reporte = {
        "total_eventos": total,
        "clasificacion_severidad": dict(severidades),
        "tipos_detectados": dict(tipos),
        "razones_frecuentes": razones.most_common(5),
        "severidad_promedio": severidad_prom,
        "ultimos_eventos": ultimos_10,
        "firma_hash": generar_firma(eventos)
    }

    logging.info("📊 Reporte generado correctamente.")
    return reporte


def generar_firma(eventos):
    cadena = json.dumps(eventos, sort_keys=True).encode("utf-8")
    firma = hashlib.sha256(cadena).hexdigest()
    logging.info(f"🔐 Firma SHA256 del dataset: {firma}")
    return firma


def exportar_reporte(reporte, path=EXPORT_PATH):
    try:
        with open(path, "w") as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        logging.info(f"📤 Reporte exportado a {path}")
        return True
    except Exception as e:
        logging.error(f"❌ Error exportando reporte: {e}")
        return False


def inspeccionar_halt():
    eventos = cargar_eventos()
    if not eventos:
        print("[ERROR] No se encontraron eventos HALT.")
        return

    reporte = generar_reporte(eventos)
    exportar_reporte(reporte)

    print("\n=== 🧠 HALT INSPECTOR REPORT ===")
    print(f"Total eventos: {reporte['total_eventos']}")
    print(f"Severidad promedio: {reporte['severidad_promedio']}")
    print(f"Clasificación: {reporte['clasificacion_severidad']}")
    print(f"Top razones HALT: {[r[0] for r in reporte['razones_frecuentes']]}")
    print(f"Hash SHA256: {reporte['firma_hash']}")
    print(f"Reporte guardado en: {EXPORT_PATH}")
    print("================================\n")


if __name__ == "__main__":
    inspeccionar_halt()
