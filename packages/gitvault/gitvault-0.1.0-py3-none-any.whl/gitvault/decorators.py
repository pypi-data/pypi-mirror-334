"""Decorator utilities for exception handling and logging.

This module provides decorators that can be used to standardize
exception handling and logging across the password sync package.
"""

import logging
import functools
from typing import Callable, TypeVar, Any
from .custom_exceptions import DataFetchError, DecryptionError, PrivateKeyNotFoundError

T = TypeVar('T')

def handle_exceptions(logger: logging.Logger) -> Callable:
    """Decorator for standardized exception handling and logging.
    
    Wraps functions to provide consistent exception handling and logging
    behavior across the application. Catches and logs specific exceptions
    while maintaining the original stack trace.
    
    Args:
        logger: Logger instance to use for error logging.
        
    Returns:
        Callable: Decorated function with exception handling.
        
    Example:
        @handle_exceptions(logger)
        def my_function():
            # Function code here
            pass
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return func(*args, **kwargs)
            except (DataFetchError, DecryptionError, PrivateKeyNotFoundError ) as e:
                logger.error(f"{func.__name__} failed: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {str(e)}", exc_info=True)
                raise DecryptionError(f"Unexpected error: {str(e)}")
        return wrapper
    return decorator
