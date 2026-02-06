#!/usr/bin/env python3
"""Convert sitemap CSV to Markdown files (simple scraper + front-matter).
- Usage: python3 scripts/convert_sitemap_to_markdown.py --limit 5 --dry-run
- Reads migrate/sitemap-urls-full.csv if present, else migrate/sitemap-urls.csv
- Creates files under src/pages, src/products, src/applications
"""
import argparse
import csv
import os
from pathlib import Path
import requests
from datetime import datetime
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MIGRATE = ROOT / 'migrate'
SRC = ROOT / 'src'

HEADERS = {'User-Agent': 'Datatronic-migration-bot/1.0 (+https://datatronic.com.hk)'}


def slug_from_url(u):
    p = urlparse(u).path.strip('/')
    if not p:
        return 'home'
    return p.replace('/', '-')


def guess_collection(u):
    path = urlparse(u).path.lower()
    if '/catalogue' in path or '/products' in path:
        return 'products'
    if '/applications' in path:
        return 'applications'
    return 'pages'


def extract_text(html):
    # Lightweight extraction: prefer <main>, else first <article>, else body text
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        main = soup.find('main') or soup.find('article')
        if main:
            body = main.get_text('\n', strip=True)
        else:
            body = soup.get_text('\n', strip=True)
        title = (soup.title.string.strip() if soup.title and soup.title.string else '').strip()
        # try to find H1 as more precise title
        h1 = soup.find('h1')
        if h1 and h1.get_text(strip=True):
            title = h1.get_text(strip=True)
        return title, body
    except Exception:
        # fallback naive
        import re
        m = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
        title = m.group(1).strip() if m else ''
        # strip tags crudely
        text = re.sub(r'<[^>]+>', '\n', html)
        text = ' '.join(text.split())
        return title, text


def write_markdown(collection, slug, title, body, url):
    out_dir = SRC / collection
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{slug}.md"
    path = out_dir / filename
    # escape double quotes in title for safe YAML
    title_esc = title.replace('"', '\\"')
    fm = [
        '---',
        f"title: \"{title_esc}\"",
        f"date: {datetime.utcnow().isoformat()}Z",
        f"original_url: \"{url}\"",
        f"collection: {collection}",
        f"slug: {slug}",
        '---\n',
    ]
    content = '\n'.join(fm) + (body[:100000]) + '\n'
    with path.open('w', encoding='utf-8') as fh:
        fh.write(content)
    return path


def main(limit=5, dry_run=True):
    csv_candidates = [MIGRATE / 'sitemap-urls-full.csv', MIGRATE / 'sitemap-urls.csv']
    csv_file = None
    for c in csv_candidates:
        if c.exists():
            csv_file = c
            break
    if not csv_file:
        print('No sitemap CSV found. Run the crawler to produce sitemap-urls-full.csv')
        return 2

    urls = []
    with csv_file.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if 'url' in row and row['url'].strip():
                urls.append(row['url'].strip())
            else:
                # support single-column CSV
                val = list(row.values())[0]
                if val:
                    urls.append(val.strip())
    print(f'Using sitemap CSV: {csv_file} ({len(urls)} URLs)')
    converted = []
    for i, u in enumerate(urls):
        if limit and i >= limit:
            break
        print(f'[{i+1}/{min(limit,len(urls))}] Fetching {u}')
        try:
            r = requests.get(u, headers=HEADERS, timeout=15)
            r.raise_for_status()
            title, body = extract_text(r.text)
            if not title:
                title = slug_from_url(u)
            collection = guess_collection(u)
            slug = slug_from_url(u)
            if dry_run:
                print(f'  -> Parsed title: "{title}"; collection: {collection}; slug: {slug}')
            else:
                p = write_markdown(collection, slug, title, body, u)
                print(f'  -> Wrote {p.relative_to(ROOT)}')
            converted.append({'url':u,'title':title,'collection':collection,'slug':slug})
        except Exception as e:
            print(f'  ERROR fetching {u}: {e}')
    # write manifest
    man = MIGRATE / 'converted_manifest.csv'
    import csv as _csv
    with man.open('w', newline='', encoding='utf-8') as mfh:
        w = _csv.DictWriter(mfh, fieldnames=['url','title','collection','slug'])
        w.writeheader()
        for r in converted:
            w.writerow(r)
    print(f'Wrote manifest: {man} ({len(converted)} entries)')
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument('--dry-run', action='store_true', default=False)
    parser.add_argument('--no-dry', dest='dry_run', action='store_false')
    args = parser.parse_args()
    rc = main(limit=args.limit, dry_run=args.dry_run)
    raise SystemExit(rc)
