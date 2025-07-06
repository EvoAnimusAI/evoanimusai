#!/bin/bash
echo "🔐 Lanzando Dashboard HALT Militar..."
cd "$(dirname "$0")/.."
nohup python3 tools/halt_server_secure.py > logs/dashboard_watchdog.log 2>&1 &
