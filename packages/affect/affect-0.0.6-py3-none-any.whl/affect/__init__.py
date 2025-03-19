"""Affect is a Python library for building robust applications."""

from affect.core import (
    Failure,
    Result,
    Success,
    as_async_result,
    as_result,
    is_err,
    is_failure,
    is_ok,
    is_success,
    safe_print,
)
from affect.version import __version__

__all__ = [
    "Failure",
    "Result",
    "Success",
    "__version__",
    "as_async_result",
    "as_result",
    "is_err",
    "is_failure",
    "is_ok",
    "is_success",
    "safe_print",
]
