"""Typings for affect."""

from typing import TypeVar

__all__ = ["FailureT", "O", "SuccessT", "T", "U"]

T = TypeVar("T")
SuccessT = TypeVar("SuccessT")
FailureT = TypeVar("FailureT")
U = TypeVar("U")
O = TypeVar("O")  # noqa: E741
ExceptionT = TypeVar("ExceptionT", bound=BaseException)
