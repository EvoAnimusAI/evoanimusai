#!/bin/bash
echo "Ejecutando tests con pytest..."
pytest tests/test_symbolic_learning_engine.py --maxfail=1 --disable-warnings -q

if [ $? -eq 0 ]; then
    echo "Tests PASADOS ✅"
else
    echo "Tests FALLADOS ❌"
fi
