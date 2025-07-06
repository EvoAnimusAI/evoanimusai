#!/bin/bash
# launch_halt_server.sh
# Lanzador militar del HALT Server EvoAI como servicio autónomo

ENV_DIR="evoai_env311"
PROJECT_DIR="$HOME/evoai22"
LOG_FILE="$PROJECT_DIR/logs/halt_server_output.log"

echo "[🟢 START] Activando entorno virtual: $ENV_DIR"
source "$HOME/$ENV_DIR/bin/activate"

echo "[🚀 LAUNCH] Iniciando halt_server.py en segundo plano..."
nohup python3 "$PROJECT_DIR/tools/halt_server.py" >> "$LOG_FILE" 2>&1 &

PID=$!
echo "[✅ PID] Servidor HALT lanzado con PID $PID"
echo "[📡 STATUS] Accede en http://localhost:8080"
echo "[📁 LOG] Salida en: $LOG_FILE"
