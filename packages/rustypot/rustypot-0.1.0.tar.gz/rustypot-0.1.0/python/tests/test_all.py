import pytest
import rustypot


def test_sum_as_string():
    assert rustypot.sum_as_string(1, 1) == "2"
