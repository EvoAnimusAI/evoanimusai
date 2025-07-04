#!/bin/bash

# ========================================
# 🔧 Script para traducir términos clave EvoAI al inglés
# ========================================

echo "🔍 Corrigiendo términos en español dentro del código fuente..."

# Mapeos clave
declare -A translations=(
  ["entropy"]="entropy"
  ["noise"]="noise"
  ["state"]="state"
  ["action"]="action"
  ["explored"]="explored"
  ["position"]="position"
  ["energy"]="energy"
)

# Recorrer el árbol del proyecto (excluyendo .venv y __pycache__)
for file in $(grep -RIlE "$(IFS=\|; echo "${!translations[*]}")" . \
              --exclude-dir=.venv --exclude-dir=__pycache__ \
              --exclude=daemon/evoai_context.py); do

  echo "📄 Procesando: $file"

  for key in "${!translations[@]}"; do
    value=${translations[$key]}
    sed -i "s/'$key'/'$value'/g" "$file"
    sed -i "s/$key/$value/g" "$file"
  done
done

# Corrección específica de f-strings en core/environment.py
sed -i 's/Acción calmante: entropy de/Soothing action: entropy from/' core/environment.py
sed -i "s/self.state'entropy'/self.state['entropy']/" core/environment.py

echo "✅ Traducción completada."
