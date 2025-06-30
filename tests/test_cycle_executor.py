import pytest
import json
from unittest.mock import MagicMock, patch, mock_open, ANY
import daemon.evoai_cycle_executor as cycle_exec

@pytest.fixture
def mock_dependencies():
    agent = MagicMock()
    agent.name = "Agent007"
    agent.memory.retrieve_all.return_value = [{"func": "dummy"}]

    engine = MagicMock()
    engine.symbolic_learning_engine.apply_rules.return_value = []  # Cambiado a vacío para activar mutate_parent
    engine.symbolic_learning_engine.cross_reinforcement = MagicMock()
    engine.last_mutated_function = None

    executor = MagicMock()
    executor.execute.return_value = True
    executor.monitor = MagicMock()

    decision_engine = MagicMock()
    decision_engine.evaluate.return_value = "mutate_parent"  # Se usa cuando apply_rules devuelve vacío

    context = MagicMock()
    context.update = MagicMock()
    context.add_concept = MagicMock()

    consciousness = MagicMock()
    consciousness.evaluate_integrity = MagicMock()

    codex = MagicMock()
    codex.network.learn_from_url = MagicMock()
    codex.network.summarize_topic.return_value = "Resumen de evolución simbólica."
    codex.execute_auto_rewrite.return_value = (True, "log_path.log")

    current_function = {"name": "sample", "steps": [{"action": "print", "param": "ok"}]}
    preferred_topics = ["topic1", "topic2"]

    return {
        "agent": agent,
        "engine": engine,
        "executor": executor,
        "decision_engine": decision_engine,
        "context": context,
        "consciousness": consciousness,
        "codex": codex,
        "current_function": current_function,
        "preferred_topics": preferred_topics
    }

@patch("daemon.evoai_cycle_executor.open", new_callable=mock_open, read_data='[]')
@patch("daemon.evoai_cycle_executor.os.path.exists", return_value=True)
@patch("daemon.evoai_cycle_executor.get_symbolic_context", return_value={"noise": "calm", "state": "active"})
@patch("daemon.evoai_cycle_executor.evaluate_mutation", return_value=True)
@patch("daemon.evoai_cycle_executor.mutate_parent_function", return_value={"name": "mutated_func", "steps": []})
@patch("daemon.evoai_cycle_executor.extract_symbolic_concepts", return_value=["vida", "entropía"])
@patch("daemon.evoai_cycle_executor.log_entry")
@patch("daemon.evoai_cycle_executor.log_agent")
@patch("daemon.evoai_cycle_executor.log_decision")
@patch("daemon.evoai_cycle_executor.log_synthesis")
@patch("daemon.evoai_cycle_executor.log_concept")
@patch("daemon.evoai_cycle_executor.log_rewrite")
@patch("daemon.evoai_cycle_executor.show_symbolic_state")
@patch("daemon.evoai_cycle_executor.time.time", return_value=1234567.89)
@patch("daemon.evoai_cycle_executor.logger")
def test_run_cycle_execution_full(
    mock_logger,
    mock_time,
    mock_show,
    mock_rewrite,
    mock_concept,
    mock_synthesis,
    mock_decision,
    mock_agent_log,
    mock_entry,
    mock_extract_concepts,
    mock_mutate_parent,
    mock_eval_mut,
    mock_get_ctx,
    mock_exists,
    mock_open_file,
    mock_dependencies
):
    deps = mock_dependencies

    cycle_exec.run_cycle(
        cycle=10,
        context=deps["context"],
        engine=deps["engine"],
        agent=deps["agent"],
        executor=deps["executor"],
        decision_engine=deps["decision_engine"],
        consciousness=deps["consciousness"],
        codex=deps["codex"],
        current_function=deps["current_function"],
        preferred_topics=deps["preferred_topics"]
    )

    # Validaciones estructurales
    deps["engine"].run_iteration.assert_called_once_with(10)
    deps["agent"].perceive.assert_called_once()
    deps["context"].update.assert_called_once()
    deps["executor"].execute.assert_called_once()
    deps["executor"].monitor.log.assert_called_once_with(10, ANY, ANY, ANY)

    # Validaciones simbólicas
    mock_logger.info.assert_any_call("🤖 Iniciando ciclo #10")
    mock_logger.info.assert_any_call("⚡ Decisión simbólica: mutate_parent")
    mock_logger.info.assert_any_call("📚 Resumen adquirido: Resumen de evolución simbólica.")

    # Validar mutaciones dirigidas
    mock_mutate_parent.assert_called_once()
    mock_eval_mut.assert_called()

    # Validar escritura en archivo
    handle = mock_open_file()
    handle.write.assert_called()

    # Validar que la memoria simbólica fue guardada
    found = any(
        "[SECURITY] Memoria simbólica actualizada correctamente" in str(call)
        for call in mock_logger.info.call_args_list
    )
    assert found, "No se encontró el log de actualización de memoria simbólica"
