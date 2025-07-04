# 🧠 EvoAI Daemon Module

**Versión clasificada - Nivel militar y gubernamental**  
Subsistema de núcleo simbólico para ejecución autónoma, evaluación continua y operación ininterrumpida de EvoAI.

## 🧬 Descripción General

El directorio `daemon/` encapsula la lógica operativa de alto nivel de EvoAI, gestionando:

- Inicialización de subsistemas críticos
- Seguridad y trazabilidad
- Memoria simbólica y funcional
- Visualización en tiempo real
- Control de apagado seguro
- Aprendizaje en red y mutación simbólica

Este bloque constituye el **superdaemon** del sistema EvoAI, cumpliendo estándares militares de robustez, modularidad y resiliencia.

---

## 📂 Estructura Modular

| Módulo                         | Función principal                                                                 |
|-------------------------------|------------------------------------------------------------------------------------|
| `evoai_config.py`             | Gestión centralizada de configuraciones y rutas internas                          |
| `evoai_context.py`            | Inicialización del contexto simbólico operativo                                   |
| `evoai_cycle_executor.py`     | Ejecución cíclica del agente con lógica de control                                |
| `evoai_daemon.py`             | Punto de entrada principal para el runtime del superdaemon                        |
| `evoai_initializer_*.py`      | Fábricas de inicialización modular para cada componente (agent, engine, etc.)     |
| `evoai_logger.py`             | Logging estructurado de nivel militar (trazabilidad, auditoría, redundancia)     |
| `evoai_memory.py`             | Memoria simbólica persistente y funcional del agente                              |
| `evoai_mutation_handler.py`   | Lógica de mutación dirigida y simbólica con evaluación en caliente                |
| `evoai_network_learning.py`   | Aprendizaje desde la red con integración simbólica y evaluación contextual        |
| `evoai_shutdown_manager.py`   | Gestión de señales del sistema y apagado seguro                                   |
| `evoai_state.py`              | Estado operativo del agente, incluyendo función activa y contador de ciclos       |
| `evoai_subsystems.py`         | Ensamblaje de subsistemas: monitoreo, Codex, autoconsciencia, análisis, red       |
| `evoai_visualization.py`      | Renderizado simbólico del state interno para auditoría visual                    |

---

## 🔐 Estándares y Seguridad

- Cifrado y validación de claves vía `.env` y `dotenv`
- Logs redundantes en disco y consola
- Control de señales UNIX: `SIGINT`, `SIGTERM`, `SIGHUP`, `SIGQUIT`
- Aislamiento modular completo mediante inicializadores dedicados
- Carga de memoria simbólica validada por consistencia estructural
- Mutación simbólica controlada por contexto semántico y ciclo

---

## 🧪 Pruebas y Cobertura

Todos los módulos son testeables con `pytest` y `pytest-cov`.  
Ejemplo de ejecución:

```bash
PYTHONPATH=. pytest --cov=daemon.evoai_mutation_handler tests/test_evoai_mutation_handler.py
