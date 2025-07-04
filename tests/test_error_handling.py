import logging
import pytest
from core.error_handling import ErrorHandler

def test_register_and_get_error_code():
    handler = ErrorHandler()
    handler.register_error(ValueError, "VAL_ERR")
    assert handler._get_error_code(ValueError) == "VAL_ERR"
    assert handler._get_error_code(KeyError) == "UNKNOWN_ERROR"

def test_log_exception_logs_error(caplog):
    handler = ErrorHandler()
    handler.register_error(ValueError, "VAL_ERR")
    with caplog.at_level(logging.ERROR):
        handler.log_exception(ValueError("test error"), context="testing context")
    assert "[Excepción - VAL_ERR]" in caplog.text
    assert "testing context" in caplog.text

def test_handle_decorator_catches_and_logs_error(caplog):
    handler = ErrorHandler()
    handler.register_error(RuntimeError, "RUNTIME")
    @handler.handle
    def func():
        raise RuntimeError("fail")
    with pytest.raises(RuntimeError):
        func()
    # Now with suppress=True
    @handler.handle(suppress=True)
    def func_suppress():
        raise RuntimeError("fail suppressed")
    result = func_suppress()
    assert result is None
    assert "fail suppressed" in caplog.text

def test_handle_with_on_error_callback(caplog):
    handler = ErrorHandler()
    called = {}
    def on_error(e):
        called["called"] = True
        assert isinstance(e, RuntimeError)
    @handler.handle(on_error=on_error, suppress=True)
    def func():
        raise RuntimeError("callback test")
    func()
    assert called.get("called") is True

def test_handle_mutation_error_logs(caplog):
    handler = ErrorHandler()
    handler.register_error(Exception, "EXC")
    with caplog.at_level(logging.ERROR):
        handler.handle_mutation_error(Exception("mutation fail"), "mutate_func")
    assert "Mutación fallida en función: mutate_func" in caplog.text

def test_critical_shutdown_calls_sys_exit(monkeypatch):
    handler = ErrorHandler()
    exited = {}
    def fake_exit(code):
        exited["code"] = code
        raise SystemExit(code)
    monkeypatch.setattr("sys.exit", fake_exit)
    with pytest.raises(SystemExit):
        handler.critical_shutdown("critical failure")
    assert exited["code"] == 100

def test_wrap_safe_execution_catches_exceptions(caplog):
    handler = ErrorHandler()
    @handler.wrap_safe_execution
    def func():
        raise ValueError("wrapped fail")
    result = func()
    assert result is None
    assert "wrapped fail" in caplog.text

