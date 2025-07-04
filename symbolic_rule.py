# symbolic_ai/symbolic_rule.py
import ast
import logging
import sys
from typing import Any, Dict, Optional
from symbolic_ai.cond_error import CondErrorHandler

logger = logging.getLogger(__name__)
_cond_error_handler = CondErrorHandler(fallback_values={"pos": 0, "noise": "calm", "state": "unknown"})

class SymbolicRule:
    """Representa una regla simbólica con rol, valor, acción, condición y un nivel de confianza."""

    def __init__(
        self,
        rol: str,
        valor: str,
        accion: str,
        condicion: str = "True",
        texto: Optional[str] = None,
        confidence: float = 1.0
    ) -> None:
        self.rol = rol.strip()
        self.valor = valor.strip()
        self.accion = accion.strip()
        self.condicion = condicion.strip() or "True"
        self.texto = texto or self._format_text()
        self.confidence = confidence
        self._validate_attributes()
        print(f"[✔️ INIT RULE] {self} [confidence={self.confidence}]")

    def _validate_attributes(self) -> None:
        if not self.rol:
            raise ValueError("El 'rol' no puede estar vacío.")
        if not self.valor:
            raise ValueError("El 'valor' no puede estar vacío.")
        if not self.accion:
            raise ValueError("The 'action' field cannot be empty.")

    def _format_text(self) -> str:
        return f"⟦{self.rol}:{self.valor}⟧ ⇒ {self.accion} :: {self.condicion}"

    def evaluar(self, contexto: Dict[str, Any]) -> bool:
        print(f"[🔍 EVALUAR] Condición: '{self.condicion}' con contexto: {contexto}")
        try:
            ast.parse(self.condicion, mode='eval')
        except Exception as e:
            logger.warning(f"[⚠️ SYNTAX] Error en condición '{self.condicion}': {e}")
            print(f"[❌ SYNTAX ERROR] '{self.condicion}' — {e}", file=sys.stderr)
            return False
        try:
            result = _cond_error_handler.safe_eval_condition(self.condicion, contexto)
            print(f"[✅ RESULT] Regla '{self}' evaluada como: {result}")
            return result
        except Exception as ex:
            print(f"[❌ EVAL ERROR] '{self.condicion}' — {ex}", file=sys.stderr)
            return False

    def body(self) -> str:
        print(f"[📦 BODY] Acción de la regla: {self.accion}")
        return self.accion

    def mutate(self, mutation_type: str) -> bool:
        print(f"[🧬 MUTATE] Tipo: {mutation_type} sobre {self}")
        logger.info(f"[MUTATE] Aplicando mutación tipo '{mutation_type}' sobre regla: {self}")
        return True

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "rol": self.rol,
            "valor": self.valor,
            "accion": self.accion,
            "condicion": self.condicion,
            "texto": self.texto,
            "confidence": self.confidence,
        }
        print(f"[📤 TO_DICT] Exportando: {d}")
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SymbolicRule":
        print(f"[📥 FROM_DICT] Entrada: {data}")
        required = {"rol", "valor", "accion", "condicion"}
        if not required.issubset(data.keys()):
            missing = required - data.keys()
            raise KeyError(f"Faltan claves requeridas para construir SymbolicRule: {missing}")
        instancia = cls(
            rol=data["rol"],
            valor=data["valor"],
            accion=data["accion"],
            condicion=data.get("condicion", "True"),
            texto=data.get("texto"),
            confidence=data.get("confidence", 1.0)
        )
        print(f"[✅ FROM_DICT OK] → {instancia}")
        return instancia

    @classmethod
    def parse(cls, rule_str: str) -> "SymbolicRule":
        print(f"[🔎 PARSE] Entrada cruda: {rule_str}")
        try:
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
                raise ValueError(f"Formato inválido en '=>': se esperaban 2 partes pero hay {len(antecedente_accion)}")

            antecedente, accion = map(str.strip, antecedente_accion)
            if ":" not in antecedente:
                raise ValueError(f"Falta ':' en el antecedente de la regla: '{rule_str}'")

            rol_valor = antecedente.split(":")
            if len(rol_valor) != 2:
                raise ValueError(f"Formato inválido en rol:valor, esperado 2 partes pero hay {len(rol_valor)}")

            rol, valor = map(str.strip, rol_valor)
            parsed = cls(rol=rol, valor=valor, accion=accion, condicion=condicion, texto=rule_str.strip())
            print(f"[✅ PARSED] → {parsed}")
            return parsed

        except Exception as e:
            print(f"[❌ PARSE ERROR] Entrada: '{rule_str}' — {e}", file=sys.stderr)
            raise ValueError(f"Error parsing rule string '{rule_str}': {e}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SymbolicRule):
            return NotImplemented
        eq = self.to_dict() == other.to_dict()
        print(f"[🤝 EQUALS] ¿{self} == {other}? → {eq}")
        return eq

    def __str__(self) -> str:
        return f"<Regla ⟦{self.rol}:{self.valor}⟧ ⇒ {self.accion} :: {self.condicion}>"

    def __repr__(self) -> str:
        return f"SymbolicRule(texto={self.texto!r})"
