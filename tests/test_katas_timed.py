from katas.timed import timer


def test_timer_returns_function_result_and_preserves_metadata(capsys):
    @timer
    def add(first: int, second: int) -> int:
        """Add two numbers."""
        return first + second

    assert add(2, second=3) == 5
    assert add.__name__ == "add"
    assert add.__doc__ == "Add two numbers."
    assert capsys.readouterr().out.startswith("'add' took ")


def test_timer_propagates_exceptions():
    @timer
    def fail() -> None:
        raise RuntimeError("failure")

    try:
        fail()
    except RuntimeError as error:
        assert str(error) == "failure"
    else:
        raise AssertionError("timer should propagate the wrapped exception")
