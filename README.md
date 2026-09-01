# extract-ghia

Download AceNumerics lid-driven cavity benchmark PDFs and extract the numerical tables into clean CSV files — including Ghia-style centerline velocity profiles.

## Installation

```bash
uv sync --group dev
```

Or with pip:

```bash
pip install -e ".[dev]"
```

## Usage

```bash
uv run extract-ghia \
  "https://www.acenumerics.com/uploads/5/3/3/5/53352785/re_1000_driven_cavity_benchmark_results.pdf" \
  --output benchmarks
```

Or run the module directly:

```bash
uv run python -m extract_ghia.cli \
  "https://www.acenumerics.com/uploads/5/3/3/5/53352785/re_1000_driven_cavity_benchmark_results.pdf" \
  --output benchmarks
```

## Output

For each Reynolds number detected in the PDF, the tool writes a directory such as `benchmarks/Re_1000/` containing:

| File | Description |
|------|-------------|
| `vortex_map.csv` | Primary and secondary vortex locations (ψ, ω, x, y) |
| `vertical_velocity.csv` | v(x, y) at fixed y locations |
| `horizontal_vorticity.csv` | ω(x, y) along vertical lines |
| `horizontal_velocity.csv` | u(x, y) at fixed x locations |
| `vertical_vorticity.csv` | ω(x, y) along horizontal lines |
| `centerline_extrema.csv` | Min/max u and v along centerlines |
| `centerline_u.csv` | u(x=0.5, y) — Ghia-style vertical centerline |
| `centerline_v.csv` | v(x, y=0.5) — Ghia-style horizontal centerline |
| `metadata.json` | Source URL, Reynolds number, table list |
| `source.pdf` | Original benchmark PDF |

## Development

```bash
uv run pytest
uv run ruff check .
```

## License

MIT
