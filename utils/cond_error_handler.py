import sys
import traceback

class CondErrorHandler:
    def __init__(self):
        self.fallbacks = {}
        print("[🔧 INIT] CondErrorHandler inicializado.")

    def define_fallbacks(self, fallbacks):
        self.fallbacks = fallbacks or {}
        print(f"[⚙️ CONFIG] Fallbacks definidos: {self.fallbacks}")

    def handle(self, variable_name, context):
        try:
            if variable_name in context:
                value = context[variable_name]
                print(f"[✅ FOUND] '{variable_name}' encontrado en contexto: {value}")
                return value
            elif variable_name in self.fallbacks:
                fallback = self.fallbacks[variable_name]
                print(f"[⚠️ FALLBACK] '{variable_name}' no está en contexto, usando fallback: {fallback}")
                return fallback
            else:
                print(f"[❌ ERROR] Variable no encontrada: '{variable_name}'")
                raise KeyError(f"[🔍 TRACE] Variable '{variable_name}' no encontrada en contexto ni en fallbacks.")
        except Exception as e:
            print(f"[🔥 EXCEPTION] Excepción al manejar '{variable_name}': {str(e)}", file=sys.stderr)
            traceback.print_exc()
            raise
