cat << 'EOF' > tools/README.md
# 🛠️ Módulo de Herramientas (`tools/`)

Este módulo contiene utilidades operativas que extienden y automatizan tareas del sistema EvoAnimusAI. Actualmente incluye lógica de carga, versionado e inyección de reglas simbólicas en el motor de aprendizaje.

---

## 📄 `load_new_rules.py`

### Funcionalidad principal

Script diseñado para:

- 📥 Cargar reglas simbólicas desde un archivo YAML (`data/rules/default_rules.yaml`)
- 🧠 Compararlas contra las reglas actualmente persistidas (`symbolic_rule_engine.json`)
- ➕ Detectar y agregar reglas nuevas no redundantes
- 💾 Guardar las reglas actualizadas en disco
- 🚀 Inicializar el motor simbólico (`SymbolicLearningEngine`) con las reglas nuevas

---

### Dependencias

- `pyyaml`: para parsear archivos `.yaml`
- `core.engine.RuleEngineAdapter`
- `symbolic_ai.symbolic_learning_engine.SymbolicLearningEngine`
- `symbolic_ai.rule_manager.RuleManager`

Instala las dependencias si falta alguna:

```bash
pip install pyyaml
