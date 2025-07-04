ARCHIVOS CLAVE INVOLUCRADOS EN MUTACIONES AUTOMÁTICAS

🔁 1. Activación de mutaciones

Archivo	Instrucción relevante

runtime/executor.py	mutate_complete_function
executor.py	mutate_complete_function
symbolic_ai/hypermutator.py	Define mutate_complete_function
tests/test_hypermutator.py	Test unitario de mutate_complete_function



---

🧠 2. Motor de aprendizaje simbólico

Archivo	Acción

symbolic_ai/symbolic_learning_engine.py	Clase SymbolicLearningEngine
tools/load_new_rules.py	Crea motor de aprendizaje con nuevas reglas
core/engine.py	Usa SymbolicLearningEngine(RuleEngineAdapter)
daemon/evoai_context.py	Inyección directa del motor simbólico
tests/test_symbolic_learning_engine.py	Tests del motor de aprendizaje



---

📚 3. Motor de reglas simbólicas (ejecución de reglas)

Archivo	Acción

symbolic_ai/symbolic_rule_engine.py	Define SymbolicRuleEngine
core/symbolic_decision_engine.py	Usa SymbolicRuleEngine()
daemon/evoai_initializer_core.py	Inicializa SymbolicRuleEngine()
evoai_bootstrap.py	Usa SymbolicRuleEngine(auto_load=True)
tests/test_symbolic_rule_engine.py	Pruebas de reglas simbólicas



---

🧩 4. Adaptadores y contexto

Archivo	Contenido

core/engine.py	Define RuleEngineAdapter
tools/load_new_rules.py	Usa RuleEngineAdapter(reglas_actualizadas)
core/symbolic_decision_engine.py	Usa SymbolicRuleEngine
daemon/evoai_context.py	Motor simbólico embebido self.symbolic = SymbolicLearningEngine(...)



---

🧪 5. Tests relacionados

Archivo	Cobertura

tests/test_hypermutator.py	Función de mutación principal
tests/test_symbolic_learning_engine.py	Motor de aprendizaje
tests/test_symbolic_rule_engine.py	Motor de reglas
tests/test_symbolic_ai.py	Integraciones simbólicas
tests/test_evoai_context.py	Integración con el contexto
tests/test_bootstrap.py	Inicialización desde arranque



---

📁 6. Rutas relevantes para reglas

Ruta	Contenido

data/rules/default_rules.yaml	Reglas YAML (entrada manual)
data/rules/symbolic_rule_engine.json	Reglas versionadas y guardadas


