#!/usr/bin/env python3
"""Fetch content from a Strapi instance and write Markdown files into src/ for Eleventy.
Usage: set STRAPI_URL (e.g., http://localhost:1337) and STRAPI_TOKEN (optional) then run.
"""
import os
import requests
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
STRAPI_URL = os.environ.get('STRAPI_URL','http://localhost:1337')
TOKEN = os.environ.get('STRAPI_TOKEN')
HEADERS = {'Authorization': f'Bearer {TOKEN}'} if TOKEN else {}

COLLECTIONS = {
    'pages': 'src/pages',
    'products': 'src/products',
    'applications': 'src/applications',
    'catalogues': 'src/catalogue'
}

os.makedirs(SRC / 'pages', exist_ok=True)
os.makedirs(SRC / 'products', exist_ok=True)
os.makedirs(SRC / 'applications', exist_ok=True)
os.makedirs(SRC / 'catalogue', exist_ok=True)


def to_yaml_frontmatter(d):
    return '---\n' + yaml.safe_dump(d, sort_keys=False, allow_unicode=True) + '---\n\n'


def write_markdown(folder, slug, fm, content_html):
    path = SRC / folder / f"{slug}.md"
    with path.open('w', encoding='utf-8') as fh:
        fh.write(to_yaml_frontmatter(fm))
        # write content as HTML; downstream we can convert to markdown if desired
        fh.write(content_html or '')
    print('Wrote', path)


def fetch_collection(name):
    url = f"{STRAPI_URL}/api/{name}?pagination[pageSize]=100&populate=deep"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    data = r.json().get('data', [])
    return data


def extract_media_urls(media_field):
    if not media_field:
        return []
    urls = []
    if isinstance(media_field, list):
        for m in media_field:
            if m and 'attributes' in m and m['attributes'].get('url'):
                urls.append(m['attributes']['url'])
    else:
        m = media_field
        if m and 'data' in m:
            d = m['data']
            if isinstance(d, list):
                for it in d:
                    if it and 'attributes' in it and it['attributes'].get('url'):
                        urls.append(it['attributes']['url'])
            elif d and 'attributes' in d and d['attributes'].get('url'):
                urls.append(d['attributes']['url'])
    return urls


def process_items(name, folder):
    items = fetch_collection(name)
    for it in items:
        attrs = it.get('attributes', {})
        title = attrs.get('title') or attrs.get('name') or 'untitled'
        slug = attrs.get('slug') or (title.lower().replace(' ','-'))
        fm = {
            'title': title,
            'slug': slug,
            'date': attrs.get('publishedAt') or attrs.get('createdAt'),
            'featured': attrs.get('featured', False),
            'seo_title': attrs.get('seo_title',''),
            'seo_description': attrs.get('seo_description','')
        }
        # extract pdfs and images
        pdfs = extract_media_urls(attrs.get('pdfs') or attrs.get('pdf') or attrs.get('pdf_file'))
        images = extract_media_urls(attrs.get('images'))
        if pdfs:
            fm['pdfs'] = pdfs
        if images:
            fm['images'] = images
        # content
        content = attrs.get('content') or attrs.get('description') or attrs.get('body') or ''
        # Strapi rich text is HTML; write as-is
        write_markdown(folder, slug, fm, content)


def main():
    for name, folder in COLLECTIONS.items():
        process_items(name, folder)

if __name__ == '__main__':
    main()
