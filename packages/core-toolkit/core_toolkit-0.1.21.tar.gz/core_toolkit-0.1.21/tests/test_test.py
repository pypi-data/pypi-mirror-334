import pytest

from core_kit.test_pckg.xxx import xxx


def test_pytest() -> None:
    with pytest.raises(ZeroDivisionError):
        _ = 1 / 0


def test_xxx():
    assert "xxx" == xxx("x")
