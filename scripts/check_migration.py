#!/usr/bin/env python3
"""简单的迁移检查脚本：
- 验证 migrate 目录存在
- 检查 sitemap-urls-full.csv 和 assets.txt
- 抽样检查下载文件夹与文件大小（警告 >5MB）
"""
import argparse
import csv
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATE = ROOT / 'migrate'

def check_files():
    ok = True
    if not MIGRATE.exists():
        print(f"ERROR: {MIGRATE} not found.")
        return False
    s1 = MIGRATE / 'sitemap-urls-full.csv'
    s2 = MIGRATE / 'assets.txt'

    if not s1.exists():
        print(f"ERROR: {s1} not found. Please generate with crawler.")
        ok = False
    else:
        with s1.open() as fh:
            reader = csv.reader(fh)
            headers = next(reader, None)
            if not headers or 'url' not in [h.lower() for h in headers]:
                print(f"ERROR: {s1} missing header with 'url' column.")
                ok = False
            else:
                count = sum(1 for _ in reader)
                print(f"Found {count} URLs in {s1} (excluding header).")

    if not s2.exists():
        print(f"WARN: {s2} not found. If site has media, provide assets.txt.")
    else:
        size_warn = False
        lines = s2.read_text().strip().splitlines()
        print(f"Found {len(lines)} asset lines in {s2}.")
        # naive check: find any local downloaded files and warn on size

    # check downloaded folder if present
    dl = MIGRATE / 'downloaded'
    if dl.exists() and dl.is_dir():
        print(f"Checking downloaded assets in {dl}...")
        for p in dl.rglob('*'):
            if p.is_file():
                sz = p.stat().st_size
                if sz > 5 * 1024 * 1024:
                    print(f"WARN: {p.relative_to(ROOT)} is {sz/1024/1024:.1f}MB > 5MB. Consider external storage.")
    else:
        print("No downloaded/ folder present — skipping local asset size checks.")

    # quick sample check for converted markdown presence
    found_md = False
    total_md = 0
    for d in ['src/pages', 'src/products', 'src/applications']:
        p = ROOT / d
        if p.exists():
            mds = list(p.rglob('*.md'))
            print(f"{d}: {len(mds)} markdown files found.")
            total_md += len(mds)
            if len(mds) > 0:
                found_md = True
        else:
            print(f"{d}: (not present)")

    if not found_md:
        print("WARN: No converted markdown files found under src/. Ensure conversions are included in PR.")
    else:
        print(f"Total markdown files found: {total_md}")
        # run a basic front-matter scan
        try:
            import scripts.normalize_frontmatter_report as _nfr
        except Exception:
            _nfr = None

    return ok

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check migration artifacts in repo')
    args = parser.parse_args()
    ok = check_files()
    if not ok:
        print('\nOne or more errors found. See messages above.')
        sys.exit(2)
    print('\nMigration checks completed. Address WARNs before merging where possible.')
    sys.exit(0)
