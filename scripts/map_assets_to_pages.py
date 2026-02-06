#!/usr/bin/env python3
"""Map assets to pages by scanning each page's original_url HTML for occurrences of asset URLs.
Produces migrate/asset_page_map.csv with columns: asset_url,page_url,page_title,local_file,size_bytes,sha256
"""
import csv
from pathlib import Path
from urllib.parse import urlparse
import requests
import re

ROOT = Path(__file__).resolve().parents[1]
MIGRATE = ROOT / 'migrate'
MANIFEST = MIGRATE / 'assets-manifest.csv'
CONVERTED = MIGRATE / 'converted_manifest.csv'
OUT = MIGRATE / 'asset_page_map.csv'
SITE_BASE = 'https://datatronic.com.hk/'


def load_assets():
    assets = []
    if MANIFEST.exists():
        with MANIFEST.open(encoding='utf-8') as fh:
            r = csv.DictReader(fh)
            for row in r:
                assets.append(row)
    else:
        # fallback: fallback to assets.txt
        assets_file = MIGRATE / 'assets.txt'
        if assets_file.exists():
            for line in assets_file.read_text(encoding='utf-8').splitlines():
                line=line.strip()
                if line:
                    assets.append({'url': line})
    return assets


def load_pages():
    pages = []
    if CONVERTED.exists():
        with CONVERTED.open(encoding='utf-8') as fh:
            r = csv.DictReader(fh)
            for row in r:
                pages.append(row)
    return pages


def find_asset_in_page(asset_url, page_url):
    try:
        r = requests.get(page_url, timeout=10)
        r.raise_for_status()
        return asset_url in r.text
    except Exception:
        return False


def main():
    assets = load_assets()
    pages = load_pages()
    mapping = []
    asset_urls = [a['url'] for a in assets]
    # For each asset try to find referring page by scanning page HTML
    for a in asset_urls:
        found = False
        for p in pages:
            page_url = p['url']
            if find_asset_in_page(a, page_url):
                mapping.append({'asset_url': a, 'page_url': page_url, 'page_title': p.get('title',''), 'local_file': '', 'size_bytes': '', 'sha256': ''})
                found = True
                break
        if not found:
            mapping.append({'asset_url': a, 'page_url': '', 'page_title': '', 'local_file': '', 'size_bytes': '', 'sha256': ''})

    # attach local file info from manifest if available
    if MANIFEST.exists():
        man = {r['url']: r for r in csv.DictReader(MANIFEST.open(encoding='utf-8'))}
        for m in mapping:
            info = man.get(m['asset_url'])
            if info:
                m['local_file'] = info.get('file','')
                m['size_bytes'] = info.get('size_bytes','')
                m['sha256'] = info.get('sha256','')

    with OUT.open('w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=['asset_url','page_url','page_title','local_file','size_bytes','sha256'])
        w.writeheader()
        for row in mapping:
            w.writerow(row)
    print('Wrote', OUT)

if __name__ == '__main__':
    main()
