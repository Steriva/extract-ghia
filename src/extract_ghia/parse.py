"""Text parsing utilities for AceNumerics benchmark PDFs."""

from __future__ import annotations

import re

NUMBER_RE = re.compile(
    r"""
    ^[+-]?
    (?:
        (?:\d+(?:\.\d*)?) |
        (?:\.\d+)
    )
    (?:[Ee][+-]?\d+)?$
    """,
    re.VERBOSE,
)


def is_number(value: str) -> bool:
    return bool(NUMBER_RE.match(value.strip()))


def to_float(value: str) -> float:
    value = value.strip()

    # AceNumerics uses "-" for undefined wall/corner values.
    if value in {"-", "–", "—"}:
        return float("nan")

    return float(value)


def numeric_rows(text: str, ncols: int) -> list[list[float]]:
    """
    Extract rows consisting of exactly ncols numerical values.
    A standalone '-' is treated as NaN.
    """
    rows = []

    for line in text.splitlines():
        tokens = line.strip().split()

        if len(tokens) != ncols:
            continue

        valid = all(
            is_number(token) or token in {"-", "–", "—"}
            for token in tokens
        )

        if not valid:
            continue

        rows.append([to_float(token) for token in tokens])

    return rows


def vortex_rows(text: str) -> list[list]:
    """
    Parse Table 1:
        vortex_name psi omega x y
    """
    rows = []

    for line in text.splitlines():
        tokens = line.strip().split()

        if len(tokens) != 5:
            continue

        name = tokens[0]

        # Known notation used by AceNumerics:
        # PV, BR1, BR2, ..., BL1, ...
        if not re.fullmatch(r"(?:PV|BR\d+|BL\d+)", name):
            continue

        if not all(is_number(x) for x in tokens[1:]):
            continue

        rows.append([name] + [float(x) for x in tokens[1:]])

    return rows
