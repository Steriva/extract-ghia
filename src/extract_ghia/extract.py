"""PDF table extraction."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import pdfplumber

from extract_ghia.parse import numeric_rows, vortex_rows


def extract_acenumerics(
    pdf_path: Path,
    source_url: str | None = None,
) -> dict[str, pd.DataFrame | int | str | None]:
    with pdfplumber.open(pdf_path) as pdf:
        if len(pdf.pages) < 4:
            raise RuntimeError(f"Expected at least 4 pages, got {len(pdf.pages)}.")

        first_page_text = pdf.pages[0].extract_text() or ""

        match = re.search(
            r"\bRe\s*=\s*([0-9]+)",
            first_page_text,
            flags=re.IGNORECASE,
        )

        reynolds = int(match.group(1)) if match else None

        # TABLE 1 — page 1: vortex map
        page = pdf.pages[0]
        text = page.extract_text(x_tolerance=2, y_tolerance=3) or ""

        table1 = pd.DataFrame(
            vortex_rows(text),
            columns=["vortex", "psi", "omega", "x", "y"],
        )

        # TABLES 2 and 3 — page 2: vertical velocity (left), vorticity (right)
        page = pdf.pages[1]
        w = page.width
        h = page.height

        left = page.crop((0, 0, 0.50 * w, h))
        right = page.crop((0.50 * w, 0, w, h))

        left_text = left.extract_text(x_tolerance=2, y_tolerance=3) or ""
        right_text = right.extract_text(x_tolerance=2, y_tolerance=3) or ""

        table2 = pd.DataFrame(
            numeric_rows(left_text, 6),
            columns=["x", "v_y0.05", "v_y0.10", "v_y0.50", "v_y0.90", "v_y0.99"],
        )

        table3 = pd.DataFrame(
            numeric_rows(right_text, 7),
            columns=[
                "x",
                "omega_y0.05",
                "omega_y0.10",
                "omega_y0.50",
                "omega_y0.90",
                "omega_y0.95",
                "omega_y1.00",
            ],
        )

        # TABLES 4 and 5 — page 3: horizontal velocity (left), vorticity (right)
        page = pdf.pages[2]
        w = page.width
        h = page.height

        left = page.crop((0, 0, 0.50 * w, h))
        right = page.crop((0.50 * w, 0, w, h))

        left_text = left.extract_text(x_tolerance=2, y_tolerance=3) or ""
        right_text = right.extract_text(x_tolerance=2, y_tolerance=3) or ""

        table4 = pd.DataFrame(
            numeric_rows(left_text, 6),
            columns=["y", "u_x0.05", "u_x0.10", "u_x0.50", "u_x0.90", "u_x0.95"],
        )

        table5 = pd.DataFrame(
            numeric_rows(right_text, 7),
            columns=[
                "y",
                "omega_x0.05",
                "omega_x0.10",
                "omega_x0.50",
                "omega_x0.90",
                "omega_x0.95",
                "omega_x1.00",
            ],
        )

        # TABLE 6 — page 4: extrema along centerlines
        page = pdf.pages[3]
        text = page.extract_text(x_tolerance=2, y_tolerance=3) or ""

        extrema_rows = numeric_rows(text, 6)
        if extrema_rows:
            extrema_rows = extrema_rows[:1]

        table6 = pd.DataFrame(
            extrema_rows,
            columns=["u_min", "y_at_u_min", "v_max", "x_at_v_max", "v_min", "x_at_v_min"],
        )

    centerline_u = table4[["y", "u_x0.50"]].rename(columns={"u_x0.50": "u"})
    centerline_v = table2[["x", "v_y0.50"]].rename(columns={"v_y0.50": "v"})

    result: dict[str, pd.DataFrame | int | str | None] = {
        "vortex_map": table1,
        "vertical_velocity": table2,
        "horizontal_vorticity": table3,
        "horizontal_velocity": table4,
        "vertical_vorticity": table5,
        "centerline_extrema": table6,
        "centerline_u": centerline_u,
        "centerline_v": centerline_v,
        "_reynolds": reynolds,
        "_source_url": source_url,
    }

    return result
