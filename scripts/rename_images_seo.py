#!/usr/bin/env python3
"""
Rename images in `images/` to SEO-friendly filenames (lowercase, hyphens, remove unsafe chars).
Dry-run by default. Use --apply to perform renames and update HTML references.

Usage:
  python3 scripts/rename_images_seo.py        # dry-run, shows proposed mapping
  python3 scripts/rename_images_seo.py --apply    # apply renames and update HTML files

This script will:
- Convert filenames to lowercase
- Replace spaces, underscores, and multiple separators with single hyphens
- Remove leading dots from filenames
- Keep file extensions
- Avoid name collisions by appending numeric suffixes when necessary
- Update all .html files in the website folder to reference the new names (only if --apply)

Always review dry-run output before running with --apply.
"""

import os
import re
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # website/
IMAGES_DIR = ROOT / 'images'

def normalize(name: str) -> str:
    # name includes extension
    name = name.strip()
    # remove leading dots that can appear from mac artifact files
    name = re.sub(r'^\.+', '', name)
    name = name.replace('%20', ' ')
    lower = name.lower()
    parts = lower.rsplit('.', 1)
    if len(parts) == 2:
        base, ext = parts
        ext = ext.lower()
    else:
        base = parts[0]
        ext = ''
    # replace undesired chars with hyphens
    base = re.sub(r'[\s_]+', '-', base)
    base = re.sub(r'[^a-z0-9\-]', '-', base)
    base = re.sub(r'-{2,}', '-', base)
    base = base.strip('-')
    new = base + ('.' + ext if ext else '')
    return new


def collect_images():
    items = []
    for p in IMAGES_DIR.iterdir():
        if p.is_file():
            items.append(p.name)
    items.sort()
    return items


def build_mapping(names):
    mapping = {}
    used = set()
    for n in names:
        new = normalize(n)
        candidate = new
        i = 1
        while candidate in used or (IMAGES_DIR / candidate).exists() and candidate != n:
            # if file with candidate already exists (and isn't the same file), append suffix
            name_no_ext, *ext = candidate.rsplit('.', 1)
            ext = ('.' + ext[0]) if ext else ''
            candidate = f"{name_no_ext}-{i}{ext}"
            i += 1
        mapping[n] = candidate
        used.add(candidate)
    return mapping


def show_mapping(mapping):
    print("Proposed renames (dry-run):\n")
    for old, new in mapping.items():
        if old == new:
            print(f"SKIP: {old} -> (unchanged)")
        else:
            print(f"RENAME: {old} -> {new}")
    print('\nTips: review mapping before running with --apply')


def apply_mapping(mapping):
    # perform renames
    for old, new in mapping.items():
        if old == new:
            continue
        src = IMAGES_DIR / old
        dst = IMAGES_DIR / new
        if not src.exists():
            print(f"WARN: source missing: {src}")
            continue
        if dst.exists():
            print(f"WARN: destination exists, skipping: {dst}")
            continue
        print(f"Renaming: {old} -> {new}")
        src.rename(dst)
    # update HTML references
    print('\nUpdating HTML files...')
    for html in ROOT.glob('**/*.html'):
        if html.is_file():
            text = html.read_text(encoding='utf-8')
            updated = text
            for old, new in mapping.items():
                if old == new:
                    continue
                updated = updated.replace(old, new)
            if updated != text:
                html.write_text(updated, encoding='utf-8')
                print(f"Updated references in {html.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Perform renames and update HTML references')
    args = parser.parse_args()

    if not IMAGES_DIR.exists():
        print(f"Images directory not found: {IMAGES_DIR}")
        return

    names = collect_images()
    mapping = build_mapping(names)
    show_mapping(mapping)

    if args.apply:
        confirm = input('Type YES to apply these changes: ')
        if confirm == 'YES':
            apply_mapping(mapping)
            print('\nDone.')
        else:
            print('Aborted.')

if __name__ == '__main__':
    main()
