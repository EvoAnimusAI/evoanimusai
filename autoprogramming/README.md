cat > autoprogramming/README.md <<EOF
# 🧠 AutoProgramming Module — EvoAI v22

Este módulo forma parte del subsistema de *programación autónoma simbólica y dirigida* de EvoAnimusAI. Está diseñado para generar, mutar y evaluar funciones simbólicas de forma autónoma, bajo principios evolutivos y semánticos.

---

## 📁 Estructura de componentes

| Archivo | Rol |
|--------|-----|
| `base_symbols.py` | Define estructuras y símbolos base utilizados en mutaciones. |
| `symbolic_function.py` | Representa funciones simbólicas con metadatos exportables. |
| `mutation_operator.py` | Aplica transformaciones sintácticas sobre árboles AST. |
| `semantic_mutation.py` | Optimiza expresiones sin alterar comportamiento funcional. |
| `directed_mutation.py` | Mutaciones guiadas por reglas, contexto o heurísticas. |
| `mutation_generator.py` | Motor de generación combinatoria de funciones. |
| `mutation_evaluation.py` | Evalúa la validez, impacto y consistencia de funciones mutadas. |

---

## ⚙️ Funcionamiento general

1. **Representación simbólica**  
   Se parte de una función representada como objeto `SymbolicFunction`.

2. **Mutación sintáctica**  
   `MutationBlock` transforma nombres de funciones, estructuras de control y bucles (`mutation_operator.py`).

3. **Mutación semántica**  
   `SemanticMutationBlock` reescribe expresiones sin afectar la lógica (e.g., `x + 0 → x`).

4. **Mutación dirigida (opcional)**  
   Se emplean reglas o condiciones adaptativas (`directed_mutation.py`) para modular las transformaciones.

5. **Evaluación post-mutation**  
   Se valida que la nueva función sea válida y significativa (`mutation_evaluation.py`).

---

## ✅ Casos de uso

```python
from autoprogramming.mutation_operator import mutate_function

original_code = \"\"\"
def energy(x):
    return x * 1 + 0
\"\"\"

mutated_code = mutate_function(original_code, force_all_mutations=True)
print(mutated_code)
