#!/bin/bash

set -euo pipefail

FILE="data/symbolic_rule_engine.json"
BACKUP_DIR="data/backups"
LOG_FILE="data/sanitize.log"
TMP_FILE="$FILE.tmp"
HASH_FILE="data/symbolic_rule_engine.sha256"
TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")

echo "[INFO] [$TIMESTAMP] Iniciando validación y control de integridad..." | tee -a "$LOG_FILE"

# 1. Verificar existencia del archivo
if [[ ! -f "$FILE" ]]; then
    echo "[ERROR] [$TIMESTAMP] Archivo no encontrado: $FILE" | tee -a "$LOG_FILE"
    exit 1
fi

# 2. Verificar integridad previa si existe firma
if [[ -f "$HASH_FILE" ]]; then
    echo "[INFO] [$TIMESTAMP] Verificando integridad previa (SHA256)..." | tee -a "$LOG_FILE"
    if ! sha256sum -c "$HASH_FILE" --status; then
        echo "[ALERT] [$TIMESTAMP] El archivo ha sido modificado desde la última firma. Abortando por seguridad." | tee -a "$LOG_FILE"
        exit 100
    else
        echo "[OK] [$TIMESTAMP] Integridad previa verificada." | tee -a "$LOG_FILE"
    fi
else
    echo "[WARN] [$TIMESTAMP] No existe firma previa. Se procederá sin verificación de integridad." | tee -a "$LOG_FILE"
fi

# 3. Validar sintaxis del JSON
if ! jq empty "$FILE" >/dev/null 2>&1; then
    echo "[ERROR] [$TIMESTAMP] JSON inválido: $FILE" | tee -a "$LOG_FILE"
    exit 2
fi

# 4. Validar esquema mínimo
if ! jq 'has("rules") and (.rules | type == "array")' "$FILE" | grep -q true; then
    echo "[ERROR] [$TIMESTAMP] JSON no contiene arreglo 'rules'" | tee -a "$LOG_FILE"
    exit 3
fi

# 5. Validar estructura interna de cada regla
if ! jq -e '
  .rules[] |
  select(
    (has("rol") and .rol | type == "string") and
    (has("valor") and .valor | type == "string") and
    (has("accion") and .accion | type == "string") and
    (has("condicion") and .condicion | type == "string") and
    (has("texto") and .texto | type == "string")
  )
' "$FILE" >/dev/null; then
    echo "[ERROR] [$TIMESTAMP] Estructura inválida en al menos una regla." | tee -a "$LOG_FILE"
    exit 4
fi

# 6. Backup
mkdir -p "$BACKUP_DIR"
cp "$FILE" "$BACKUP_DIR/symbolic_rule_engine_$TIMESTAMP.json"
echo "[INFO] [$TIMESTAMP] Backup guardado en $BACKUP_DIR" | tee -a "$LOG_FILE"

# 7. Reemplazo condicional
jq '.
  rules |= map(
    if .condicion == "entropy > 0.5"
    then
      .condicion = "entropy >= 0.9"
      | .texto = (.texto | sub("entropy > 0.5"; "entropy >= 0.9"))
    else
      .
    end
  )
' "$FILE" > "$TMP_FILE" && mv "$TMP_FILE" "$FILE"
echo "[INFO] [$TIMESTAMP] Reemplazo aplicado correctamente" | tee -a "$LOG_FILE"

# 8. Generar firma nueva
sha256sum "$FILE" > "$HASH_FILE"
echo "[INFO] [$TIMESTAMP] Nueva firma SHA256 almacenada en $HASH_FILE" | tee -a "$LOG_FILE"

# 9. Verificación de reemplazo
if grep -q 'entropy >= 0.9' "$FILE"; then
    echo "[SUCCESS] [$TIMESTAMP] Operación finalizada con éxito." | tee -a "$LOG_FILE"
    exit 0
else
    echo "[ERROR] [$TIMESTAMP] La modificación no fue aplicada correctamente" | tee -a "$LOG_FILE"
    exit 5
fi
