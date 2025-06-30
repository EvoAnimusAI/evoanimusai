from autoprogramming.symbolic_function import SymbolicFunction
from autoprogramming.mutation_evaluation import evaluate_mutation, memory, save_memory

# Crear función simbólica sencilla
func = SymbolicFunction(name="prueba", code="def prueba(): return 42")

# Evaluar mutación dado un contexto dummy
res = evaluate_mutation(func, {"entropy": 0.5, "energy": 100})

print("Resultado:", res)
print("Memoria actual:", [f.name for f in memory["functions"]])

# Guardar memoria en carpeta local 'data'
save_memory("data")
