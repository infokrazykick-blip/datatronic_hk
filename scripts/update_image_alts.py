#!/usr/bin/env python3
"""
Update <img> alt attributes for images under images/ to SEO-friendly text.
Dry-run by default. Use --apply to write changes. Use --force to overwrite existing alt text.

Behavior:
- For each HTML file under the website root, find <img ... src="...images/..."> occurrences.
- Derive an alt text from the image filename (strip extension, replace hyphens/underscores with spaces, title-case).
- If the img has no alt or alt is empty or --force is used, set alt to the generated value.
- Report changes and optionally apply them.

Usage:
  python3 scripts/update_image_alts.py        # dry-run
  python3 scripts/update_image_alts.py --apply   # apply changes
  python3 scripts/update_image_alts.py --apply --force  # overwrite existing alts
"""

import re
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = list(ROOT.glob('**/*.html'))
IMG_SRC_RE = re.compile(r'<img\b([^>]*?)\bsrc=["\']([^"\']*images/([^"\']+))["\']([^>]*)>', re.IGNORECASE)
ALT_RE = re.compile(r'\balt=["\']([^"\']*)["\']', re.IGNORECASE)


def filename_to_alt(fname: str) -> str:
    # fname is like 'service1-img.jpg' or 'about-company-history.png'
    # strip querystrings
    base = fname.split('?')[0]
    name = base.rsplit('.', 1)[0]
    # replace separators
    name = re.sub(r'[_\-]+', ' ', name)
    # replace multiple spaces
    name = re.sub(r'\s{2,}', ' ', name).strip()
    # title case but keep common lowercase words? simple title()
    alt = name.replace('.jpg','').replace('.png','')
    alt = alt.strip()
    alt = ' '.join([w.capitalize() for w in alt.split()])
    return alt


def process_file(path: Path, apply: bool=False, force: bool=False):
    text = path.read_text(encoding='utf-8', errors='replace')
    updated = text
    changes = []

    for m in IMG_SRC_RE.finditer(text):
        full_match = m.group(0)
        before_attrs = m.group(1) or ''
        src = m.group(2)
        filename = m.group(3)
        after_attrs = m.group(4) or ''

        # check for alt in whole match
        alt_m = ALT_RE.search(full_match)
        generated = filename_to_alt(filename)
        if alt_m:
            current_alt = alt_m.group(1)
            if current_alt.strip() == '' or force:
                # replace existing alt value
                new_img = re.sub(r'\balt=["\']([^"\']*)["\']', f' alt="{generated}"', full_match, flags=re.IGNORECASE)
                updated = updated.replace(full_match, new_img)
                changes.append((path, filename, current_alt, generated))
        else:
            # insert alt before closing of attributes
            # place alt attribute after src attribute for readability
            insert_after = src
            # construct replacement: add alt="..." before after_attrs
            new_img = full_match.replace(after_attrs + '>', f' alt="{generated}"{after_attrs}>')
            # fallback: simple replace
            if new_img == full_match:
                # simpler construction
                new_img = full_match[:-1] + f' alt="{generated}">'
            updated = updated.replace(full_match, new_img)
            changes.append((path, filename, None, generated))

    if changes and apply:
        path.write_text(updated, encoding='utf-8', errors='replace')

    return changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--force', action='store_true', help='Overwrite existing alt values')
    args = parser.parse_args()

    all_changes = []
    for html in HTML_FILES:
        changes = process_file(html, apply=args.apply, force=args.force)
        for c in changes:
            all_changes.append(c)

    if not all_changes:
        print('No alt updates proposed.')
        return

    print('\nProposed alt updates:')
    for p, fname, old, new in all_changes:
        rel = p.relative_to(ROOT)
        if old is None:
            print(f'ADD: {rel} -> {fname} => "{new}"')
        else:
            print(f'REPLACE: {rel} -> {fname} : "{old}" => "{new}"')

    if args.apply:
        print('\nApplied updates to files.')
    else:
        print('\nDry-run complete. Run with --apply to write changes.')

if __name__ == "__main__":
    main()
