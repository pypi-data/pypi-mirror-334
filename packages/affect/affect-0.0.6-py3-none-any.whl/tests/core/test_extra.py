import pytest

from affect import as_async_result, as_result


@as_result()
def divide(a: float, b: float) -> float:
    return a / b


def test_divide_success() -> None:
    result = divide(10, 2)
    assert result.is_ok()
    assert result.unwrap() == 5.0


def test_divide_by_zero() -> None:
    result = divide(10, 0)
    assert result.is_err()
    assert isinstance(result.unwrap_err(), Exception)


def test_divide_with_non_number() -> None:
    @as_result(TypeError)
    def divide(a: float, b: float) -> float:
        return a / b

    result = divide(10, "a")  # type: ignore[arg-type]
    assert result.is_err() is True
    assert isinstance(result.unwrap_err(), TypeError)


def test_divide_with_multiple_exceptions() -> None:
    @as_result(ZeroDivisionError, TypeError)
    def safe_divide(a: float, b: float) -> float:
        return a / b

    result = safe_divide(10, 0)
    assert result.is_err() is True
    assert isinstance(result.unwrap_err(), ZeroDivisionError)


@as_async_result()
async def async_divide(a: float, b: float) -> float:
    return a / b


@pytest.mark.asyncio
async def test_async_divide_success() -> None:
    result = await async_divide(10, 2)
    assert result.is_ok()
    assert result.unwrap() == 5.0


@pytest.mark.asyncio
async def test_async_divide_by_zero() -> None:
    result = await async_divide(10, 0)
    assert result.is_err()
    assert isinstance(result.unwrap_err(), Exception)


@pytest.mark.asyncio
async def test_async_divide_with_non_number() -> None:
    @as_async_result(TypeError)
    async def async_divide(a: float, b: float) -> float:
        return a / b

    result = await async_divide(10, "a")  # type: ignore[arg-type]
    assert result.is_err() is True
    assert isinstance(result.unwrap_err(), TypeError)


@pytest.mark.asyncio
async def test_async_divide_with_multiple_exceptions() -> None:
    @as_async_result(ZeroDivisionError, TypeError)
    async def safe_async_divide(a: float, b: float) -> float:
        return a / b

    result = await safe_async_divide(10, 0)
    assert result.is_err() is True
    assert isinstance(result.unwrap_err(), ZeroDivisionError)
