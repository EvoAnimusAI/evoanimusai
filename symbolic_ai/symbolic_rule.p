# symbolic_ai/symbolic_rule.py

import ast
import logging
import sys
from typing import Any, Dict, Optional
from symbolic_ai.cond_error import CondErrorHandler

# --- Configuración de logger ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# --- Handler seguro con fallback defensivo ---
_cond_error_handler = CondErrorHandler(fallback_values={
    "pos": 0,
    "noise": "calm",
    "state": "unknown"
})

class SymbolicRule:
    """
    Representa una regla simbólica con estructura formal:
    ⟦rol:valor⟧ ⇒ acción :: condición
    """
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
        self.name = self.texto or f"{self.rol}:{self.valor}⇒{self.accion}"
        self.confidence = confidence

        print(f"[🛠 INIT] Inicializando regla con confidence={self.confidence}")
        self._validate_attributes()
        print(f"[✔️ OK] Regla inicializada correctamente: {self}")

    def _validate_attributes(self) -> None:
        if not self.rol:
            raise ValueError("[❌ VALIDATION] 'rol' no puede estar vacío.")
        if not self.valor:
            raise ValueError("[❌ VALIDATION] 'valor' no puede estar vacío.")
        if not self.accion:
            raise ValueError("[❌ VALIDATION] 'accion' no puede estar vacío.")
        print("[✅ VALIDATION] Atributos validados correctamente.")

    def _format_text(self) -> str:
        return f"⟦{self.rol}:{self.valor}⟧ ⇒ {self.accion} :: {self.condicion}"

    def evaluar(self, contexto: Dict[str, Any]) -> bool:
        print(f"\n[🔍 EVALUAR] Condición: '{self.condicion}' con contexto original: {contexto}")
        contexto_eval = dict(contexto)

        if any(k.startswith("last_action.") for k in contexto):
            print(f"[📥 CONTEXTO] Detectadas claves aplanadas de 'last_action'. Reconstruyendo...")
            la_dict = {}
            for k, v in contexto.items():
                if k.startswith("last_action."):
                    subkey = k.split(".", 1)[1]
                    la_dict[subkey] = v
                    print(f"    ↪ reconstruido last_action.{subkey} = {v}")
            contexto_eval["last_action"] = la_dict

        if "entropy" not in contexto_eval:
            if "last_action" in contexto_eval and isinstance(contexto_eval["last_action"], dict):
                contexto_eval["entropy"] = contexto_eval["last_action"].get("entropy", 0.0)
                print(f"[🛡️ PROPAGATE] entropy extraído desde last_action.entropy → {contexto_eval['entropy']}")
            elif "entropy" in contexto:
                contexto_eval["entropy"] = contexto["entropy"]
            else:
                contexto_eval["entropy"] = 0.0
                print(f"[🛡️ FALLBACK] entropy no definido. Usando valor por defecto: 0.0")

        print(f"[📦 CONTEXTO FINAL] Usado para evaluación: {contexto_eval}")

        try:
            ast.parse(self.condicion, mode='eval')
            print(f"[🧪 SYNTAX CHECK] Condición válida.")
        except Exception as e:
            logger.warning(f"[⚠️ SYNTAX ERROR] Condición inválida: {e}")
            print(f"[❌ SYNTAX ERROR] '{self.condicion}' — {e}", file=sys.stderr)
            return False

        try:
            result = _cond_error_handler.safe_eval_condition(self.condicion, contexto_eval)
            print(f"[✅ RESULTADO] Evaluación de '{self}': {result}")
            return result
        except Exception as ex:
            logger.error(f"[🔥 EVAL ERROR] {self.condicion}: {ex}")
            print(f"[❌ EVAL ERROR] '{self.condicion}' — {ex}", file=sys.stderr)
            return False

    def body(self) -> str:
        return self.accion

    def mutate(self, mutation_type: str) -> bool:
        print(f"[🧬 MUTATE] Tipo de mutación: '{mutation_type}' → {self}")
        logger.info(f"[MUTATE] Aplicando mutación '{mutation_type}' sobre regla: {self}")
        return True

    def to_dict(self) -> Dict[str, Any]:
        print(f"[📤 TO_DICT] Exportando: {self}")
        return {
            "rol": self.rol,
            "valor": self.valor,
            "accion": self.accion,
            "condicion": self.condicion,
            "texto": self.texto,
            "confidence": self.confidence
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SymbolicRule":
        print(f"[📥 FROM_DICT] Cargando desde: {data}")
        required = {"rol", "valor", "accion", "condicion"}
        if not required.issubset(data.keys()):
            missing = required - data.keys()
            raise KeyError(f"[❌ ERROR] Faltan claves requeridas: {missing}")
        return cls(
            rol=data["rol"],
            valor=data["valor"],
            accion=data["accion"],
            condicion=data.get("condicion", "True"),
            texto=data.get("texto"),
            confidence=data.get("confidence", 1.0)
        )

    @classmethod
    def parse(cls, rule_str: str) -> "SymbolicRule":
        print(f"[🔎 PARSE] Cadena de entrada: '{rule_str}'")
        try:
            normalized = rule_str.replace("⟦", "").replace("⟧", "").replace("⇒", "=>")
            condicion = "True"
            if "::" in normalized:
                main_part, condicion = map(str.strip, normalized.split("::", 1))
            else:
                main_part = normalized.strip()
            if "=>" not in main_part:
                raise ValueError("Falta '=>' en regla.")
            antecedente, accion = map(str.strip, main_part.split("=>", 1))
            if ":" not in antecedente:
                raise ValueError("Falta ':' en el antecedente.")
            rol, valor = map(str.strip, antecedente.split(":", 1))
            parsed = cls(rol=rol, valor=valor, accion=accion, condicion=condicion, texto=rule_str.strip())
            print(f"[✅ PARSE OK] Resultado: {parsed}")
            return parsed
        except Exception as e:
            logger.error(f"[❌ PARSE ERROR] '{rule_str}' — {e}")
            print(f"[❌ PARSE ERROR] '{rule_str}' — {e}", file=sys.stderr)
            raise ValueError(f"Error parsing rule string '{rule_str}': {e}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SymbolicRule):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __str__(self) -> str:
        return f"<Regla ⟦{self.rol}:{self.valor}⟧ ⇒ {self.accion} :: {self.condicion}>"

    def __repr__(self) -> str:
        return f"SymbolicRule(texto={self.texto!r})"

# Alias para compatibilidad con módulos existentes
parse_symbolic_rule = SymbolicRule.parse
