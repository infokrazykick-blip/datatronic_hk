#!/usr/bin/env python3
"""Update HTML pages from UTF-8 CSV data (EN fields).

Usage:
  python3 scripts/update_from_csv.py --file path/to/page.html [--csv data/data.csv] [--dry-run]

Behavior:
  - Reads CSV (UTF-8) with a `page` column (page basename without .html) or `category`/`subcategory`.
  - Finds matching row and replaces `en_name` and `description_en` values inside the `productData` JS object.
  - Creates a `.bak` backup before writing. Supports `--dry-run` to preview changes.
"""
import argparse
import csv
import os
import re
import sys


def load_csv(csv_path):
    with open(csv_path, encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)


def find_row(rows, page_key, category=None, subcategory=None):
    # Prefer exact page match if present
    for r in rows:
        if r.get('page') and r.get('page').strip() == page_key:
            return r
    # Fallback to category/subcategory match
    if category:
        for r in rows:
            if r.get('category') and r.get('subcategory') and r['category'].strip()==category and r['subcategory'].strip()==subcategory:
                return r
    return None


def replace_productdata(content, title_en, description_en):
    # Replace en_name: '...' and description_en: '...'
    def esc(s):
        return s.replace('\\', '\\\\').replace("'", "\\'")

    title_repl = esc(title_en)
    desc_repl = esc(description_en)

    content_new = re.sub(r"en_name\s*:\s*'[^']*'", f"en_name: '{title_repl}'", content)
    content_new = re.sub(r"description_en\s*:\s*'[^']*'", f"description_en: '{desc_repl}'", content_new)
    return content_new


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--file', required=True, help='HTML file to update')
    p.add_argument('--csv', default='data/data.csv', help='CSV path (UTF-8)')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    html_path = args.file
    if not os.path.isfile(html_path):
        print('ERROR: target file not found:', html_path)
        sys.exit(1)

    if not os.path.isfile(args.csv):
        print('ERROR: CSV file not found:', args.csv)
        sys.exit(1)

    rows = load_csv(args.csv)

    basename = os.path.basename(html_path)
    page_key = os.path.splitext(basename)[0]
    # try to infer category/subcategory from page_key if formatted like 'category_subcategory'
    parts = page_key.split('_')
    category = parts[0] if len(parts) >= 1 else None
    subcategory = parts[-1] if len(parts) >= 2 else None

    row = find_row(rows, page_key, category, subcategory)
    if not row:
        print('No matching CSV row found for page:', page_key)
        sys.exit(2)

    title_en = row.get('title_en', '').strip()
    description_en = row.get('description_en', '').strip()
    if not title_en and not description_en:
        print('CSV row has no title_en or description_en to apply.')
        sys.exit(3)

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content_new = replace_productdata(content, title_en, description_en)

    if content_new == content:
        print('No changes detected (productData fields unchanged).')
        sys.exit(0)

    print('--- Preview of changes (first 400 chars) ---')
    # show a short diff-ish preview: show surrounding context for en_name
    m_before = re.search(r"en_name\s*:\s*'[^']*'", content)
    m_after = re.search(r"en_name\s*:\s*'[^']*'", content_new)
    if m_before and m_after:
        print('Before:', m_before.group(0))
        print('After :', m_after.group(0))

    if args.dry_run:
        print('\nDry-run complete. No files modified.')
        sys.exit(0)

    # backup
    bak_path = html_path + '.bak'
    with open(bak_path, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content_new)

    print('Updated', html_path, ' (backup saved to', bak_path + ')')


if __name__ == '__main__':
    main()
