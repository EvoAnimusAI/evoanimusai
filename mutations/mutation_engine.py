# mutations/mutation_engine.py

import random
import string
from typing import Optional, Callable, Any, Dict


class MutatedFunction:
    """
    Contenedor ejecutable para funciones mutadas con metadatos extensibles.

    Attributes:
        name (str): Identificador único de la función mutada.
        description (str): Descripción clara de la función y su propósito.
        code (str): Código fuente en formato texto.
        callable (Optional[Callable]): Objeto función compilada para ejecución.
        metadata (Dict[str, Any]): Información adicional para trazabilidad y auditoría.
        file_path (Optional[str]): Ruta del archivo fuente si existe.
    """

    def __init__(
        self,
        name: str,
        description: str,
        code: str,
        callable_obj: Optional[Callable] = None,
        metadata: Optional[Dict[str, Any]] = None,
        file_path: Optional[str] = None,
    ) -> None:
        self.name = name
        self.description = description
        self.code = code
        self.callable = callable_obj
        self.metadata = metadata or {}
        self.file_path = file_path

    def __call__(self, *args, **kwargs) -> Any:
        """
        Ejecuta la función mutada.

        Raises:
            RuntimeError: Si el objeto callable no está inicializado.
        """
        if not self.callable:
            raise RuntimeError("Callable object not initialized for mutated function.")
        return self.callable(*args, **kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """
        Exporta la función mutada y sus metadatos en formato dict.

        Returns:
            dict: Representación serializable de la función mutada.
        """
        return {
            "name": self.name,
            "description": self.description,
            "code": self.code,
            "metadata": self.metadata,
            "file_path": self.file_path,
        }

    def __str__(self) -> str:
        return f"<MutatedFunction name={self.name} description={self.description}>"


def mutate_function(agent_knowledge: Any, context: Any) -> MutatedFunction:
    """
    Motor básico para generar funciones mutadas en base a contexto simbólico.

    Args:
        agent_knowledge (Any): Estado o conocimiento actual del agente para la mutación.
        context (Any): Contexto simbólico que provee información relevante y reciente.

    Returns:
        MutatedFunction: Objeto con la función mutada y metadatos.

    Raises:
        ValueError: Si el contexto no provee conceptos simbólicos válidos.
    """
    # Generación de identificador único para la función
    unique_name = "func_" + ''.join(random.choices(string.ascii_lowercase, k=6))

    # Obtención de conceptos simbólicos recientes con validación estricta
    try:
        recent_concepts_raw = getattr(context.symbolic, "get_recent_concepts", lambda: [])()
    except Exception as e:
        raise ValueError(f"Error obteniendo conceptos simbólicos del contexto: {e}")

    if not recent_concepts_raw:
        raise ValueError("No se encontraron conceptos simbólicos recientes para mutación.")

    # Procesamiento explícito de conceptos
    if isinstance(recent_concepts_raw, list) and all(isinstance(c, dict) and "concept" in c for c in recent_concepts_raw):
        conceptos = [c["concept"] for c in recent_concepts_raw]
    else:
        conceptos = recent_concepts_raw

    descripcion = f"Función mutada generada a partir de conceptos simbólicos recientes: {conceptos}"

    # Código dinámico base (placeholder para integración futura de motores mutacionales avanzados)
    codigo_fuente = (
        f"def {unique_name}(x):\n"
        f"    # Función mutada de ejemplo que duplica el valor de entrada\n"
        f"    return x * 2\n"
    )

    # Compilación dinámica y segura del código fuente
    exec_globals: Dict[str, Any] = {}
    try:
        exec(codigo_fuente, exec_globals)
        callable_func = exec_globals.get(unique_name)
        if not callable_func or not callable(callable_func):
            raise RuntimeError("No se generó una función ejecutable válida.")
    except Exception as ex:
        raise RuntimeError(f"Error compilando función mutada: {ex}")

    # Metadatos de trazabilidad para auditoría y evolución
    metadatos = {
        "source_concepts": conceptos,
        "mutation_strategy": "basic_multiplication",
        "agent_state_snapshot": repr(agent_knowledge),
    }

    return MutatedFunction(
        name=unique_name,
        description=descripcion,
        code=codigo_fuente,
        callable_obj=callable_func,
        metadata=metadatos,
        file_path=None,
    )
