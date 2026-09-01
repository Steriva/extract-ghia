"""Backward-compatible entry point. Prefer: extract-ghia or python -m extract_ghia.cli."""

from extract_ghia.cli import main

if __name__ == "__main__":
    main()
