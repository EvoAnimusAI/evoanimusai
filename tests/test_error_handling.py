import pytest
from unittest.mock import MagicMock, patch
from core.error_handling import ErrorHandler

def test_register_error_and_get_code():
    handler = ErrorHandler()
    handler.register_error(ValueError, "VAL_ERR")
    assert handler._get_error_code(ValueError) == "VAL_ERR"
    assert handler._get_error_code(KeyError) == "UNKNOWN_ERROR"

def test_log_exception_logs_error(caplog):
    handler = ErrorHandler()
    handler.register_error(ValueError, "VAL_ERR")

    with caplog.at_level("ERROR"):
        handler.log_exception(ValueError("test error"), context="testing")
    assert "Exception [VAL_ERR]" in caplog.text
    assert "testing" in caplog.text

def test_handle_decorator_executes_function_and_returns_value():
    handler = ErrorHandler()

    @handler.handle
    def func(x):
        return x * 2

    assert func(3) == 6

def test_handle_decorator_catches_and_logs_exception(caplog):
    handler = ErrorHandler()
    handler.register_error(ValueError, "VAL_ERR")

    @handler.handle
    def func():
        raise ValueError("fail")

    with caplog.at_level("ERROR"):
        with pytest.raises(ValueError):
            func()
    assert "Error [VAL_ERR]" in caplog.text

def test_handle_decorator_calls_on_error_callback():
    handler = ErrorHandler()
    callback = MagicMock()

    @handler.handle(on_error=callback, suppress=True)
    def func():
        raise ValueError("fail")

    func()
    callback.assert_called_once()
    assert callback.call_args[0][0].args[0] == "fail"

def test_handle_decorator_suppresses_exception_when_flagged():
    handler = ErrorHandler()

    @handler.handle(suppress=True)
    def func():
        raise RuntimeError("fail silently")

    result = func()
    assert result is None  # Should suppress and return None, not raise

def test_handle_decorator_preserves_exception_when_not_suppress():
    handler = ErrorHandler()

    @handler.handle(suppress=False)
    def func():
        raise RuntimeError("fail loudly")

    with pytest.raises(RuntimeError):
        func()

def test_handle_decorator_used_with_and_without_parameters():
    handler = ErrorHandler()

    # Without parameters
    @handler.handle
    def f1():
        return "no params"

    # With parameters
    @handler.handle(suppress=True)
    def f2():
        raise Exception("test")

    assert f1() == "no params"
    assert f2() is None

def test_on_error_callback_exception_logged(caplog):
    handler = ErrorHandler()

    def faulty_callback(exc):
        raise RuntimeError("callback fail")

    @handler.handle(on_error=faulty_callback, suppress=True)
    def func():
        raise ValueError("original fail")

    with caplog.at_level("ERROR"):
        func()
    assert "Error in on_error callback" in caplog.text
