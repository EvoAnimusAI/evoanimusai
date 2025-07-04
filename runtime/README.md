# Runtime ‒ Núcleo de Ejecución de **EvoAnimus AI**

> **Versión:** 2025-07-03  
> **Ámbito:** Operaciones críticas, entornos militares, gubernamentales y corporativos de alta seguridad.  
> **Licencia:** Propietaria. Todos los derechos reservados.

---

## 1. Propósito

El bloque **`runtime`** orquesta la ejecución de EvoAnimus AI.  
Garantiza la interaction coherente entre el motor simbólico, los módulos de mutación autónoma y los sistemas de monitorización, bajo estrictos controles de entropy y de seguridad estructural.

---

## 2. Componentes Principales

| Módulo | Descripción Ejecutiva |
|-------|------------------------|
| **`executor.py`** | Motor central. Aplica reglas simbólicas, ejecuta acciones, dispara mutaciones (funcionales, hiper-mutaciones y de reglas) y persiste el conocimiento. |
| **`monitor.py`** | Instrumentación de alto nivel; provee métricas de ciclo y resúmenes ejecutivos. |
| **`rule_adaptation.py`** | Estrategias de adaptación de reglas: primarias (`adapt_rules`) y de contingencia (`fallback_adapt_rules`). |
| **`utils.logging`** (externo) | Canal único de auditoría; registra eventos en consola y en `logs/system_events.log`. |
| **Coberturas (`*.cover`)** | Artefactos generados por herramientas de análisis estático/cobertura; pueden purgarse en producción. |

---

## 3. Flujo de Ejecución

1. **Inyección de contexto** → `Executor.run()`  
2. **Evaluación simbólica** → `engine.decide(context)`  
3. **Ejecución de action** → `ActionRegistry.dispatch()`  
4. **Observación y logging** → `SymbioticObserver` + `log_event`  
5. **Mutaciones controladas**  
   - Reglas: `RULE_MUTATION_PROBABILITY`  
   - Funciones: `FUNCTION_MUTATION_PROBABILITY`  
   - Hiper-mutación: `HYPERMUTATION_PROBABILITY` (gatillada por la clase `MutationTrigger`)  
6. **Persistencia periódica** (cada `SYMBOLIC_PERSISTENCE_INTERVAL` pasos)  
7. **Monitorización** → `ExecutionMonitor` y `EvoAIMonitor` consolidan telemetría de misión.

> **Corte de emergencia:** `evaluate_contextual_stop` puede emitir `StopIteration` para cesar la operación de manera autónoma sin intervención humana.

---

## 4. Parámetros Críticos (ajuste fino)

| Constante (Executor) | Valor por defecto | Impacto | Recom. producción |
|----------------------|-------------------|---------|-------------------|
| `ENTROPY_THRESHOLD` | **0.7** | Dispara mutaciones automáticas si la entropy del agente supera el umbral. | Ajustar ≥ 0.85 en entornos estables. |
| `ACTION_REPEAT_LIMIT` | 5 | Previene bucles de action repetitiva. | Mantener. |
| `HYPERMUTATION_PROBABILITY` | 0.02 | Hiper-mutaciones de alto riesgo / alta recompensa. | ≤ 0.01 en sistemas críticos. |
| `SYMBOLIC_PERSISTENCE_INTERVAL` | 10 | Frecuencia de guardado de reglas. | Elevar a 50 si I/O es costoso. |

Cambios se aplican directamente en `executor.py` o vía variables de entorno inyectadas al proceso.

---

## 5. Instalación

```bash
# Clonar repositorio privado
git clone git@repositorio_privado:evoai/evoai22.git
cd evoai22

# Crear entorno
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
