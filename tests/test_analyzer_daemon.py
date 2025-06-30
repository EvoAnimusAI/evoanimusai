import pytest
import tempfile
import os
import json
from monitoring.analyzer_daemon import EvoAIAnalyzerDaemon

class MockEvoAIEngine:
    def __init__(self, events):
        self._events = events

    def get_recent_events(self):
        return self._events

@pytest.fixture
def sample_events():
    return [
        {"accion": "explorar", "recompensa": 0.8, "regla_aplicada": "r1"},
        {"accion": "analizar", "recompensa": -0.2, "regla_aplicada": "r2"},
        {"accion": "explorar", "recompensa": 0.6, "regla_aplicada": "r1"},
        {"accion": "explorar", "recompensa": -0.4},  # sin regla
        {"recompensa": 1.0, "regla_aplicada": "r3"}  # sin acción
    ]

def test_analyzer_generates_correct_summary(sample_events):
    engine = MockEvoAIEngine(sample_events)
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        analyzer = EvoAIAnalyzerDaemon(engine, interval=1, log_file=tmpfile.name)
        summary = analyzer.run_cycle()

        assert summary is not None
        assert "actions" in summary
        assert "rules" in summary

        # Verificamos acción "explorar"
        explorar = summary["actions"].get("explorar")
        assert explorar is not None
        assert abs(explorar["average_reward"] - (0.8 + 0.6 - 0.4) / 3) < 1e-5
        assert explorar["count"] == 3

        # Verificamos regla "r1"
        r1 = summary["rules"].get("r1")
        assert r1 is not None
        assert abs(r1["average_reward"] - (0.8 + 0.6) / 2) < 1e-5
        assert r1["recommendation"] == "keep/mutate"

        # Verificamos regla "r2"
        r2 = summary["rules"].get("r2")
        assert r2 is not None
        assert r2["recommendation"] == "prune"

        # Verificamos archivo generado
        with open(tmpfile.name, 'r') as f:
            file_summary = json.load(f)
            assert file_summary == summary

    os.remove(tmpfile.name)

def test_analyzer_handles_empty_events():
    engine = MockEvoAIEngine([])
    analyzer = EvoAIAnalyzerDaemon(engine, interval=1)
    summary = analyzer.run_cycle()
    assert summary is None  # No debe analizar si no hay eventos
