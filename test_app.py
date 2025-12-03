# test_app.py
import math
import pytest
from add import add

def test_add_integers():
    assert add(1, 2) == 3
    assert add(-1, 5) == 4

def test_add_floats():
    assert pytest.approx(add(1.2, 3.4), rel=1e-9) == 4.6

def test_add_integer_and_float():
    assert pytest.approx(add(1, 2.5), rel=1e-9) == 3.5

def test_add_zero():
    assert add(0, 0) == 0
    assert add(0, 5) == 5

def test_add_large_numbers():
    assert add(10**12, 1) == 10**12 + 1

def test_add_returns_number_type():
    r = add(1, 2)
    assert isinstance(r, (int, float))

def test_add_nan_behavior():
    # adding NaN should produce NaN (propagate)
    nan = float('nan')
    assert math.isnan(add(nan, 1)) or math.isnan(add(1, nan))