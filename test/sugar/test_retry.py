import pytest

from cloudeasy.sugar.retry import retry, MaxRetryError


def test_retry():
    @retry([KeyError], [1, 2])
    def test_retry_func():
        raise KeyError

    with pytest.raises(MaxRetryError):
        test_retry_func()
