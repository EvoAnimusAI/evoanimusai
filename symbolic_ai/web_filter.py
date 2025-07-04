import re
import html
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

KEY_TERMS = [
    "símbolo", "simbólica", "agente", "agentes", "mutación", "mutaciones",
    "evolución", "evolutiva", "regla", "reglas", "heurística", "razonamiento", "contexto"
]

KEY_TERMS_RE = re.compile(r'\b(' + '|'.join(re.escape(term) for term in KEY_TERMS) + r')\b', re.IGNORECASE)


class WebFilter:
    """
    Clase para filtrar y extraer conceptos simbólicos relevantes desde texto plano,
    eliminando noise y aplicando reglas específicas.
    """

    @staticmethod
    def extract_symbolic_concepts(text: str, max_concepts: int = 5) -> list[str]:
        """
        Extrae frases relevantes con carga simbólica de un texto plano.

        Args:
            text (str): Texto crudo de entrada.
            max_concepts (int): Número máximo de frases simbólicas a devolver.

        Returns:
            list[str]: Lista de frases relevantes ordenadas por relevancia.

        Raises:
            TypeError: Si `text` no es una cadena.
            ValueError: Si `max_concepts` no es positivo.
        """
        if not isinstance(text, str):
            logger.error("Entrada inválida: se esperaba una cadena de texto.")
            raise TypeError("Expected a string input")

        if not isinstance(max_concepts, int) or max_concepts <= 0:
            logger.error("max_concepts debe ser un entero positivo.")
            raise ValueError("max_concepts must be a positive integer")

        try:
            # Desescape de entidades HTML
            clean_text = html.unescape(text)
            # Eliminar etiquetas HTML
            clean_text = re.sub(r'<[^>]+>', '', clean_text)

            # Separar en líneas y limpiar espacios
            lines = [line.strip() for line in clean_text.splitlines()]

            # Filtrar líneas relevantes: longitud adecuada y presencia de palabras clave
            symbolic_lines = [
                line for line in lines
                if 10 < len(line) < 250 and KEY_TERMS_RE.search(line)
            ]

            # Ordenar por número de coincidencias con palabras clave (más relevante primero)
            ranked_lines = sorted(
                symbolic_lines,
                key=lambda l: len(KEY_TERMS_RE.findall(l)),
                reverse=True
            )

            logger.info(f"Extraction completada: {min(max_concepts, len(ranked_lines))} conceptos encontrados.")

            return ranked_lines[:max_concepts]

        except Exception as e:
            logger.exception("Error inesperado durante la extraction de conceptos simbólicos.")
            raise e


extract_symbolic_concepts = WebFilter.extract_symbolic_concepts
