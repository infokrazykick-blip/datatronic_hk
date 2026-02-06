#!/usr/bin/env python3
"""Batch update HTML pages from data/products_extracted.csv

Usage:
  python3 scripts/batch_update_from_extracted.py [--dry-run]

Writes backups `<page>.html.bak` when performing real run.
"""
import csv
import os
import re
import argparse


def esc(s):
    return s.replace('\\', '\\\\').replace("'", "\\'")


def replace_productdata(content, title_en, description_en):
    title_repl = esc(title_en)
    desc_repl = esc(description_en)
    content_new = re.sub(r"en_name\s*:\s*'[^']*'", f"en_name: '{title_repl}'", content)
    content_new = re.sub(r"description_en\s*:\s*'[^']*'", f"description_en: '{desc_repl}'", content_new)
    return content_new


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    csv_path = os.path.join(os.getcwd(), 'data', 'products_extracted.csv')
    if not os.path.isfile(csv_path):
        print('CSV not found:', csv_path)
        return

    rows = []
    with open(csv_path, encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    summary = {'updated': 0, 'skipped': 0, 'missing': 0}
    for r in rows:
        page = r.get('page')
        if not page:
            summary['skipped'] += 1
            continue
        html = os.path.join(os.getcwd(), page + '.html')
        if not os.path.isfile(html):
            print('MISSING:', html)
            summary['missing'] += 1
            continue
        with open(html, 'r', encoding='utf-8') as f:
            content = f.read()
        title = r.get('title_en', '') or ''
        desc = r.get('description_en', '') or ''
        new = replace_productdata(content, title, desc)
        if new == content:
            print('NOCHANGE:', page)
            summary['skipped'] += 1
            continue
        if args.dry_run:
            print('DRY-RUN update for', page)
            summary['updated'] += 1
            continue
        bak = html + '.bak'
        with open(bak, 'w', encoding='utf-8') as bf:
            bf.write(content)
        with open(html, 'w', encoding='utf-8') as wf:
            wf.write(new)
        print('UPDATED:', page, '-> backup:', os.path.basename(bak))
        summary['updated'] += 1

    print('\nSummary:', summary)


if __name__ == '__main__':
    main()
