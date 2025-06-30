import ast
import operator
import logging
import sys
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class SymbolicRule:
    """
    Representa una regla simbólica con rol, valor, acción y condición.

    Attributes:
        rol (str): El rol o categoría de la regla.
        valor (str): El valor asociado al rol.
        accion (str): La acción a ejecutar si la condición se cumple.
        condicion (str): Expresión booleana que define cuándo aplicar la regla.
        texto (Optional[str]): Representación textual original de la regla.
    """

    def __init__(
        self,
        rol: str,
        valor: str,
        accion: str,
        condicion: str = "True",
        texto: Optional[str] = None,
    ) -> None:
        self.rol = rol.strip()
        self.valor = valor.strip()
        self.accion = accion.strip()
        self.condicion = condicion.strip() or "True"
        self.texto = texto or self._format_text()

        self._validate_attributes()

    def _validate_attributes(self) -> None:
        if not self.rol:
            raise ValueError("El 'rol' no puede estar vacío.")
        if not self.valor:
            raise ValueError("El 'valor' no puede estar vacío.")
        if not self.accion:
            raise ValueError("La 'acción' no puede estar vacía.")
        # Condición puede ser cualquier expresión, validación en evaluación.

    def _format_text(self) -> str:
        return f"⟦{self.rol}:{self.valor}⟧ ⇒ {self.accion} :: {self.condicion}"

    def evaluar(self, contexto: Dict[str, Any]) -> bool:
        """
        Evalúa la condición de la regla en el contexto dado.

        Args:
            contexto (Dict[str, Any]): Variables disponibles para evaluar la condición.

        Returns:
            bool: True si la condición se cumple, False si no o si hay error.
        """
        try:
            # Seguridad: solo expresiones booleanas simples, sin ejecución arbitraria.
            expr = ast.parse(self.condicion, mode='eval')

            # Se puede implementar validación del AST para restringir nodos aquí.
            compiled = compile(expr, filename="<ast>", mode="eval")
            resultado = eval(compiled, {}, contexto)

            if not isinstance(resultado, bool):
                raise ValueError(f"La condición '{self.condicion}' debe evaluar a un valor booleano.")

            return resultado
        except Exception as e:
            logger.warning(f"[⚠️ Error evaluando condición '{self.condicion}']: {e}")
            print(f"Variable no definida o error evaluando condición '{self.condicion}': {e}", file=sys.stderr)
            return False

    def body(self) -> str:
        """
        Retorna la acción de la regla.
        """
        return self.accion

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializa la regla a un diccionario.
        """
        return {
            "rol": self.rol,
            "valor": self.valor,
            "accion": self.accion,
            "condicion": self.condicion,
            "texto": self.texto,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SymbolicRule":
        """
        Deserializa una regla desde un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con keys: rol, valor, accion, condicion, texto (opcional).

        Returns:
            SymbolicRule: Nueva instancia de regla.
        """
        required = {"rol", "valor", "accion", "condicion"}
        if not required.issubset(data.keys()):
            missing = required - data.keys()
            raise KeyError(f"Faltan claves requeridas para construir SymbolicRule: {missing}")

        return cls(
            rol=data["rol"],
            valor=data["valor"],
            accion=data["accion"],
            condicion=data.get("condicion", "True"),
            texto=data.get("texto"),
        )

    @classmethod
    def parse(cls, rule_str: str) -> "SymbolicRule":
        """
        Parsea una regla desde su representación en texto.

        Formato esperado:
            "rol:valor => accion :: condicion"

        Args:
            rule_str (str): Cadena con la regla.

        Returns:
            SymbolicRule: Objeto parseado.

        Raises:
            ValueError: Si la regla no cumple el formato esperado.
        """
        try:
            # Normalizar Unicode a ASCII
            normalized = rule_str.replace("⟦", "").replace("⟧", "").replace("⇒", "=>")

            condicion = "True"
            if "::" in normalized:
                parts = normalized.split("::", 1)
                if len(parts) != 2:
                    raise ValueError(f"Formato inválido, esperado solo un '::' en '{rule_str}'")
                main_part, condicion = map(str.strip, parts)
            else:
                main_part = normalized.strip()

            if "=>" not in main_part:
                raise ValueError(f"Falta '=>' en la parte principal de la regla: '{rule_str}'")

            antecedente_accion = main_part.split("=>")
            if len(antecedente_accion) != 2:
                raise ValueError(f"Formato inválido en '=>', esperado 2 partes pero hay {len(antecedente_accion)} en '{rule_str}'")

            antecedente, accion = map(str.strip, antecedente_accion)

            if ":" not in antecedente:
                raise ValueError(f"Falta ':' en el antecedente de la regla: '{rule_str}'")

            rol_valor = antecedente.split(":")
            if len(rol_valor) != 2:
                raise ValueError(f"Formato inválido en rol:valor, esperado 2 partes pero hay {len(rol_valor)} en '{rule_str}'")

            rol, valor = map(str.strip, rol_valor)

            return cls(rol=rol, valor=valor, accion=accion, condicion=condicion, texto=rule_str.strip())

        except Exception as e:
            raise ValueError(f"Error parsing rule string '{rule_str}': {e}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SymbolicRule):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __str__(self) -> str:
        return f"<Regla ⟦{self.rol}:{self.valor}⟧ ⇒ {self.accion} :: {self.condicion}>"

    def __repr__(self) -> str:
        return f"SymbolicRule(texto={self.texto!r})"
