#!/usr/bin/env python3
"""Scan markdown files under src/ and report missing front-matter fields.
- Usage: python3 scripts/normalize_frontmatter_report.py
"""
import yaml
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'

issues = []
for md in SRC.rglob('*.md'):
    text = md.read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        issues.append((md, 'missing front-matter'))
        continue
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception as e:
        issues.append((md, f'invalid front-matter: {e}'))
        continue
    for key in ('title','date','slug','collection'):
        if key not in (fm or {}):
            issues.append((md, f'missing key: {key}'))

if issues:
    print('Found issues:')
    for p, msg in issues:
        print(p, '-', msg)
else:
    print('No front-matter issues detected.')
