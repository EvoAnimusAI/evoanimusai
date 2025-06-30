import json
from unittest import mock
from daemon import evoai_state


def test_get_symbolic_context_keys():
    ctx = evoai_state.get_symbolic_context()
    assert "noise" in ctx and "state" in ctx
    assert ctx["noise"] in ["neutral", "harmonic", "chaos", "tension", "calm", None]
    assert ctx["state"] in ["normal", "active", "stressed"]


def test_update_cycle_counter_increments():
    original = evoai_state.cycle_counter
    updated = evoai_state.update_cycle_counter()
    assert updated == original + 1


@mock.patch("os.makedirs")
def test_ensure_logs_dir(mock_makedirs):
    evoai_state.ensure_logs_dir()
    mock_makedirs.assert_called_once_with("knowledge_logs", exist_ok=True)


@mock.patch("builtins.open", new_callable=mock.mock_open)
@mock.patch("os.path.exists", return_value=True)
def test_load_memory_reads_json(mock_exists, mock_open_file):
    data = {"name": "test", "steps": []}
    handle = mock_open_file.return_value
    handle.__enter__.return_value.read.return_value = json.dumps(data)
    evoai_state.load_memory()
    assert evoai_state.current_function["name"] == "test"


@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_save_memory_writes_json(mock_open_file):
    evoai_state.current_function = {"name": "mock_func", "steps": []}
    evoai_state.save_memory()
    mock_open_file.assert_called_once_with("symbolic_memory.json", "w", encoding="utf-8")


@mock.patch("daemon.evoai_state.logger")
def test_execute_directed_function_logs_actions(mock_logger):
    func = {
        "name": "cool_down",
        "steps": [{"action": "breathe", "param": 1}]
    }
    evoai_state.execute_directed_function(func)
    mock_logger.info.assert_any_call("[Directed] Ejecutando función dirigida: cool_down")
    mock_logger.info.assert_any_call("  • Acción: breathe | Param: 1")


@mock.patch("builtins.open", new_callable=mock.mock_open)
@mock.patch("os.path.exists", return_value=False)
def test_save_to_symbolic_memory_creates_file(mock_exists, mock_open_file):
    evoai_state.save_to_symbolic_memory("print('hello')")
    mock_open_file.assert_called_once_with("data/symbolic_memory.json", "w", encoding="utf-8")


@mock.patch("os.path.exists", return_value=True)
def test_save_to_symbolic_memory_appends(mock_exists):
    existing = [{"code": "a=1", "origin": "mutation"}]
    m_open = mock.mock_open(read_data=json.dumps(existing))

    with mock.patch("builtins.open", m_open):
        evoai_state.save_to_symbolic_memory("b=2")

    # Une todas las llamadas a write para reconstruir el JSON escrito
    written_calls = m_open().write.call_args_list
    written_str = "".join(call.args[0] for call in written_calls)

    written_json = json.loads(written_str)
    assert written_json[0]["code"] == "a=1"
    assert written_json[1]["code"] == "b=2"
    assert written_json[1]["origin"] == "mutation"
