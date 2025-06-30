# evoai/autoprogramming/symbolic_function.py

from typing import Optional, Dict


class SymbolicFunction:
    """
    Representa una función simbólica en formato estructurado con código fuente y metadatos.
    """

    def __init__(self, name: str, code: str, metadata: Optional[Dict] = None):
        self.name = name
        self.code = code
        self.metadata = metadata or {}

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "code": self.code,
            "metadata": self.metadata
        }

    @staticmethod
    def from_dict(data: Dict) -> 'SymbolicFunction':
        return SymbolicFunction(
            name=data["name"],
            code=data["code"],
            metadata=data.get("metadata", {})
        )

    def __repr__(self):
        return f"<SymbolicFunction name={self.name} metadata={self.metadata}>"
