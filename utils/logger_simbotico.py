# utils/logger_simbotico.py

import os
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "knowledge_logs"
HALT_LOG = BASE_DIR / "halt_events_log.jsonl"
RECOVERY_LOG = BASE_DIR / "recovery_sessions.json"
SNAPSHOT_DIR = BASE_DIR / "crisis_snapshots"

def ensure_directories():
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    if not HALT_LOG.exists():
        HALT_LOG.write_text("")
    if not RECOVERY_LOG.exists():
        RECOVERY_LOG.write_text("[]")

def log_halt_event(event_data: dict):
    ensure_directories()
    timestamp = datetime.utcnow().isoformat()
    event_data["timestamp"] = timestamp
    with HALT_LOG.open("a") as f:
        f.write(json.dumps(event_data) + "\n")
    print(f"[📉 LOG] Evento HALT registrado en: {HALT_LOG}")

def save_crisis_snapshot(context_data: dict, cycle_num: int):
    ensure_directories()
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    filename = SNAPSHOT_DIR / f"snapshot_cycle{cycle_num}_{timestamp}.json"
    with filename.open("w") as f:
        json.dump(context_data, f, indent=2)
    print(f"[🧊 SNAPSHOT] Contexto crítico guardado en: {filename}")
    return filename.name

def append_recovery_session(session_data: dict):
    ensure_directories()
    timestamp = datetime.utcnow().isoformat()
    session_data["timestamp"] = timestamp
    sessions = []
    if RECOVERY_LOG.exists():
        try:
            sessions = json.loads(RECOVERY_LOG.read_text())
        except Exception:
            print("[WARN] Registro de sesiones de recuperación estaba corrupto.")
            sessions = []
    sessions.append(session_data)
    with RECOVERY_LOG.open("w") as f:
        json.dump(sessions, f, indent=2)
    print(f"[🔁 RECOVERY LOG] Sesión registrada: {session_data.get('motivo', 'N/A')}")
