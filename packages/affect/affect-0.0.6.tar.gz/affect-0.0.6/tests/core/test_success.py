from typing import Any

import pytest

from affect import Failure, Result, Success
from affect.exceptions import PanicError


def test_success_is_ok() -> None:
    success_result = Success(value="Test Value")
    assert success_result.is_ok() is True


def test_failure_is_ok_and() -> None:
    success_result = Success(value="Test Value")
    assert success_result.is_ok_and(lambda x: x == "Test Value") is True


def test_success_is_err() -> None:
    success_result = Success(value="Test Value")
    assert success_result.is_err() is False


def test_success_is_err_and() -> None:
    success_result = Success(value="Test Value")
    assert success_result.is_err_and(lambda x: x == "Test Value") is False


def test_success_ok() -> None:
    success_result = Success(value="Test Value")
    assert success_result.ok() == "Test Value"


def test_success_err() -> None:
    success_result: Result[str, None] = Success(value="Test Value")
    assert success_result.err() is None


def test_success_map() -> None:
    success_result = Success(value=2)
    mapped_result = success_result.map(lambda x: x * 2)
    assert mapped_result.ok() == 4


def test_success_map_or() -> None:
    success_result = Success(value=2)
    result = success_result.map_or(0, lambda x: x * 2)
    assert result == 4


def test_success_map_or_else() -> None:
    success_result = Success(value=2)
    result = success_result.map_or_else(lambda _: 0, lambda x: x * 2)
    assert result == 4


def test_success_map_err() -> None:
    success_result = Success(value="Test Value")
    mapped_result = success_result.map_err(lambda _: "Error")
    assert mapped_result.ok() == "Test Value"


def test_success_inspect() -> None:
    success_result = Success(value="Test Value")

    def inspect_func(value: Any) -> None:
        assert value == "Test Value"

    inspected_result = success_result.inspect(inspect_func)
    assert inspected_result.ok() == "Test Value"


def test_success_inspect_err() -> None:
    success_result = Success(value="Test Value")
    inspected_result = success_result.inspect_err(lambda _: "Error")
    assert inspected_result.ok() == "Test Value"


def test_success_hash() -> None:
    success_result = Success(value="Test Value")
    assert hash(success_result) == hash((True, "Test Value"))


def test_success_iter() -> None:
    success_result = Success(value="Test Value")
    values = list(success_result.iter())
    assert values == ["Test Value"]


def test_success_iter_method() -> None:
    success_result = Success(value="Test Value")
    values = list(success_result)
    assert values == ["Test Value"]


def test_success_expect() -> None:
    success_result = Success(value="Test Value")
    assert success_result.expect("This should return the value") == "Test Value"


def test_success_unwrap() -> None:
    success_result = Success(value="Test Value")
    assert success_result.unwrap() == "Test Value"


def test_success_expect_err() -> None:
    success_result = Success(value="Test Value")
    with pytest.raises(PanicError, match="This should panic: Test Value"):
        success_result.expect_err("This should panic")


def test_success_unwrap_err() -> None:
    success_result = Success(value="Test Value")
    with pytest.raises(PanicError, match="Test Value"):
        success_result.unwrap_err()


def test_success_and() -> None:
    success_result = Success(value="Test Value")
    other_result = Success(value="Other Value")
    assert success_result.and_(other_result) == other_result


def test_success_and_failure() -> None:
    success_result = Success(value="Test Value")
    failure_result = Failure(value="Test Error")
    assert success_result.and_(failure_result) == failure_result
