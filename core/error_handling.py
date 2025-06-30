import logging
from typing import Callable, Type, Optional, Any, Dict
import functools

class ErrorHandler:
    """
    Centralized error handling utility.

    Provides structured exception handling, logging,
    and optional callback execution on errors.

    Attributes:
        logger (logging.Logger): Logger instance for error reporting.
        error_registry (Dict[Type[BaseException], str]): Map of exception types to error codes or messages.
    """

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self.error_registry: Dict[Type[BaseException], str] = {}

    def register_error(self, error_type: Type[BaseException], error_code: str) -> None:
        """
        Registers an error type with a specific code or label.

        Args:
            error_type (Type[BaseException]): Exception class to register.
            error_code (str): Identifier or code for the error type.
        """
        self.error_registry[error_type] = error_code
        self.logger.debug(f"Registered error type {error_type} with code '{error_code}'")

    def handle(
        self,
        func: Optional[Callable] = None,
        *,
        on_error: Optional[Callable[[Exception], Any]] = None,
        suppress: bool = False,
    ) -> Callable:
        """
        Decorator to wrap function calls with error handling.
        Supports usage with or without parameters.

        Usage:
            @handler.handle
            def func(...):
                ...

            or

            @handler.handle(suppress=True, on_error=callback)
            def func(...):
                ...

        Args:
            func (Optional[Callable]): Function to wrap (if decorator used without parameters).
            on_error (Optional[Callable[[Exception], Any]]): Optional callback to execute on error.
            suppress (bool): If True, suppresses exceptions and logs only.

        Returns:
            Callable: Wrapped function with error handling.
        """

        def decorator(f: Callable) -> Callable:
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    error_code = self._get_error_code(type(e))
                    self.logger.error(f"Error [{error_code}]: {e}", exc_info=True)
                    if on_error:
                        try:
                            on_error(e)
                        except Exception as cb_exc:
                            self.logger.error(f"Error in on_error callback: {cb_exc}", exc_info=True)
                    if not suppress:
                        raise
                    return None

            return wrapper

        if func is not None:
            # Decorator used without parameters
            return decorator(func)

        # Decorator used with parameters
        return decorator

    def _get_error_code(self, exc_type: Type[BaseException]) -> str:
        """
        Retrieves the registered error code for a given exception type.

        Args:
            exc_type (Type[BaseException]): Exception class.

        Returns:
            str: Error code or 'UNKNOWN_ERROR' if not registered.
        """
        return self.error_registry.get(exc_type, "UNKNOWN_ERROR")

    def log_exception(self, exc: Exception, context: Optional[str] = None) -> None:
        """
        Logs an exception with optional contextual information.

        Args:
            exc (Exception): The exception instance.
            context (Optional[str]): Additional context for logging.
        """
        context_msg = f"Context: {context}" if context else "No additional context"
        error_code = self._get_error_code(type(exc))
        self.logger.error(f"Exception [{error_code}]: {exc} | {context_msg}", exc_info=True)
