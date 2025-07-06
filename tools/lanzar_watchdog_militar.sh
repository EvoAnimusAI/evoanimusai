#!/bin/bash

echo "🔐 Iniciando Watchdog EvoAI Simbiótico..."

# Ruta absoluta al entorno virtual
VENV_PATH="$HOME/evoai_env311/bin/activate"

# Validar existencia del entorno virtual
if [ ! -f "$VENV_PATH" ]; then
  echo "❌ ERROR: No se encontró el entorno virtual en $VENV_PATH"
  exit 1
fi

# Activar entorno virtual
source "$VENV_PATH"

# Asegurar existencia del directorio de logs
mkdir -p logs

# Lanzar watchdog en segundo plano con trazabilidad
nohup python3 tools/watchdog_daemon_recover.py >> logs/watchdog.log 2>> logs/watchdog_error.log &
disown

echo "✅ Watchdog lanzado en segundo plano. Log: logs/watchdog.log"
