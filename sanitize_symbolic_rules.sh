#!/bin/bash

FILE="data/symbolic_rule_engine.json"

printf "[INFO] Cargando archivo: %s\n" "$FILE"

# 1. Verificar existencia
if [[ ! -f "$FILE" ]]; then
    printf "[ERROR] Archivo no encontrado: %s\n" "$FILE"
    exit 1
fi

# 2. Validar sintaxis JSON
if ! jq empty "$FILE" >/dev/null 2>&1; then
    printf "[ERROR] Sintaxis JSON inválida en %s\n" "$FILE"
    exit 2
fi

# 3. Verificar campo raíz 'rules'
if ! jq 'has("rules") and (.rules | type == "array")' "$FILE" | grep -q true; then
    printf "[ERROR] JSON no contiene arreglo 'rules' válido\n"
    exit 3
fi

# 4. Validar estructura de cada regla
jq -e '
  .rules[] |
  select(
    (has("rol") and .rol | type == "string") and
    (has("valor") and .valor | type == "string") and
    (has("accion") and .accion | type == "string") and
    (has("condicion") and .condicion | type == "string") and
    (has("texto") and .texto | type == "string")
  )
' "$FILE" >/dev/null || {
    printf "[ERROR] Al menos una regla no cumple estructura esperada\n"
    exit 4
}

printf "[OK] Validación estructural completa\n"

# 5. Modificar condición si contiene 'entropy > 0.5'
printf "[INFO] Reescribiendo condiciones 'entropy > 0.5' → 'entropy >= 0.9'\n"

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
' "$FILE" > "$FILE.tmp" && mv "$FILE.tmp" "$FILE"

# 6. Confirmar resultado
if grep -q 'entropy >= 0.9' "$FILE"; then
    printf "[SUCCESS] Actualización completada exitosamente\n"
    exit 0
else
    printf "[ERROR] No se aplicó la modificación esperada\n"
    exit 5
fi
