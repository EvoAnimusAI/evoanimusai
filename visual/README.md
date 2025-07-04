visual/README.md
# 👁️ Módulo de Visualización Simbólica (`visual/`)

Este módulo proporciona soporte visual en tiempo real para inspeccionar el **state simbólico interno** del sistema EvoAnimusAI, con fines de depuración, trazabilidad y análisis de decisiones simbólicas.

---

## 📄 `symbolic_view.py`

### ✨ Propósito

El archivo `symbolic_view.py` contiene la función `show_symbolic_state`, la cual imprime una representación estructurada del state simbólico actual del agente, en base a los siguientes componentes:

- **Contexto simbólico actual (`context`)**
- **Decisión tomada (`decision`)**
- **Observación simbólica actual (`observation`)**
- **Recompensa asociada (`reward`)** *(opcional)*
- **Información adicional (`extra_info`)** *(opcional)*

### 🧪 Ejemplo de uso:

```python
from visual.symbolic_view import show_symbolic_state

show_symbolic_state(
    context=my_context,
    decision={"action": "advance"},
    observation={"action": "advance", "confidence": 0.95},
    reward=1.0,
    extra_info={"note": "strategic decision"}
)
