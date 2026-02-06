#!/usr/bin/env python3
"""Produce suggested human-friendly slugs from the converted manifest.
- Run: python3 scripts/suggest_slug_mappings.py
- Output: migrate/suggested_slugs.csv (original_url, current_slug, suggested_slug)
"""
import csv
from pathlib import Path
import re
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
MIGRATE = ROOT / 'migrate'
MANIFEST = MIGRATE / 'converted_manifest.csv'
OUT = MIGRATE / 'suggested_slugs.csv'

def slugify(text):
    # simple ASCII-safe slug: lowercase, replace non-alnum with -, collapse dashes
    s = unquote(text)
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-{2,}', '-', s).strip('-')
    if not s:
        s = 'page'
    return s[:80]

rows = []
if MANIFEST.exists():
    with MANIFEST.open() as fh:
        r = csv.DictReader(fh)
        for row in r:
            url = row['url']
            cur = row['slug']
            # propose suggestion: based on last path segment
            path = urlparse(url).path.strip('/')
            last = path.split('/')[-1] if path else 'home'
            sugg = slugify(last)
            # prefix with lang if `en-` detected
            if cur.startswith('en-') and not sugg.startswith('en-'):
                sugg = 'en-' + sugg
            rows.append({'url':url,'current_slug':cur,'suggested_slug':sugg})
    with OUT.open('w',newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['url','current_slug','suggested_slug'])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print('Wrote', OUT)
else:
    print('Manifest not found at', MANIFEST)
