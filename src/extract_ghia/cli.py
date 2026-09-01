"""Command-line interface."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from extract_ghia.download import download_pdf
from extract_ghia.extract import extract_acenumerics
from extract_ghia.save import save
from extract_ghia.validate import validate


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract AceNumerics lid-driven cavity benchmark tables from PDF.",
    )

    parser.add_argument(
        "url",
        help="URL of the AceNumerics benchmark PDF",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("acenumerics_benchmarks"),
        help="Output directory",
    )

    args = parser.parse_args()

    tmp_pdf = args.output / "_download.pdf"

    print(f"Downloading:\n  {args.url}")

    download_pdf(args.url, tmp_pdf)

    print("Extracting tables...")

    data = extract_acenumerics(tmp_pdf, source_url=args.url)

    validate(data)

    output_dir = save(data, args.output)

    final_pdf = output_dir / "source.pdf"
    tmp_pdf.replace(final_pdf)

    print()
    print(f"Re = {data['_reynolds']}")
    print(f"Saved benchmark to: {output_dir}")
    print()

    for name, df in data.items():
        if isinstance(df, pd.DataFrame):
            print(f"{name:24s}: {df.shape}")


if __name__ == "__main__":
    main()
