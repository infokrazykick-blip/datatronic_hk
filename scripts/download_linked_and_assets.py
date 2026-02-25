#!/usr/bin/env python3
"""Download a page and the pages it links to (optionally including external domains),
and download images/CSS/JS referenced by those pages. Rewrites links to local files.

Usage:
  python3 scripts/download_linked_and_assets.py --base http://localhost:3000 --page /products.html --out downloaded_site
"""

import argparse
import os
import re
import sys
from urllib.parse import urljoin, urlparse, urlunparse
import requests
from bs4 import BeautifulSoup

USER_AGENT = "datatronic-downloader/1.0 (+https://example.com)"

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def local_path_for_url(base_netloc, url, outdir):
    p = urlparse(url)
    # If external (different netloc) prefix with domain
    if p.netloc and p.netloc != base_netloc:
        prefix = os.path.join(outdir, p.netloc)
    else:
        prefix = outdir
    path = p.path.lstrip('/') or 'index.html'
    # If path ends with / make it index.html inside
    if path.endswith('/'):
        path = os.path.join(path, 'index.html')
    # Ensure filename has extension for html pages lacking extension
    return os.path.join(prefix, path)


def save_binary(url, outpath):
    try:
        r = session.get(url, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"Failed to download asset {url}: {e}")
        return False
    ensure_dir(os.path.dirname(outpath))
    with open(outpath, 'wb') as f:
        f.write(r.content)
    return True


def save_text(url, outpath):
    try:
        r = session.get(url, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"Failed to download page {url}: {e}")
        return None
    ensure_dir(os.path.dirname(outpath))
    with open(outpath, 'wb') as f:
        f.write(r.content)
    return r.content


def find_links_and_assets(html, page_url, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    assets = set()

    # anchor links
    for a in soup.select('a[href]'):
        href = a['href'].strip()
        if href.startswith('mailto:') or href.startswith('tel:') or href.startswith('javascript:') or href.startswith('#'):
            continue
        full = urljoin(page_url, href)
        links.add(full)

    # images
    for img in soup.select('img[src]'):
        src = img['src'].strip()
        if src.startswith('data:'):
            continue
        assets.add(urljoin(page_url, src))

    # scripts
    for s in soup.select('script[src]'):
        src = s['src'].strip()
        assets.add(urljoin(page_url, src))

    # stylesheets
    for l in soup.select('link[rel~=stylesheet][href]'):
        href = l['href'].strip()
        assets.add(urljoin(page_url, href))

    # inline styles with url(...) in style attributes
    for tag in soup.find_all(style=True):
        for m in re.findall(r"url\(([^)]+)\)", tag['style']):
            u = m.strip(' \"\'')
            if u and not u.startswith('data:'):
                assets.add(urljoin(page_url, u))

    return links, assets


def rewrite_urls_in_html(html, page_url, base_netloc, outdir):
    soup = BeautifulSoup(html, 'html.parser')

    def rewrite_attr(tag, attr):
        if tag.has_attr(attr):
            orig = tag[attr].strip()
            if orig.startswith('data:') or orig.startswith('javascript:'):
                return
            full = urljoin(page_url, orig)
            local = local_path_for_url(base_netloc, full, outdir)
            # compute relative path from the html's saved location
            saved_html_path = local_path_for_url(base_netloc, page_url, outdir)
            rel = os.path.relpath(local, os.path.dirname(saved_html_path))
            tag[attr] = rel.replace(os.path.sep, '/')

    for a in soup.select('a[href]'):
        href = a['href'].strip()
        if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('javascript:'):
            continue
        full = urljoin(page_url, href)
        local = local_path_for_url(base_netloc, full, outdir)
        saved_html_path = local_path_for_url(base_netloc, page_url, outdir)
        rel = os.path.relpath(local, os.path.dirname(saved_html_path))
        a['href'] = rel.replace(os.path.sep, '/')

    for img in soup.select('img[src]'):
        rewrite_attr(img, 'src')
    for s in soup.select('script[src]'):
        rewrite_attr(s, 'src')
    for l in soup.select('link[rel~=stylesheet][href]'):
        rewrite_attr(l, 'href')

    # rewrite inline style url(...) patterns
    for tag in soup.find_all(style=True):
        style = tag['style']
        def repl(m):
            url_part = m.group(1).strip(' \"\'')
            if url_part.startswith('data:'):
                return m.group(0)
            full = urljoin(page_url, url_part)
            local = local_path_for_url(base_netloc, full, outdir)
            saved_html_path = local_path_for_url(base_netloc, page_url, outdir)
            rel = os.path.relpath(local, os.path.dirname(saved_html_path)).replace(os.path.sep, '/')
            return f"url('{rel}')"
        new_style = re.sub(r"url\(([^)]+)\)", repl, style)
        tag['style'] = new_style

    return str(soup)


def download_site(base, page, outdir, include_external=True, max_depth=1):
    base_parsed = urlparse(base)
    base_netloc = base_parsed.netloc

    # normalize page
    start_url = urljoin(base, page)
    to_visit = {start_url}
    visited = set()
    pages_saved = 0
    assets_saved = set()

    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        print(f"Fetching page: {current}")
        try:
            r = session.get(current, timeout=15)
            r.raise_for_status()
            html = r.text
        except Exception as e:
            print(f"Failed to fetch page {current}: {e}")
            visited.add(current)
            continue

        links, assets = find_links_and_assets(html, current, base)

        # Decide which links to queue
        for l in links:
            p = urlparse(l)
            if (p.scheme in ('http','https')):
                if include_external or p.netloc == base_netloc:
                    if l not in visited:
                        to_visit.add(l)
        # Download assets
        for asset in assets:
            p = urlparse(asset)
            if p.scheme not in ('http','https'):
                continue
            local_asset_path = local_path_for_url(base_netloc, asset, outdir)
            if local_asset_path in assets_saved:
                continue
            ok = save_binary(asset, local_asset_path)
            if ok:
                assets_saved.add(local_asset_path)
                # if the asset is CSS, scan it for url(...) and download referenced assets
                if local_asset_path.lower().endswith('.css'):
                    try:
                        with open(local_asset_path, 'r', encoding='utf-8', errors='ignore') as f:
                            css = f.read()
                        for m in re.findall(r"url\(([^)]+)\)", css):
                            urlpart = m.strip(' \"\'')
                            if urlpart.startswith('data:'):
                                continue
                            ref = urljoin(asset, urlpart)
                            ref_local = local_path_for_url(base_netloc, ref, outdir)
                            if not os.path.exists(ref_local):
                                save_binary(ref, ref_local)
                    except Exception as e:
                        print(f"Failed parsing CSS {local_asset_path}: {e}")

        # Rewrite URLs in HTML and save
        rewritten = rewrite_urls_in_html(html, current, base_netloc, outdir)
        saved_html_path = local_path_for_url(base_netloc, current, outdir)
        if not os.path.splitext(saved_html_path)[1]:
            saved_html_path += '.html'
        ensure_dir(os.path.dirname(saved_html_path))
        with open(saved_html_path, 'w', encoding='utf-8') as f:
            f.write(rewritten)
        pages_saved += 1
        visited.add(current)

    print('\nDownload complete:')
    print(f"Pages saved: {pages_saved}")
    print(f"Assets saved: {len(assets_saved)}")
    print(f"Output directory: {os.path.abspath(outdir)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', required=True, help='Base URL (e.g. http://localhost:3000)')
    parser.add_argument('--page', default='/', help='Start page path (e.g. /products.html)')
    parser.add_argument('--out', default='downloaded_site', help='Output directory')
    parser.add_argument('--no-external', action='store_true', help='Do not fetch external domains')
    args = parser.parse_args()

    include_external = not args.no_external

    download_site(args.base, args.page, args.out, include_external=include_external)
