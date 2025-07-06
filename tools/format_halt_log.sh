#!/bin/bash
FILE="logs/halt_history_export.json"

if [ -f "$FILE" ]; then
  echo "🛠️  Formateando $FILE..."
  jq . "$FILE" > "$FILE.tmp" && mv "$FILE.tmp" "$FILE"
  echo "✅ Formato corregido."
else
  echo "⚠️  Archivo $FILE no encontrado."
fi
