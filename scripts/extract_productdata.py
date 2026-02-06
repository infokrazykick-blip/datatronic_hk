#!/usr/bin/env python3
"""Extract `productData` en fields from HTML files into CSV.

Writes `data/products_extracted.csv` with columns: page,title_en,description_en
"""
import os
import re
import csv


def extract_from_content(content):
    m = re.search(r"productData\s*=\s*\{([\s\S]*?)\};", content)
    if not m:
        return None
    body = m.group(1)
    def find_field(name):
        patt = rf"{name}\s*:\s*'((?:\\'|[^'])*)'"
        mm = re.search(patt, body)
        if not mm:
            return ''
        return mm.group(1).replace("\\'", "'").replace('\\\\', '\\')
    en_name = find_field('en_name')
    description_en = find_field('description_en')
    return en_name, description_en


def main():
    root = os.getcwd()
    out_path = os.path.join(root, 'data', 'products_extracted.csv')
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        # only scan top-level HTML files in repo root
        if dirpath != root:
            continue
        for fn in filenames:
            if not fn.lower().endswith('.html'):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
            res = extract_from_content(content)
            if res:
                en_name, description_en = res
                page = os.path.splitext(fn)[0]
                rows.append({'page': page, 'title_en': en_name, 'description_en': description_en})

    os.makedirs(os.path.join(root, 'data'), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['page', 'title_en', 'description_en'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print('Wrote', out_path, 'with', len(rows), 'rows')


if __name__ == '__main__':
    main()
