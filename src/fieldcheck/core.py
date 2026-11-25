"""Small, readable research-calculation example for the workshop."""

import logging
import math

import numpy as np

logger = logging.getLogger(__name__)


def ndvi_value(red, nir, quality):
    """Return one index, or NaN for an excluded/invalid measurement.

    Bands are already-scaled, dimensionless reflectances in [0, 1].
    Quality is 0 (clear) or 1 (excluded); other codes raise ValueError.
    Negative and zero NDVI values remain valid.

    Parameters
    ----------
    red : float
        value of red
    nir : float
        near infrared value
    quality : int
        quality of the value

    Returns
    -------
    float
        gives back the calculated nvdi value
    """
    # Move the calculation from archive/analysis.py here; return its value.
    # Preserve its existing numerical behavior for now, including its defects.
    if quality not in [0, 1]:
        raise ValueError
    if (
        red + nir <= 0
        or quality != 0
        or not (math.isfinite(nir) and 0 <= nir <= 1)
        or not (math.isfinite(red) and 0 <= red <= 1)
    ):
        value = float("nan")
    else:
        value = (nir - red) / (nir + red)
    return value


def ndvi(red, nir, quality):
    """
    Compute NDVI (Normalized Difference Vegetation Index) for multiple pixels.

    Ts, returning a vector of NDVI values.

    Parameters
    ----------
    red : array_like
        Array of red band reflectance values (0 to 1). Must be 1-D.
    nir : array_like
        Array of near-infrared (NIR) band reflectance values (0 to 1). Must be 1-D
        and of the same shape as `red`.
    quality : array_like
        Array of quality flags (e.g., 0 = valid, non-zero = invalid). Must be 1-D
        and of the same shape as `red`.

    Returns
    -------
    ndvi_values : numpy.ndarray
        1-D array of NDVI values computed as `(nir - red) / (nir + red)` for valid
        pixels. Returns `nan` for invalid pixels (e.g., when `quality != 0` or
        `nir + red <= 0`).

    Raises
    ------
    ValueError
        If `red`, `nir`, or `quality` are not 1-D arrays of the same shape.

    See Also
    --------
    ndvi_value : Scalar version of this function for single values.
    numpy.ndarray : Array data type used for input and output.

    Notes
    -----
    - NDVI is defined as: (NIR - Red) / (NIR + Red)
    - Values range from -1 to +1.
    - Returns `nan` for invalid or zero-sum cases.
    - Input arrays must be finite and in [0, 1] (enforced in `ndvi_value`).

    Examples
    --------
    >>> red = [0.2, 0.3, 0.0]
    >>> nir = [0.6, 0.4, 0.1]
    >>> quality = [0, 0, 1]  # third pixel is invalid
    >>> ndvi(red, nir, quality)
    array([ 0.5       , -0.16666667,        nan])
    """
    red = np.asarray(red, dtype=float)
    nir = np.asarray(nir, dtype=float)
    quality = np.asarray(quality)
    if red.ndim != 1 or nir.shape != red.shape or quality.shape != red.shape:
        raise ValueError("red, nir, and quality must be equally shaped 1-D arrays")
    result = []
    for index in range(len(red)):
        result.append(ndvi_value(red[index], nir[index], quality[index]))
    return np.array(result, dtype=float)


def summarize(values):
    """
    Count finite values and compute their mean.

    Parameters
    ----------
    values : array_like
        1-D array of numeric values (e.g., NDVI).

    Returns
    -------
    dict
        Dictionary with:
        - 'n_total': total number of values
        - 'n_valid': number of finite values
        - 'mean_ndvi': mean of finite values, or None if none

    Examples
    --------
    >>> summarize([1.0, 2.0, float('nan'), 3.0])
    {'n_total': 4, 'n_valid': 3, 'mean_ndvi': 2.0}
    """
    values = np.asarray(values, dtype=float)
    if values.ndim != 1:
        raise ValueError("values must be 1-D")
    # Supplied boundary: the extracted loop works with ordinary Python numbers.
    values = values.tolist()
    # Move the finite-value loop and summary calculations here.
    valid_values = []
    for value in values:
        if math.isfinite(value):
            valid_values.append(value)
    n = len(valid_values)
    mean = sum(valid_values) / n if n else None
    out = {
        "n_total": len(values),
        "n_valid": n,
        "mean_ndvi": mean,
    }
    return out
    # Use None for an empty mean so the supplied CLI can reject that analysis.
    # raise NotImplementedError("Extract the summary from analysis.py")
