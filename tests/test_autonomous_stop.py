import pytest
from metacognition.autonomous_stop import evaluate_contextual_stop

@pytest.mark.parametrize("context,expected_stop,expected_reasons", [
    # Caso 1: Nada gatilla el stop
    (
        {
            "recent_rewards": [1.0, 0.5, -0.1, 0.2],
            "rejected_mutations": 3,
            "cycles_without_new_rule": 5,
            "current_entropy": 0.5,
        },
        False, []
    ),
    # Caso 2: 5 recompensas negativas seguidas
    (
        {
            "recent_rewards": [-1.0, -0.9, -1.2, -0.5, -2.0],
        },
        True, ["Too many recent negative rewards."]
    ),
    # Caso 3: Mutaciones rechazadas excesivamente
    (
        {
            "rejected_mutations": 15
        },
        True, ["Excessive number of rejected mutations."]
    ),
    # Caso 4: Estancamiento simbólico
    (
        {
            "cycles_without_new_rule": 20
        },
        True, ["Symbolic stagnation detected."]
    ),
    # Caso 5: Entropía alta
    (
        {
            "current_entropy": 0.96
        },
        True, ["High entropy detected — system behaving chaotically."]
    ),
    # Caso 6: Múltiples condiciones activas
    (
        {
            "recent_rewards": [-1, -2, -3, -4, -5],
            "rejected_mutations": 12,
            "cycles_without_new_rule": 25,
            "current_entropy": 0.98
        },
        True, [
            "Too many recent negative rewards.",
            "Excessive number of rejected mutations.",
            "Symbolic stagnation detected.",
            "High entropy detected — system behaving chaotically."
        ]
    ),
])
def test_evaluate_contextual_stop(context, expected_stop, expected_reasons):
    stop, reasons = evaluate_contextual_stop(context)
    assert stop == expected_stop
    assert set(reasons) == set(expected_reasons)
