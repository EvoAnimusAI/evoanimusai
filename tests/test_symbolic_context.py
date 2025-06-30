import pytest
import json
from unittest.mock import patch, mock_open
from symbolic_ai.symbolic_context import SymbolicContext
from symbolic_ai.symbolic_rule import SymbolicRule
from symbolic_ai.interpreter import ExpresionSimbolica


@pytest.fixture
def context():
    return SymbolicContext()


def test_add_expression_valid_and_invalid(context):
    exp = context.add_expression("valid expression")
    assert isinstance(exp, ExpresionSimbolica)
    assert exp in context.expressions

    exp_none = context.add_expression("")  # texto vacío devuelve None
    assert exp_none is None


def test_update_valid_and_invalid(context):
    rule_dict = {"rol": "r", "valor": "v", "accion": "a", "condicion": "c"}
    with patch("symbolic_ai.symbolic_rule.SymbolicRule.from_dict",
               return_value=SymbolicRule(rol='r', valor='v', accion='a', condicion='c')):
        data = {
            "history": [{"concept": "c1"}],
            "expressions": ["expr1", 123],  # 123 debe ignorarse
            "metacognition": [{"text": "m1", "timestamp": "t1"}],
            "rules": [rule_dict, "invalid_rule"],
            "memory": [1, 2, 3]
        }
        context.update(data)

        assert any("concept" in h for h in context.history)
        assert any(isinstance(e, ExpresionSimbolica) for e in context.expressions)
        assert any("text" in m for m in context.metacognition)
        assert isinstance(context.rules[-1], SymbolicRule)
        assert context.memory[-1] == 3


@patch("builtins.open", new_callable=mock_open, read_data='[{"rol": "r", "valor": "v", "accion": "a", "condicion": "c"}]')
@patch("os.path.isfile", return_value=True)
def test_load_rules(mock_isfile, mock_file, context):
    with patch("symbolic_ai.symbolic_rule.SymbolicRule.from_dict",
               return_value=SymbolicRule(rol='r', valor='v', accion='a', condicion='c')):
        context.load_rules("dummy_path.json")
        assert len(context.rules) > 0


@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
@patch("os.replace")
def test_save_context_success(mock_replace, mock_makedirs, mock_file, context):
    context.rules.append(SymbolicRule(rol='r', valor='v', accion='a', condicion='c'))
    context.memory.append({"mem": "val"})
    context.save_context("dummy_path.json")
    mock_makedirs.assert_called_once()
    mock_replace.assert_called_once()


@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
@patch("os.replace")
def test_save_rules_success(mock_replace, mock_makedirs, mock_file, context):
    context.rules.append(SymbolicRule(rol='r', valor='v', accion='a', condicion='c'))
    context.save_rules("dummy_rules.json")
    mock_makedirs.assert_called_once()
    mock_replace.assert_called_once()


def test_values_property(context):
    context.history.append({"k": "v"})
    context.expressions.append(ExpresionSimbolica("mock"))
    context.metacognition.append({"text": "m", "timestamp": "t"})
    context.rules.append(SymbolicRule(rol='r', valor='v', accion='a', condicion='c'))
    context.memory.append("mem")

    vals = context.values
    assert isinstance(vals, dict)
    assert "history" in vals
    assert "expressions" in vals
    assert "metacognition" in vals
    assert "rules" in vals
    assert "memory" in vals
