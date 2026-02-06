#!/usr/bin/env python3
"""Download assets listed in migrate/assets.txt to migrate/downloaded/
- Produces migrate/assets-manifest.csv with columns: url,file,size_bytes,sha256
- Warns about files >5MB and skips unchanged files by default
"""
import argparse
import csv
import hashlib
import os
from pathlib import Path
from urllib.parse import urlparse, urljoin

import requests

ROOT = Path(__file__).resolve().parents[1]
MIGRATE = ROOT / 'migrate'
OUT = MIGRATE / 'downloaded'
MANIFEST_OUT = MIGRATE / 'assets-manifest.csv'
SITE_BASE = 'https://datatronic.com.hk/'


def normalize_url(u: str) -> str:
    u = u.strip()
    if not u:
        return u
    if u.startswith('http://wp-content') or u.startswith('https://wp-content') or u.startswith('http:///'):
        # some assets may be missing host; join with site base
        return urljoin(SITE_BASE, u)
    if u.startswith('//'):
        return 'https:' + u
    if u.startswith('/wp-content'):
        return urljoin(SITE_BASE, u)
    if u.startswith('http'):
        return u
    # fallback - relative path
    return urljoin(SITE_BASE, u)


def sha256_of_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as fh:
        for chunk in iter(lambda: fh.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, outdir: Path, timeout=30, skip_existing=True) -> dict:
    urln = normalize_url(url)
    parsed = urlparse(urln)
    filename = os.path.basename(parsed.path) or hashlib.sha1(urln.encode()).hexdigest()
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / filename
    if outpath.exists() and skip_existing:
        try:
            sha = sha256_of_file(outpath)
            size = outpath.stat().st_size
            return {'url': urln, 'file': str(outpath.relative_to(ROOT)), 'size_bytes': size, 'sha256': sha, 'skipped': True}
        except Exception:
            pass
    r = requests.get(urln, stream=True, timeout=timeout)
    r.raise_for_status()
    h = hashlib.sha256()
    size = 0
    with outpath.open('wb') as fh:
        for chunk in r.iter_content(chunk_size=8192):
            if not chunk:
                continue
            fh.write(chunk)
            h.update(chunk)
            size += len(chunk)
    return {'url': urln, 'file': str(outpath.relative_to(ROOT)), 'size_bytes': size, 'sha256': h.hexdigest(), 'skipped': False}


def main(args):
    assets_file = MIGRATE / (args.assets or 'assets.txt')
    if not assets_file.exists():
        print(f"Assets file not found: {assets_file}")
        return 2
    urls = [line.strip() for line in assets_file.read_text(encoding='utf-8').splitlines() if line.strip()]
    results = []
    large = []
    for i, u in enumerate(urls, 1):
        try:
            print(f"[{i}/{len(urls)}] Downloading {u}")
            r = download(u, OUT, skip_existing=not args.force)
            results.append(r)
            if r.get('size_bytes', 0) > args.large_size * 1024 * 1024:
                large.append(r)
        except Exception as e:
            print(f"  ERROR downloading {u}: {e}")

    # write manifest
    with MANIFEST_OUT.open('w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=['url', 'file', 'size_bytes', 'sha256', 'skipped'])
        w.writeheader()
        for r in results:
            w.writerow(r)
    print(f"Wrote manifest: {MANIFEST_OUT} ({len(results)} entries)")
    if large:
        print('\nWARN: Large files detected (> {0}MB):'.format(args.large_size))
        for r in large:
            print(f"  {r['file']} - {r['size_bytes']/1024/1024:.1f}MB")
    print('\nDone')
    return 0


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Download assets listed in migrate/assets.txt')
    p.add_argument('--assets', default='assets.txt')
    p.add_argument('--force', action='store_true', help='re-download even if file exists')
    p.add_argument('--large-size', type=int, default=5, help='size in MB to warn as large')
    args = p.parse_args()
    raise SystemExit(main(args))
