# Módulo: mutations/

## Propósito

Este módulo implementa el **motor de mutación simbólica** del sistema EvoAI. Su función principal es generar funciones alteradas dinámicamente (mutadas) basadas en el conocimiento del agente y el contexto simbólico actual. Las funciones resultantes son auditables, ejecutables y trazables para análisis posteriores o evolución adaptativa.

---

## Componentes

### `mutation_engine.py`

Contiene:

- `MutatedFunction`: clase contenedora para funciones mutadas, incluye:
  - Código fuente.
  - Objeto ejecutable (`callable`).
  - Metadatos extensibles (trazabilidad, estrategia, conceptos origen).
  - Serialización estructurada (`to_dict()`).

- `mutate_function(agent_knowledge, context)`: genera dinámicamente una función mutada:
  - Toma conceptos simbólicos recientes del contexto (`context.symbolic.get_recent_concepts()`).
  - Crea una función Python simple (por defecto: duplicador `x * 2`).
  - Compila, valida y encapsula todo dentro de `MutatedFunction`.

---

## Casos de uso

- **Evolución simbólica programática**.
- **Análisis de desempeño mutacional**.
- **Integración con estrategias adaptativas del agente**.
- **Auditoría de cambios funcionales sobre la marcha**.

---

## Estándares aplicables

- Validación estricta de conceptos simbólicos.
- Fallos explícitos ante inconsistencias estructurales (`ValueError`, `RuntimeError`).
- Trazabilidad integrada: snapshot del state del agente, estrategia usada, conceptos origen.

---

## Pruebas unitarias

Archivo: `tests/test_mutation_engine.py`

- Cobertura sobre:
  - Generación exitosa.
  - Manejo de errores por falta de conceptos.
  - Manejo de fallos de obtención simbólica.

---

## Pendientes futuros

- Soporte para múltiples estrategias de mutación (no solo multiplicación).
- Persistencia de funciones mutadas.
- Seguridad de ejecución aislada.

