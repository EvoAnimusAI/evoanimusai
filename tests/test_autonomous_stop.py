# tests/test_autonomous_stop.py

import pytest
from metacognition.autonomous_stop import evaluate_contextual_stop

def test_no_stop_conditions_met():
    context = {
        "recent_rewards": [1, 0.5, 0.1],
        "rejected_mutations": 5,
        "cycles_without_new_rule": 2,
        "current_entropy": 0.3
    }
    should_stop, reasons = evaluate_contextual_stop(context)
    assert should_stop is False
    assert reasons == []

def test_negative_rewards_trigger_stop():
    context = {
        "recent_rewards": [-1, -0.5, -0.3, -0.2, -0.9],
        "rejected_mutations": 0,
        "cycles_without_new_rule": 0,
        "current_entropy": 0.1
    }
    should_stop, reasons = evaluate_contextual_stop(context)
    assert should_stop is True
    assert any("negative rewards" in r for r in reasons)

def test_excessive_rejected_mutations():
    context = {
        "recent_rewards": [1, 1],
        "rejected_mutations": 11,
        "cycles_without_new_rule": 0,
        "current_entropy": 0.1
    }
    should_stop, reasons = evaluate_contextual_stop(context)
    assert should_stop is True
    assert any("rejected mutations" in r for r in reasons)

def test_symbolic_stagnation_detected():
    context = {
        "recent_rewards": [],
        "rejected_mutations": 0,
        "cycles_without_new_rule": 20,
        "current_entropy": 0.1
    }
    should_stop, reasons = evaluate_contextual_stop(context)
    assert should_stop is True
    assert any("stagnation" in r for r in reasons)

def test_entropy_threshold_triggered():
    context = {
        "recent_rewards": [],
        "rejected_mutations": 0,
        "cycles_without_new_rule": 0,
        "current_entropy": 0.96
    }
    should_stop, reasons = evaluate_contextual_stop(context)
    assert should_stop is True
    assert any("entropy" in r for r in reasons)

def test_multiple_conditions_trigger_stop():
    context = {
        "recent_rewards": [-1, -1, -1, -1, -1],
        "rejected_mutations": 15,
        "cycles_without_new_rule": 30,
        "current_entropy": 0.99
    }
    should_stop, reasons = evaluate_contextual_stop(context)
    assert should_stop is True
    assert len(reasons) == 4

def test_invalid_context_values_do_not_crash():
    context = {
        "recent_rewards": "not a list",
        "rejected_mutations": "many",
        "cycles_without_new_rule": None,
        "current_entropy": "chaotic"
    }
    should_stop, reasons = evaluate_contextual_stop(context)
    assert should_stop is False
    assert reasons == []

def test_edge_case_just_under_thresholds():
    context = {
        "recent_rewards": [-1, -1, -1, -1],  # not 5
        "rejected_mutations": 10,
        "cycles_without_new_rule": 15,
        "current_entropy": 0.95
    }
    should_stop, reasons = evaluate_contextual_stop(context)
    assert should_stop is False
    assert reasons == []
