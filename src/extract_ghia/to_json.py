"""Convert extracted benchmark CSVs (benchmarks/Re_<Re>/*.csv) to a single JSON per case.

Output format mirrors the flat-dict-of-arrays style used by XLB's example data
(see XLB/examples/cfd/data/*.json): one JSON file per Reynolds number, with a
"_comment" describing provenance and one entry per benchmark table, each table
being a dict of column-name -> list of floats (as read straight off the CSV
header, e.g. "v_y0.05").
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

TABLES = ["centerline_u", "centerline_v", "vertical_velocity", "horizontal_velocity"]


def convert_case(case_dir: Path) -> dict:
    with open(case_dir / "metadata.json") as f:
        metadata = json.load(f)

    data = {
        "_comment": (
            f"Ghia-style lid-driven cavity benchmark, Re={metadata['reynolds']}. "
            f"Source: {metadata['source']} ({metadata['source_url']}). "
            f"centerline_u = u(x=0.5, y), centerline_v = v(x, y=0.5); "
            "vertical_velocity = v(x) at fixed y locations, horizontal_velocity = u(y) at fixed x locations."
        ),
        "reynolds": metadata["reynolds"],
    }

    for name in TABLES:
        df = pd.read_csv(case_dir / f"{name}.csv")
        data[name] = {col: df[col].tolist() for col in df.columns}

    return data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert extract-ghia benchmark CSVs to JSON files for XLB examples.",
    )
    parser.add_argument(
        "--benchmarks-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "benchmarks",
        help="Directory containing Re_<Re>/*.csv folders",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "benchmarks_json",
        help="Output directory for the JSON files",
    )
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    for case_dir in sorted(args.benchmarks_dir.glob("Re_*")):
        if not case_dir.is_dir():
            continue

        data = convert_case(case_dir)
        out_path = args.output / f"ghia_{case_dir.name}.json"

        with open(out_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"{case_dir.name}: wrote {out_path}")


if __name__ == "__main__":
    main()
