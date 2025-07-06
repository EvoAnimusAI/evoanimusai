#!/bin/bash

set -euo pipefail

FILE="data/symbolic_rule_engine.json"
BACKUP_DIR="data/backups"
LOG_FILE="data/sanitize.log"
TMP_FILE="$FILE.tmp"
CLEAN_FILE="data/symbolic_rule_engine_cleaned.json"
HASH_FILE="data/symbolic_rule_engine.sha256"
TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")

echo "[INFO] [$TIMESTAMP] Sanitizando reglas defectuosas..." | tee -a "$LOG_FILE"

if [[ ! -f "$FILE" ]]; then
    echo "[ERROR] [$TIMESTAMP] Archivo no encontrado: $FILE" | tee -a "$LOG_FILE"
    exit 1
fi

mkdir -p "$BACKUP_DIR"
cp "$FILE" "$BACKUP_DIR/symbolic_rule_engine_$TIMESTAMP.json"
echo "[INFO] [$TIMESTAMP] Backup completo guardado." | tee -a "$LOG_FILE"

if ! jq empty "$FILE" >/dev/null 2>&1; then
    echo "[ERROR] [$TIMESTAMP] JSON malformado: $FILE" | tee -a "$LOG_FILE"
    exit 2
fi

TOTAL=$(jq '.rules | length' "$FILE")

jq '.rules |= map(select(
    (has("rol") and (.rol | type == "string")) and
    (has("valor") and (.valor | type == "string")) and
    (has("accion") and (.accion | type == "string")) and
    (has("condicion") and (.condicion | type == "string")) and
    (has("texto") and (.texto | type == "string"))
))' "$FILE" > "$CLEAN_FILE"

VALID=$(jq '.rules | length' "$CLEAN_FILE")
REMOVED=$((TOTAL - VALID))

if [[ "$VALID" -eq 0 ]]; then
    echo "[ALERT] [$TIMESTAMP] No se encontraron reglas válidas. Abortando por seguridad." | tee -a "$LOG_FILE"
    exit 3
fi

mv "$CLEAN_FILE" "$FILE"
echo "[INFO] [$TIMESTAMP] Archivo reparado: $VALID reglas válidas / $REMOVED eliminadas." | tee -a "$LOG_FILE"

sha256sum "$FILE" > "$HASH_FILE"
echo "[INFO] [$TIMESTAMP] Firma SHA256 generada correctamente." | tee -a "$LOG_FILE"

echo "[SUCCESS] [$TIMESTAMP] Reparación completada." | tee -a "$LOG_FILE"
