# watchdog_daemon_recover.py
# -*- coding: utf-8 -*-
"""
Watchdog simbólico militar — reinicia evoai_daemon.py si se detecta estancamiento prolongado o inactividad total.
"""
import time
import subprocess
import psutil
import os

DAEMON_PATH = "daemon/evoai_daemon.py"
CHECK_INTERVAL = 30  # segundos
INACTIVITY_THRESHOLD = 120  # segundos sin actividad

LAST_LOG = "logs/cycle_activity.log"
PID_FILE = "runtime/evoai_daemon.pid"

def is_daemon_running():
    if not os.path.exists(PID_FILE):
        return False
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        return psutil.pid_exists(pid)
    except Exception:
        return False

def check_last_activity():
    if not os.path.exists(LAST_LOG):
        return 0
    return time.time() - os.path.getmtime(LAST_LOG)

def restart_daemon():
    print("[🛡️ WATCHDOG] Reiniciando daemon EvoAI...")
    subprocess.Popen(["nohup", "python3", DAEMON_PATH, "&"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    print("[🔒 WATCHDOG] Monitoreo activo del daemon EvoAI...")
    while True:
        if not is_daemon_running() or check_last_activity() > INACTIVITY_THRESHOLD:
            restart_daemon()
        time.sleep(CHECK_INTERVAL)
