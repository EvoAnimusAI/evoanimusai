#!/bin/bash
# ========================================================================================
# 🔧 clean_cache.sh — Limpieza oficial de caché de Python para EvoAnimusAI
# Autor: Unidad de Sistemas Avanzados
# Descripción: Elimina todos los __pycache__, .pyc y .pyo de forma segura y trazable.
# Nivel: Seguridad estructural gubernamental
# ========================================================================================

echo "[🧹] Iniciando limpieza estructural de cachés de Python..."

PROJECT_ROOT="$(dirname "$0")"
cd "$PROJECT_ROOT" || exit 1

# Eliminar todos los directorios __pycache__
echo "[INFO] Eliminando directorios __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} +

# Eliminar todos los archivos .pyc y .pyo
echo "[INFO] Eliminando archivos *.pyc y *.pyo..."
find . -type f -name "*.pyc" -o -name "*.pyo" -delete

echo "[✅] Limpieza completada con éxito. Sistema sin residuos de compilación."
