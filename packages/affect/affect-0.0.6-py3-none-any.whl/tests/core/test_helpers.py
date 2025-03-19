from affect import as_result, is_failure, is_success, safe_print


def test_safe_print_value_error() -> None:
    class CustomObject:
        def __str__(self) -> str:
            msg = "This object cannot be converted to a string"
            raise ValueError(msg)

    obj = CustomObject()
    safe_print_ = as_result(ValueError)(print)

    res = safe_print_(obj)

    assert is_failure(res)
    assert str(res.unwrap_err()) == "This object cannot be converted to a string"


def test_safe_print_unknown_error() -> None:
    class Writable:
        def write(self, __s: str, /) -> int:
            msg = "This object cannot be written to"
            raise Exception(msg)  # noqa: TRY002

    obj = Writable()
    safe_print_ = as_result(Exception)(print)

    res = safe_print_("hello", file=obj)

    assert is_failure(res)
    assert isinstance(res.unwrap_err(), Exception)


def test_safe_print_normal_value() -> None:
    obj = "Hello, World!"

    res = safe_print(obj)

    assert is_success(res)
    assert res.value is None
