
import pytest

def test_sq_sum():
    from layoutimg.arith import sq_sum
    assert sq_sum([2.0, 1.0]) == pytest.approx(5.0)