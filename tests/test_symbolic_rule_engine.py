import os
import json
import pytest
from symbolic_ai.symbolic_rule_engine import SymbolicRuleEngine
from symbolic_ai.symbolic_rule import SymbolicRule


@pytest.fixture
def engine(tmp_path):
    # Usar archivo temporal para no afectar reglas reales
    file_path = tmp_path / "rules_test.json"
    engine = SymbolicRuleEngine(auto_load=False, rules_file=str(file_path))
    engine._add_default_rules()
    engine.save_to_file(str(file_path))
    return engine


def test_add_rule(engine):
    rule_str = "test_role:test_val => test_action() :: True"
    engine.add_rule(rule_str)
    found = any(r.accion == "test_action()" for rules in engine.rules.values() for r in rules)
    assert found


def test_add_duplicate_rule(engine):
    rule = SymbolicRule("role", "val", "action()", "True")
    engine.add_rule(rule)
    count_before = sum(len(rules) for rules in engine.rules.values())
    engine.add_rule(rule)  # Duplicate
    count_after = sum(len(rules) for rules in engine.rules.values())
    assert count_before == count_after  # No se duplica


def test_update_rule(engine):
    rule = next(iter(next(iter(engine.rules.values()))))
    engine.update_rule(rule, reward=10)  # No error, log update


def test_evaluate_rules(engine):
    contexto = {"noise": "calm", "pos": 1}
    matched = engine.evaluate(contexto)
    assert all(isinstance(r, SymbolicRule) for r in matched)
    assert any(r.rol == "action" for r in matched)


def test_get_rule_by_action(engine):
    action_name = "move_forward"
    rule = engine.get_rule_by_action(action_name)
    assert rule is not None
    assert rule.accion == action_name


def test_assert_fact_logging(engine, caplog):
    fact = {"noise": "calm"}
    with caplog.at_level("INFO"):
        matched = engine.assert_fact(fact)
        assert len(matched) > 0
        assert "reglas activadas" in caplog.text


def test_save_and_load(tmp_path):
    file_path = tmp_path / "rules.json"
    engine1 = SymbolicRuleEngine(auto_load=False, rules_file=str(file_path))
    engine1._add_default_rules()
    engine1.save_to_file(str(file_path))

    engine2 = SymbolicRuleEngine(auto_load=False, rules_file=str(file_path))
    engine2.load_from_file(str(file_path))

    # Mismas reglas tras cargar
    assert sum(len(r) for r in engine1.rules.values()) == sum(len(r) for r in engine2.rules.values())


def test_load_corrupt_file(tmp_path, caplog):
    file_path = tmp_path / "corrupt.json"
    file_path.write_text("{ invalid json }")

    engine = SymbolicRuleEngine(auto_load=False, rules_file=str(file_path))

    with caplog.at_level("ERROR"):
        engine.load_from_file(str(file_path))
        assert "Error cargando reglas" in caplog.text or "Borrando reglas corruptas" in caplog.text


def test_reset(engine):
    engine.reset()
    assert len(engine.rules) > 0
