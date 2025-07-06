#!/bin/bash

set -euo pipefail

timestamp() {
    date -u +"%Y%m%dT%H%M%SZ"
}

log() {
    printf "[%s] [%s] %s\n" "$(date -u +"%Y%m%dT%H%M%SZ")" "$1" "$2"
}

# === Parámetros base ===
DATA_DIR="data/rules"
RULES_FILE="$DATA_DIR/symbolic_rule_engine.json"
SHA_FILE="$DATA_DIR/symbolic_rule_engine.sha256"
BACKUP_DIR="data/backups"
MAX_BACKUPS=10

# === Validaciones iniciales ===
log "INFO" "Iniciando validación y control de integridad..."
log "INFO" "Archivo objetivo: $RULES_FILE"

if [[ ! -f "$RULES_FILE" ]]; then
    log "ERROR" "Archivo no encontrado: $RULES_FILE"
    exit 1
fi

# === Verificación SHA256 previa si existe ===
if [[ -f "$SHA_FILE" ]]; then
    log "INFO" "Verificando integridad previa (SHA256)..."
    EXPECTED_HASH=$(cut -d ' ' -f1 < "$SHA_FILE")
    CURRENT_HASH=$(sha256sum "$RULES_FILE" | cut -d ' ' -f1)
    if [[ "$EXPECTED_HASH" != "$CURRENT_HASH" ]]; then
        log "ALERT" "El archivo ha sido modificado desde la última firma. Abortando por seguridad."
        exit 1
    else
        log "OK" "Integridad previa verificada."
    fi
else
    log "WARN" "Archivo de firma no encontrado. Se generará uno nuevo si pasa la validación."
fi

# === Validación estructural del JSON ===
if ! jq -e '.rules | arrays' "$RULES_FILE" > /dev/null 2>&1; then
    log "ERROR" "JSON no contiene arreglo 'rules'"
    exit 1
fi

RULE_COUNT=$(jq '.rules | length' "$RULES_FILE")
log "INFO" "Reglas encontradas: $RULE_COUNT"

# === Backup preventivo ===
mkdir -p "$BACKUP_DIR"
BACKUP_NAME="symbolic_rule_engine_$(timestamp).json"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"
cp "$RULES_FILE" "$BACKUP_PATH"
log "INFO" "Backup guardado: $BACKUP_PATH"

# === Rotación de backups (mantener últimos $MAX_BACKUPS) ===
TOTAL_BACKUPS=$(ls -1t "$BACKUP_DIR"/symbolic_rule_engine_*.json 2>/dev/null | wc -l)
if (( TOTAL_BACKUPS > MAX_BACKUPS )); then
    TO_DELETE=$(ls -1t "$BACKUP_DIR"/symbolic_rule_engine_*.json | tail -n +$((MAX_BACKUPS + 1)))
    for f in $TO_DELETE; do
        rm -f "$f"
        log "INFO" "Backup eliminado por rotación: $f"
    done
fi

# === Firmar el archivo (SHA256) ===
sha256sum "$RULES_FILE" > "$SHA_FILE"
log "INFO" "Firma SHA256 actualizada: $SHA_FILE"

log "SUCCESS" "Validación y firma completadas correctamente."
