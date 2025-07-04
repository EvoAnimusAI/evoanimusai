cat << 'EOF' > utils/README.md
# 🧩 Módulo de Utilidades (`utils/`)

Este módulo proporciona herramientas auxiliares críticas que dan soporte al núcleo del sistema EvoAnimusAI. Contiene componentes reutilizables como loggers personalizados, observadores simbióticos y configuraciones por defecto de reglas de comportamiento.

---

## 📄 `default_rules.py`

### Propósito

Define un conjunto inicial de reglas simbólicas con prioridades preestablecidas, útil para pruebas, simulaciones o carga base del motor simbólico.

### Salida esperada

```python
[
    {"action": "explore", "priority": 1.0},
    {"action": "wait", "priority": 0.8},
    {"action": "calm", "priority": 0.5},
    {"action": "advance", "priority": 0.9}
]
