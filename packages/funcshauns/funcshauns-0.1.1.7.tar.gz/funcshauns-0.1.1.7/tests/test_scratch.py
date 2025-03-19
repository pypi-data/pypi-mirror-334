import pytest


def test_example():
    assert 1 + 1 == 2


def test_string():
    assert "hello".upper() == "HELLO"


def test_list():
    assert len([1, 2, 3]) == 3


def test_dict():
    assert "key" in {"key": "value"}


def test_exception():
    with pytest.raises(ZeroDivisionError):
        1 / 0
