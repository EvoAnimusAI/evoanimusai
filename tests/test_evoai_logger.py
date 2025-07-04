import os
from pathlib import Path
from daemon import evoai_logger


def test_log_local_creates_and_writes(monkeypatch, tmp_path):
    # Redirigir log_local a un archivo temporal para no afectar el real
    monkeypatch.chdir(tmp_path)

    message = "🔍 Test de trazabilidad EvoAI"
    evoai_logger.log_local(message)

    # Validar que el archivo evoai_log.txt fue creado
    log_file = Path("evoai_log.txt")
    assert log_file.exists()

    # Validar que el contenido fue escrito
    with log_file.open("r", encoding="utf-8") as f:
        content = f.read()
    assert message in content
