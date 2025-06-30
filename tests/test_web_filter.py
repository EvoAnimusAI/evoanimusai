# tests/test_web_filter.py

import pytest
from symbolic_ai.web_filter import extract_symbolic_concepts

def test_extract_symbolic_concepts_basic():
    text = """
    Este es un sistema basado en agentes que usa reglas simbólicas.
    La evolución del conocimiento ocurre por mutaciones heurísticas.
    Nada relevante aquí.
    <p>Texto con HTML que menciona un símbolo emergente</p>
    Agente autónomo percibe el entorno simbólico y actúa.
    """
    result = extract_symbolic_concepts(text)
    assert isinstance(result, list)
    assert len(result) <= 5
    assert any("simbólica" in r or "agente" in r.lower() for r in result)

def test_extract_symbolic_concepts_max_limit():
    text = "\n".join([
        "Agente simbólico 1",
        "Mutación evolutiva 2",
        "Símbolo 3",
        "Evolución 4",
        "Regla 5",
        "Otra simbólica 6",
    ])
    result = extract_symbolic_concepts(text, max_concepts=3)
    assert len(result) == 3

def test_extract_symbolic_concepts_html_cleaning():
    html_text = """
    <html><body>
    <p>La <b>mutación</b> simbólica ocurre en el <i>contexto</i>.</p>
    <div>No simbólico</div>
    </body></html>
    """
    result = extract_symbolic_concepts(html_text)
    assert any("mutación" in r.lower() for r in result)
    assert all("<" not in r and ">" not in r for r in result)

def test_extract_symbolic_concepts_type_error():
    with pytest.raises(TypeError):
        extract_symbolic_concepts(1234)

def test_extract_symbolic_concepts_no_matches():
    text = "Esto es un texto completamente irrelevante para el análisis simbólico."
    result = extract_symbolic_concepts(text)
    assert isinstance(result, list)
    assert len(result) == 0
