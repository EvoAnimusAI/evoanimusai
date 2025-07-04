# symbolic_env.py

from types import SimpleNamespace
import traceback

class SymbolicEnvironment:
    """
    Clase de alto nivel para construir, validar y preparar el entorno simbólico
    antes de la evaluación de reglas en EvoAI.
    """

    def __init__(self, raw_context: dict):
        print("[🧱 symbolic_env] Inicializando entorno simbólico...")
        self.context = self._validate_context(raw_context)
        self.namespace = self._dict_to_namespace(self.context)
        print("[✅ symbolic_env] Entorno simbólico listo para evaluación.")

    def get_eval_context(self):
        """Devuelve el contexto preparado como objeto evaluable."""
        return self.namespace

    def _validate_context(self, ctx: dict) -> dict:
        """Verifica y completa variables clave del contexto."""
        print("[🔎 symbolic_env] Validando contexto simbólico...")

        defaults = {
            'pos': 0,
            'noise': 'calm',
            'state': 'unknown',
            'entropy': 0.0,
            'last_action': {
                'action': 'noop',
                'reason': 'No valid symbolic decision',
                'entropy': 0.0
            }
        }

        for key, default_value in defaults.items():
            if key not in ctx or ctx[key] is None:
                print(f"[⚠️ FALLBACK] Variable '{key}' no definida o es None → asignado: {default_value}")
                ctx[key] = default_value

        print("[✅ symbolic_env] Validación de contexto completada.")
        return ctx

    def _dict_to_namespace(self, d):
        """Convierte diccionarios anidados en objetos SimpleNamespace."""
        try:
            if isinstance(d, dict):
                return SimpleNamespace(**{k: self._dict_to_namespace(v) for k, v in d.items()})
            return d
        except Exception as e:
            print("[🔥 symbolic_env] Error al convertir a namespace:")
            traceback.print_exc()
            raise RuntimeError("Fallo en dict_to_namespace") from e
