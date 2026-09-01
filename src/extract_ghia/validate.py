"""Sanity checks for extracted benchmark data."""

from __future__ import annotations


def validate(data: dict) -> None:
    """
    Basic sanity checks so PDF layout changes do not silently produce
    corrupted benchmark data.
    """
    required = {
        "vortex_map": 1,
        "vertical_velocity": 10,
        "horizontal_vorticity": 10,
        "horizontal_velocity": 10,
        "vertical_vorticity": 10,
        "centerline_extrema": 1,
    }

    for name, minimum_rows in required.items():
        n = len(data[name])

        if n < minimum_rows:
            raise RuntimeError(
                f"{name}: extracted only {n} rows; expected at least {minimum_rows}. "
                "The PDF layout may have changed."
            )

    for name in ("vertical_velocity", "horizontal_vorticity"):
        values = data[name]["x"].dropna()

        if not values.between(0, 1).all():
            raise RuntimeError(f"{name}: invalid x coordinates detected.")

    for name in ("horizontal_velocity", "vertical_vorticity"):
        values = data[name]["y"].dropna()

        if not values.between(0, 1).all():
            raise RuntimeError(f"{name}: invalid y coordinates detected.")
