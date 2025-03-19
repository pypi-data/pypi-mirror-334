from affect import Failure, Success, is_err, is_ok


def test_is_ok() -> None:
    success_result = Success(value="Test Value")
    assert is_ok(success_result) is True


def test_is_err() -> None:
    failure_result = Failure(value="Test Error")
    assert is_err(failure_result) is True
