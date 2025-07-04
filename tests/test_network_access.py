import pytest
from core.network_access import NetworkAccess

def test_authenticate_success():
    net = NetworkAccess(verbose=False)
    assert net.authenticate("A591243133418571088300454z") is True

def test_authenticate_failure():
    net = NetworkAccess(verbose=False)
    assert net.authenticate("wrong_key") is False

def test_search_web():
    net = NetworkAccess(verbose=False)
    url = net.search_web("evoai test")
    assert url.startswith("https://duckduckgo.com/?q=")
    assert "evoai+test" in url

def test_fetch_page_invalid_url():
    net = NetworkAccess(verbose=False)
    result = net.fetch_page("ftp://invalid.url")
    assert "Invalid URL" in result

def test_fetch_page_valid(monkeypatch):
    net = NetworkAccess(verbose=False)
    sample_html = "<html><body><p>Test Content</p></body></html>"

    class Response:
        def raise_for_status(self): pass
        @property
        def text(self): return sample_html

    def mock_get(*args, **kwargs):
        return Response()

    monkeypatch.setattr("requests.get", mock_get)
    content = net.fetch_page("http://valid.url")
    assert "Test Content" in content

def test_learn_from_url_and_summarize(monkeypatch):
    net = NetworkAccess(verbose=False)
    # Contenido simulado con párrafos largos (>80 chars)
    sample_content = (
        "Esta es una línea suficientemente larga para el resumen que excede los 80 caracteres "
        "y continúa sin puntos para evitar división. " * 3 + "\n" +
        "Otro párrafo que también es suficientemente largo para el resumen automático en EvoAI. " * 2
    )

    def mock_fetch_page(url):
        return sample_content

    net.fetch_page = mock_fetch_page

    net.learn_from_url("http://example.com", "TestTopic")
    assert "testtopic" in net.knowledge_base

    summary = net.summarize_topic("TestTopic")
    assert summary.startswith("-")
