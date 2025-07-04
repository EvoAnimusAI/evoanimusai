import json
import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from daemon import evoai_mutation_handler


def test_get_symbolic_context_returns_valid_structure():
    ctx = evoai_mutation_handler.get_symbolic_context()
    assert isinstance(ctx, dict)
    assert "noise" in ctx and "state" in ctx


@patch("daemon.evoai_mutation_handler.evaluate_mutation", return_value=True)
@patch("daemon.evoai_mutation_handler.mutate_parent_function")
def test_perform_directed_mutation_accepts_and_updates(mutate_fn, eval_fn, tmp_path):
    current_function = {"steps": [{"action": "think"}]}
    new_function = {"steps": [{"action": "evolve"}]}
    mutate_fn.return_value = new_function

    path = tmp_path / "symbolic_memory.json"
    with patch("builtins.open", mock_open()) as mock_file, \
         patch("daemon.evoai_mutation_handler.open", mock_open()) as f_mock, \
         patch("daemon.evoai_mutation_handler.os.path.exists", return_value=True), \
         patch("daemon.evoai_mutation_handler.json.dump"):

        evoai_mutation_handler.perform_directed_mutation(current_function, ["ethics"], {})
        assert current_function == new_function


@patch("daemon.evoai_mutation_handler.generate_and_save_mutation", return_value="fake_mut.py")
@patch("daemon.evoai_mutation_handler.evaluate_mutation", return_value=True)
def test_perform_symbolic_mutation_accepts(fake_eval, fake_generate, tmp_path):
    fake_file = tmp_path / "data/mutated_functions/fake_mut.py"
    fake_file.parent.mkdir(parents=True, exist_ok=True)
    fake_file.write_text("print('mutated')")

    with patch("daemon.evoai_mutation_handler.os.path.exists", return_value=True), \
         patch("daemon.evoai_mutation_handler.open", mock_open(read_data="print('mutated')")), \
         patch("daemon.evoai_mutation_handler.save_to_symbolic_memory") as save_mock:
        evoai_mutation_handler.perform_symbolic_mutation(10, 10, context={})
        save_mock.assert_called()


@patch("daemon.evoai_mutation_handler.mutate_function", return_value={"mut": "ok"})
def test_perform_internal_memory_mutation(mut_fn):
    agent = MagicMock()
    agent.memory.retrieve_all.return_value = [{"m": 1}]
    engine = MagicMock()
    evoai_mutation_handler.perform_internal_memory_mutation(agent, context={}, engine=engine)
    assert engine.last_mutated_function == {"mut": "ok"}


def test_save_to_symbolic_memory_appends(tmp_path):
    path = tmp_path / "data/symbolic_memory.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("[]", encoding="utf-8")

    with patch("daemon.evoai_mutation_handler.os.path.exists", return_value=True), \
         patch("daemon.evoai_mutation_handler.open", mock_open()) as m_open, \
         patch("daemon.evoai_mutation_handler.json.load", return_value=[]), \
         patch("daemon.evoai_mutation_handler.json.dump") as j_dump:
        evoai_mutation_handler.save_to_symbolic_memory("print('X')")
        j_dump.assert_called()
