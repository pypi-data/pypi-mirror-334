import pytest

from affect import Failure, Result, Success
from affect.exceptions import PanicError


def test_failure_is_ok() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.is_ok() is False


def test_failure_is_ok_and() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.is_ok_and(lambda x: x == "Test Error") is False


def test_failure_is_err() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.is_err() is True


def test_failure_is_err_and() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.is_err_and(lambda x: x == "Test Error") is True


def test_failure_ok() -> None:
    failure_result: Result[None, str] = Failure(value="Test Error")
    assert failure_result.ok() is None


def test_failure_err() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.err() == "Test Error"


def test_failure_map() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.map(lambda x: x + " mapped") is failure_result


def test_failure_map_or() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.map_or("default", lambda x: x + " mapped") == "default"


def test_failure_map_or_else() -> None:
    failure_result = Failure(value="Test Error")
    assert (
        failure_result.map_or_else(lambda x: x + " default", lambda x: x + " mapped")
        == "Test Error default"
    )


def test_failure_map_err() -> None:
    failure_result = Failure(value="Test Error")
    mapped_failure = failure_result.map_err(lambda x: x + " mapped")
    assert mapped_failure.err() == "Test Error mapped"


def test_failure_inspect() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.inspect(lambda x: print(x)) is failure_result


def test_failure_inspect_err() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.inspect_err(lambda x: print(x)) is failure_result


def test_failure_hash() -> None:
    failure_result = Failure(value="Test Error")
    assert hash(failure_result) == hash((False, "Test Error"))


def test_failure_iter() -> None:
    failure_result = Failure(value="Test Error")
    assert list(failure_result.iter()) == [None]


def test_failure_iter_method() -> None:
    failure_result = Failure(value="Test Error")
    values = list(failure_result)
    assert values == [None]


def test_failure_expect() -> None:
    failure_result = Failure(value="Test Error")
    with pytest.raises(PanicError, match="This should panic: Test Error"):
        failure_result.expect("This should panic")


def test_failure_unwrap() -> None:
    failure_result = Failure(value="Test Error")
    with pytest.raises(PanicError, match="Unwrapping a failure: Test Error"):
        failure_result.unwrap()


def test_failure_expect_err() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.expect_err("This should return the error") == "Test Error"


def test_failure_unwrap_err() -> None:
    failure_result = Failure(value="Test Error")
    assert failure_result.unwrap_err() == "Test Error"


def test_failure_and() -> None:
    failure_result = Failure(value="Test Error")
    other_result = Success(value="Other Value")
    assert failure_result.and_(other_result) == failure_result


def test_failure_and_failure() -> None:
    failure_result = Failure(value="Test Error")
    other_failure_result = Failure(value="Another Error")
    assert failure_result.and_(other_failure_result) == failure_result
