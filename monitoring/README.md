# 🧠 EvoAI Monitoring Subsystem

El submódulo `monitoring/` forma parte integral de la infraestructura de vigilancia cognitiva de EvoAI. Su función es detectar, registrar y analizar comportamientos anómalos o subóptimos en el sistema simbólico y de toma de decisiones. Diseñado bajo estándares militares y normativas de control ultra-especializadas.

---

## 📁 Estructura

### `analyzer_daemon.py`
- **Clase principal**: `EvoAIAnalyzerDaemon`
- **Propósito**: Ejecuta análisis periódicos sobre eventos generados por el motor de decisiones EvoAI.
- **Características**:
  - Detecta rendimiento promedio por action y por regla.
  - Emite recomendaciones (`keep/mutate` o `prune`) para reglas basadas en recompensa.
  - Persistencia de informes JSON (`logs/evoai_analysis_report.json`).
  - Preparado para ejecución cíclica (`run_cycle()`).

### `context_anomaly_logger.py`
- **Clase principal**: `ContextAnomalyLogger`
- **Propósito**: Valida la estructura del contexto simbólico utilizado en decisiones.
- **Norma interna**: `EVO-MON/CTX-VAL-4042`
- **Características**:
  - Revisa existencia y tipo de claves críticas: `state`, `observations`, `history`, `rewards`, `parameters`.
  - Emite logs críticos ante inconsistencias.
  - Facilita intervenciones preventivas antes de que una decisión incorrecta afecte el sistema.

---

## ⚙️ Dependencias
- Python ≥ 3.8
- Compatible con entornos donde EvoAI esté desplegado.
- Logging estándar (`logging`), no requiere dependencias externas.

---

## 🧪 Pruebas Unitarias

Ambos componentes están preparados para pruebas con `pytest`. Archivos de test esperados:

- `tests/test_analyzer_daemon.py`
- `tests/test_context_anomaly_logger.py`

---

## 🚨 Consideraciones de Seguridad

- **Sensibilidad**: Este módulo puede registrar decisiones y recompensas, potencialmente sensibles.
- **Privacidad de logs**: Asegúrese de cifrar o proteger el archivo `evoai_analysis_report.json` si opera en entornos públicos o compartidos.

---

## 🔒 Clasificación Interna

> **Clasificación**: *Militar / Gubernamental / Ultra-secreto*  
> **Uso restringido a entornos de simulación, combate cognitivo o validación ética avanzada.**

---

## 🧭 Futuro

Se proyecta que este módulo se integre con:
- Detección de anomalías basada en IA (autoencoders).
- Alerta temprana en tiempo real vía `websocket`.
- Panel visual tipo dashboard (`Grafana` o `Streamlit`).

---

## 🛰️ Unidad Responsable

> División de Monitoreo Cognitivo Preventivo (DMCP)  
> [Dirección General de Autonomía Evolutiva]

---
