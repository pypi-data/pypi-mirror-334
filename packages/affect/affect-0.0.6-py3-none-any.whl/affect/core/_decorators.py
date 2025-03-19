import functools
from collections.abc import Awaitable, Callable
from typing import ParamSpec, TypeVar, cast, overload

from affect.core._core import Failure, Result, Success
from affect.typings import ExceptionT

P = ParamSpec("P")
T = TypeVar("T")


@overload
def as_result(
    exception: None = None,
    /,
) -> Callable[[Callable[P, T]], Callable[P, Result[T, Exception]]]: ...


@overload
def as_result(
    exception: type[ExceptionT],
    /,
    *exceptions: type[ExceptionT],
) -> Callable[[Callable[P, T]], Callable[P, Result[T, ExceptionT]]]: ...


def as_result(
    exception: type[ExceptionT] | None = None,
    *exceptions: type[ExceptionT],
) -> Callable[
    [Callable[P, T]],
    Callable[P, Result[T, ExceptionT] | Result[T, Exception]],
]:
    """Make a decorator to turn a function into one that returns a ``Result``.

    Regular return values are turned into ``Ok(return_value)``. Raised
    exceptions of the specified exception type(s) are turned into ``Err(exc)``.
    """
    exceptions_ = cast(
        tuple[type[ExceptionT], ...],
        (exception, *exceptions) if exception else exceptions,
    )

    def decorator(
        f: Callable[P, T],
    ) -> Callable[P, Result[T, ExceptionT] | Result[T, Exception]]:
        """Decorator to turn a function into one that returns a ``Result``."""

        @functools.wraps(f)
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> Result[T, ExceptionT] | Result[T, Exception]:
            exceptions__ = exceptions_ or Exception
            try:
                return Success(f(*args, **kwargs))
            except exceptions__ as exc:
                return cast(Result[T, ExceptionT] | Result[T, Exception], Failure(exc))

        return wrapper

    return decorator


@overload
def as_async_result(
    exception: None = None,
    /,
) -> Callable[
    [Callable[P, Awaitable[T]]],
    Callable[P, Awaitable[Result[T, Exception]]],
]: ...


@overload
def as_async_result(
    exception: type[ExceptionT],
    /,
    *exceptions: type[ExceptionT],
) -> Callable[
    [Callable[P, Awaitable[T]]],
    Callable[P, Awaitable[Result[T, ExceptionT]]],
]: ...


def as_async_result(
    exception: type[ExceptionT] | None = None,
    *exceptions: type[ExceptionT],
) -> Callable[
    [Callable[P, Awaitable[T]]],
    Callable[P, Awaitable[Result[T, ExceptionT] | Result[T, Exception]]],
]:
    """Make a decorator to turn a function into one that returns a ``Result``.

    Regular return values are turned into ``Ok(return_value)``. Raised
    exceptions of the specified exception type(s) are turned into ``Err(exc)``.
    """
    exceptions_ = cast(
        tuple[type[ExceptionT], ...],
        (exception, *exceptions) if exception else exceptions,
    )

    def decorator(
        f: Callable[P, Awaitable[T]],
    ) -> Callable[P, Awaitable[Result[T, ExceptionT] | Result[T, Exception]]]:
        """Decorator to turn a function into one that returns a ``Result``."""

        @functools.wraps(f)
        async def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> Result[T, ExceptionT] | Result[T, Exception]:
            exceptions__ = exceptions_ or Exception
            try:
                return Success(await f(*args, **kwargs))
            except exceptions__ as exc:
                return cast(Result[T, ExceptionT] | Result[T, Exception], Failure(exc))

        return wrapper

    return decorator
