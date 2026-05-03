#!/usr/bin/env python3
"""Capture local site screenshots with hardened Chromium launch flags.

Usage:
  python3 scripts/capture_screenshots.py --base-url http://127.0.0.1:4173
"""

from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


PAGES = [
    ("index.html", "home.png"),
    ("book-a-call.html", "book-a-call.png"),
    ("confirmation.html", "confirmation.png"),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:4173")
    parser.add_argument("--output-dir", default="artifacts")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    chromium_flags = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--single-process",
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(args=chromium_flags)
        page = browser.new_page(viewport={"width": 1440, "height": 2400})
        for route, filename in PAGES:
            page.goto(f"{args.base_url.rstrip('/')}/{route}", wait_until="networkidle")
            page.screenshot(path=str(out_dir / filename), full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
