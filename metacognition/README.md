# 🧠 Metacognition Module — EvoAI

El módulo `metacognition/` implementa las capacidades de *metacognición simbólica* para EvoAI, permitiendo que el sistema observe, evalúe y modifique sus propios procesos internos en tiempo de ejecución.

## 📌 Propósito

Este subsistema actúa como un "supervisor cognitivo" que analiza el desempeño del agente, detecta errores o ineficiencias, y aplica mutaciones dirigidas o detenciones autónomas para corregir la conducta simbólica.

## 🧩 Componentes

| Archivo                  | Rol principal                                                                 |
|--------------------------|------------------------------------------------------------------------------|
| `autonomous_stop.py`     | Detiene el sistema en función de criterios de error, agotamiento o recursión. |
| `targeted_mutation.py`   | Aplica mutaciones dirigidas sobre reglas simbólicas, basadas en el contexto. |
| `controller.py`          | Coordina decisiones metacognitivas según el state simbólico del agente.     |
| `interfaces.py`          | Define contratos abstractos para estrategias de mutación y control.          |
| `constants.py`           | Variables simbólicas y umbrales críticos utilizados por el controlador.      |
| `__init__.py`            | Inicializa el submódulo metacognitivo de EvoAI.                              |

## 🛠️ Funcionalidades clave

- **Mutación dirigida:**  
  Cambia dinámicamente reglas simbólicas de bajo rendimiento con base en métricas como entropy o tasa de error.

- **Parada autónoma:**  
  Detiene la ejecución del ciclo de vida del agente si se cumplen condiciones críticas (ej. errores reiterados, contexto degenerativo).

- **Control centralizado:**  
  El `controller.py` orquesta acciones metacognitivas (mutar, detener, continuar) según estrategias dinámicas.

## 🔁 Ejemplo de uso

```python
from metacognition.targeted_mutation import TargetedMutation

mutador = TargetedMutation()
contexto = {
    "entropy": 0.85,
    "error_rate": 0.6,
    "mutation_budget": 3
}
if mutador.mutate(contexto):
    print("✅ Mutación aplicada con éxito.")
else:
    print("⚠️ No se aplicó mutación.")
