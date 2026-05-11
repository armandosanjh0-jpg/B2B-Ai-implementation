#!/usr/bin/env python3
"""Basic production checks for static site pages."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob('*.html'))

class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.forms: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs):
        d = dict(attrs)
        if tag == 'a' and 'href' in d:
            self.links.append(d['href'])
        if tag == 'form':
            self.forms.append(d)

errors: list[str] = []

existing = {p.name for p in HTML_FILES}
for page in HTML_FILES:
    parser = LinkParser()
    parser.feed(page.read_text(encoding='utf-8'))

    for href in parser.links:
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
            continue
        target = href.split('#', 1)[0]
        if target and target not in existing:
            errors.append(f"{page.name}: broken internal link -> {href}")

    if page.name == 'book-a-call.html':
        if not parser.forms:
            errors.append('book-a-call.html: missing form element')
        for form in parser.forms:
            if form.get('method', '').lower() != 'post':
                errors.append('book-a-call.html: form method should be POST')
            if not form.get('action'):
                errors.append('book-a-call.html: form action missing')

if errors:
    for err in errors:
        print(f"ERROR: {err}")
    sys.exit(1)

print(f"OK: validated {len(HTML_FILES)} HTML files")
