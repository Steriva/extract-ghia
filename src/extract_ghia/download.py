"""PDF download utilities."""

from __future__ import annotations

from pathlib import Path

import requests


def download_pdf(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 AceNumerics benchmark downloader",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=60,
    )
    response.raise_for_status()

    content_type = response.headers.get("content-type", "")

    if "pdf" not in content_type.lower() and not response.content.startswith(b"%PDF"):
        raise RuntimeError(
            f"Downloaded object does not appear to be a PDF: content-type={content_type!r}"
        )

    destination.write_bytes(response.content)
