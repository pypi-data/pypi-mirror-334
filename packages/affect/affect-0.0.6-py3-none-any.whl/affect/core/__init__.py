"""Core module for affect."""

from affect.core._core import (
    Failure,
    Result,
    Success,
    is_err,
    is_failure,
    is_ok,
    is_success,
)
from affect.core._decorators import as_async_result, as_result
from affect.core._helpers import safe_print

__all__ = [
    "Failure",
    "Result",
    "Success",
    "as_async_result",
    "as_result",
    "is_err",
    "is_failure",
    "is_ok",
    "is_success",
    "safe_print",
]
