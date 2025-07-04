#!/bin/bash
echo "🔍 Verificando que no existan términos en español en el código fuente..."
if grep -RInE "entrop[ií]a|ruido|acción|estado" . \
  --exclude-dir=.venv \
  --exclude-dir=__pycache__ \
  --exclude-dir=.git \
  --exclude-dir=scripts \
  --exclude=*.md \
  --exclude=*.txt \
  --exclude=*.po \
  --exclude=Makefile; then
    echo "❌ Commit bloqueado: Se encontraron términos en español."
    exit 1
else
    echo "✅ Pre-commit aprobado: todo en inglés."
fi
