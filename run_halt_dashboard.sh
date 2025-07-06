#!/bin/bash
source ~/evoai_env311/bin/activate
python3 tools/halt_server_secure.py >> logs/halt_dashboard.log 2>&1
