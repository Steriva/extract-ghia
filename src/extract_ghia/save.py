"""Save extracted benchmark tables to disk."""

from __future__ import annotations

import json
from pathlib import Path


def save(data: dict, output_root: Path) -> Path:
    reynolds = data["_reynolds"]

    if reynolds is None:
        case_name = "unknown_re"
    else:
        case_name = f"Re_{reynolds}"

    out = output_root / case_name
    out.mkdir(parents=True, exist_ok=True)

    table_names = [
        "vortex_map",
        "vertical_velocity",
        "horizontal_vorticity",
        "horizontal_velocity",
        "vertical_vorticity",
        "centerline_extrema",
        "centerline_u",
        "centerline_v",
    ]

    for name in table_names:
        data[name].to_csv(out / f"{name}.csv", index=False)

    metadata = {
        "reynolds": reynolds,
        "source": "AceNumerics",
        "source_url": data["_source_url"],
        "pdf_file": "source.pdf",
        "tables": table_names,
        "centerline_definition": {
            "centerline_u": "u(x=0.5, y)",
            "centerline_v": "v(x, y=0.5)",
        },
    }

    with open(out / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    return out
