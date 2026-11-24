"""Small, readable research-calculation example for the workshop."""

import math

import numpy as np


def ndvi_value(red, nir, quality):
    """Lab 2: extract the script's calculation for one observation."""
    # Move the calculation from archive/analysis.py here; return its value.
    # Preserve its existing numerical behavior for now, including its defects.
    if red + nir == 0:
        value = float("nan")
    else:
        value = (nir - red) / (nir + red)
    return value


def ndvi(red, nir, quality):
    """Supplied wrapper: apply the scalar function to equally shaped 1-D inputs."""
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
    """Lab 2: extract the script's filtering, counting, and mean calculation."""
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
    n = sum(value != 0 for value in valid_values)
    if len(valid_values) == 0:
        return None
    mean = sum(valid_values) / len(valid_values)
    print("total:", len(values), "valid:", n, "mean:", mean)
    # Return n_total, n_valid, and mean_ndvi in a dictionary.
    out = {
        "n_total": len(values),
        "n_valid": sum(value != 0 for value in valid_values),
        "mean_ndvi": sum(valid_values) / len(valid_values),
    }
    return out
    # Use None for an empty mean so the supplied CLI can reject that analysis.
    # raise NotImplementedError("Extract the summary from analysis.py")
