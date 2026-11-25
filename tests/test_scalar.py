import math

import pytest

from fieldcheck.core import ndvi_value


@pytest.mark.parametrize(
    "red,nir, q, expected", [(0.2, 0.6, 0, 0.5)]
)
def test_scalar_regular(red, nir, q, expected):
    assert ndvi_value(red, nir, q)== pytest.approx(expected)

@pytest.mark.parametrize(
    "red,nir,q", [(0.2, 0.6, 1),
                 (1.1, 0.6, 0),
                 (0.0, 0.0, 0),
                 (float("nan"), 0.6, 0),
                 (float("nan"), 0.6, 0),
                  (0.2, float("nan"), 0)]
)
def test_scalar_isnan(red, nir, q):
    assert math.isnan(ndvi_value(red, nir, q))

@pytest.mark.parametrize(
    "red,nir, q", [(0.2, 0.6, 2)]
)
def test_scalar_raise(red, nir, q):
    with pytest.raises(ValueError):
        ndvi_value(red, nir, q)