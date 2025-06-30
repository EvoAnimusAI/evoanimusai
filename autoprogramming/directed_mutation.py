# evoai/autoprogramming/directed_mutation.py

import random
import copy
from typing import List, Optional
from autoprogramming.symbolic_function import SymbolicFunction


def mutate_parent_function(
    func_padre: SymbolicFunction,
    contexto: dict,
    temas_preferidos: Optional[List[str]] = None
) -> SymbolicFunction:
    """
    Realiza una mutación dirigida sobre una función simbólica.

    :param func_padre: función simbólica original
    :param contexto: dict con variables simbólicas de entorno
    :param temas_preferidos: lista opcional de temas relevantes para mutación
    :return: nueva instancia SymbolicFunction mutada
    """
    func_nueva = copy.deepcopy(func_padre)

    if temas_preferidos:
        for paso in func_nueva.pasos:
            if any(t in paso.get("accion", "") for t in temas_preferidos):
                paso["param"] = paso.get("param", 0) + random.uniform(-0.5, 0.5)
                break
        else:
            if func_nueva.pasos:
                idx = random.randint(0, len(func_nueva.pasos) - 1)
                func_nueva.pasos[idx]["param"] = func_nueva.pasos[idx].get("param", 0) + random.uniform(-1, 1)
    else:
        if func_nueva.pasos:
            idx = random.randint(0, len(func_nueva.pasos) - 1)
            func_nueva.pasos[idx]["param"] = func_nueva.pasos[idx].get("param", 0) + random.uniform(-1, 1)

    return func_nueva
