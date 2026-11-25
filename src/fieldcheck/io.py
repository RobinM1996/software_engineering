"""Read a tiny CSV; data validation belongs at the input boundary."""

import csv
from pathlib import Path

import numpy as np


def read_csv(path: Path):
    """
    Read red, nir, and quality columns from CSV.

    Additional columns (e.g., id) are allowed.

    Parameters
    ----------
    path : Path
        Path to input CSV file.

    Returns
    -------
    tuple of (np.ndarray, np.ndarray, np.ndarray)
        red, nir, and quality arrays (float, float, int).

    Raises
    ------
    ValueError
        If required columns are missing or values are invalid.
    """
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if not {"red", "nir", "quality"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV requires red,nir,quality columns")
        red, nir, quality = [], [], []
        for row_number, row in enumerate(reader, 2):
            try:
                red.append(float(row["red"]))
                nir.append(float(row["nir"]))
                quality.append(int(row["quality"]))
            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"invalid numeric value on CSV row {row_number}"
                ) from exc
    return np.array(red), np.array(nir), np.array(quality, dtype=int)
