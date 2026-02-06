#!/usr/bin/env python3
"""Seed a local Strapi instance with content from src/ Markdown files.

Usage:
  STRAPI_URL=http://localhost:1337 STRAPI_TOKEN=<admin-api-token> python3 scripts/seed_strapi.py

Notes:
- Requires `pyyaml`, `requests`, `python-frontmatter` packages.
- Works in dry-run mode with --dry-run to preview actions without POSTing.
- Uploads media files (local paths or remote URLs) to Strapi's /api/upload and attaches by id.
"""
import os
import sys
import glob
import yaml
import requests
import frontmatter
import tempfile
from urllib.parse import urlparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
STRAPI_URL = os.environ.get('STRAPI_URL','http://localhost:1337').rstrip('/')
TOKEN = os.environ.get('STRAPI_TOKEN')
HEADERS = {'Authorization': f'Bearer {TOKEN}'} if TOKEN else {}
DRY = '--dry-run' in sys.argv

COLLECTION_MAP = {
    'pages': 'pages',
    'products': 'products',
    'applications': 'applications',
    'catalogue': 'catalogues'
}

MEDIA_FIELDS = ['pdfs','pdf','images']


def upload_file(path_or_url):
    """Upload a local file or remote URL to Strapi, return file id."""
    print('Upload:', path_or_url)
    if DRY:
        return None
    files = {}
    tmp = None
    try:
        if str(path_or_url).startswith('http'):
            r = requests.get(path_or_url, stream=True, timeout=30)
            r.raise_for_status()
            suffix = Path(urlparse(path_or_url).path).suffix or ''
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            for chunk in r.iter_content(8192):
                tmp.write(chunk)
            tmp.flush()
            tmp.close()
            files['files'] = open(tmp.name, 'rb')
        else:
            files['files'] = open(str(path_or_url), 'rb')
        upload_url = f"{STRAPI_URL}/api/upload"
        rsp = requests.post(upload_url, headers=HEADERS, files=files, timeout=60)
        rsp.raise_for_status()
        res = rsp.json()
        if isinstance(res, list):
            return res[0]['id']
        elif isinstance(res, dict) and 'id' in res:
            return res['id']
        else:
            # Strapi v4 normally returns a list
            return res
    finally:
        if tmp:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass
        if 'files' in files and not files['files'].closed:
            files['files'].close()


def create_entry(collection, data):
    print('Create entry in', collection, '->', data.get('title') or data.get('slug'))
    if DRY:
        return None
    url = f"{STRAPI_URL}/api/{collection}"
    r = requests.post(url, headers={**HEADERS, 'Content-Type':'application/json'}, json={'data':data}, timeout=30)
    r.raise_for_status()
    return r.json()


def process_file(folder, path):
    fm = frontmatter.load(path)
    data = {}
    # Map simple fields
    data['title'] = fm.get('title') or fm.get('slug') or path.stem
    if 'slug' in fm:
        data['slug'] = fm['slug']
    if 'date' in fm:
        data['publishedAt'] = fm['date']
    if 'featured' in fm:
        data['featured'] = fm['featured']
    if 'seo_title' in fm:
        data['seo_title'] = fm['seo_title']
    if 'seo_description' in fm:
        data['seo_description'] = fm['seo_description']
    # content: use raw content (converted HTML) or body
    content = fm.content or ''
    # try to put into plausible field names
    data['content'] = content
    # handle media
    for mf in MEDIA_FIELDS:
        if mf in fm:
            items = fm[mf] or []
            if isinstance(items, str):
                items = [items]
            ids = []
            for it in items:
                # if looks like a relative path inside migrate/downloaded, prefer that
                if it.startswith('/'):
                    # convert to local path
                    local = ROOT / it.lstrip('/')
                    if local.exists():
                        fid = upload_file(local)
                        if fid:
                            ids.append(fid)
                        continue
                if it.startswith('http'):
                    fid = upload_file(it)
                    if fid:
                        ids.append(fid)
                    continue
                # local relative to repo
                local = ROOT / it
                if local.exists():
                    fid = upload_file(local)
                    if fid:
                        ids.append(fid)
            if ids:
                # attach by id list
                data[mf if mf != 'pdf' else 'pdfs'] = ids
    return data


def iterate_and_seed():
    for folder, api in COLLECTION_MAP.items():
        dirpath = SRC / folder
        if not dirpath.exists():
            continue
        for path in sorted(dirpath.glob('*.md')):
            data = process_file(folder, path)
            create_entry(api, data)


def main():
    if not TOKEN:
        print('Warning: no STRAPI_TOKEN set. You may need to create an API token in Strapi Settings and set STRAPI_TOKEN env var.')
    print('DRY RUN:' , DRY)
    iterate_and_seed()

if __name__ == '__main__':
    main()
