import unittest
from unittest.mock import MagicMock, patch
from runtime.executor import Executor
import traceback

class TestExecutor(unittest.TestCase):
    def setUp(self):
        # Mock agente, motor y demás dependencias para el Executor
        self.mock_agent = MagicMock()
        self.mock_agent.entropy = 0.0
        self.mock_agent.rewards = [1, 1, 1, 1, 1]

        self.mock_engine = MagicMock()
        self.mock_engine.decide.return_value = "mock_action"
        self.mock_engine.save_rules = MagicMock()

        self.executor = Executor(agent=self.mock_agent, engine=self.mock_engine)

    def test_run_calls_symbolic_step(self):
        with patch.object(self.executor, '_run_symbolic_step') as mock_symbolic_step:
            self.executor.run(steps=3)
            self.assertEqual(mock_symbolic_step.call_count, 3)

    def test_run_respects_environment_termination(self):
        self.executor.environment = MagicMock()
        self.executor._run_environment_step = MagicMock(return_value=False)
        with patch('runtime.executor.log_event') as mock_log:
            self.executor.run(steps=10)
            mock_log.assert_any_call("EXECUTOR", "Execution terminated by environment.", level="INFO")

    def test_run_handles_keyboard_interrupt(self):
        with patch.object(self.executor, '_run_symbolic_step', side_effect=KeyboardInterrupt):
            with patch('runtime.executor.log_event') as mock_log:
                with patch.object(self.executor, 'stop') as mock_stop:
                    self.executor.run(steps=1)
                    mock_log.assert_any_call("EXECUTOR", "Execution manually interrupted.", level="WARNING")
                    mock_stop.assert_called_once()

    def test_run_handles_stop_iteration(self):
        with patch.object(self.executor, '_run_symbolic_step', side_effect=StopIteration("stop")):
            with patch('runtime.executor.log_event') as mock_log:
                with patch.object(self.executor, 'stop') as mock_stop:
                    self.executor.run(steps=1)
                    mock_log.assert_any_call("EXECUTOR", "Autonomous stop triggered: stop", level="INFO")
                    mock_stop.assert_called_once()

    def test_run_handles_generic_exception(self):
        with patch.object(self.executor, '_run_symbolic_step', side_effect=Exception("error")):
            with patch('runtime.executor.log_event') as mock_log:
                with patch.object(self.executor, 'stop') as mock_stop:
                    self.executor.run(steps=1)
                    mock_log.assert_any_call("EXECUTOR", "Unexpected error: error", level="ERROR")
                    mock_log.assert_any_call("TRACEBACK", unittest.mock.ANY, level="ERROR")
                    mock_stop.assert_called_once()

    def test_detect_stagnation(self):
        self.mock_agent.rewards = [0, -1, 0, -2, -1]
        self.assertTrue(self.executor._detect_stagnation())

        self.mock_agent.rewards = [1, 1, 1, 1, 1]
        self.assertFalse(self.executor._detect_stagnation())

        self.mock_agent.rewards = [1, 0, 0]
        self.assertFalse(self.executor._detect_stagnation())

if __name__ == "__main__":
    unittest.main()
