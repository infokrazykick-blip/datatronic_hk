#!/usr/bin/env python3
import csv, re, os, sys
root = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(root, 'data', 'products.csv')
map_cat_to_file = {
    'Inductors, Shielded, SMT': 'inductors_shielded_smt.html',
    'Inductors, Shielded, Thru Hole': 'inductors_shielded_thru_hole.html',
    'Inductors, Unshielded, SMT': 'inductors_unshielded_smt.html',
    'Inductors, Unshielded, Thru Hole': 'inductors_unshielded_thru_hole.html',
    'Inductors, Unshielded, Thru-hole': 'inductors_unshielded_thru_hole.html'
}
# Read CSV as rows, keeping commas in quoted fields
with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = [r for r in reader]

# Robust parse: detect category rows containing 'Inductors' and series rows that have a non-empty second column
cats = {}
cur_cat = None
for row in rows:
    if not any(cell.strip() for cell in row):
        continue
    first = row[0].strip()
    second = row[1].strip() if len(row) > 1 else ''
    # Category detection
    if 'Inductors' in first or first.startswith('Our Products') or first.endswith(',') and 'Inductors' in first:
        # set category; prefer the exact label if present
        cur_cat = first.strip().strip(' ,"')
        cats[cur_cat] = {'description': '', 'series': []}
        continue
    # If a row has a second column, treat as series+specs
    if second:
        if cur_cat is None:
            # try to skip until a category found
            continue
        specs = second.replace('\r\n', '\n').replace('\r', '\n').strip()
        cats[cur_cat]['series'].append({'series': first.strip(), 'specs': specs})
        continue
    # If row looks like a category line without comma, handle it
    if 'Inductors' in first:
        cur_cat = first
        if cur_cat not in cats:
            cats[cur_cat] = {'description': '', 'series': []}
        continue

# Function to update an HTML file
def update_file(html_file, csv_series_list):
    path = os.path.join(root, html_file)
    if not os.path.exists(path):
        return {'error': 'missing_file'}
    s = open(path, 'r', encoding='utf-8').read()
    updated = 0
    missing = []
    # regex to find pdf object blocks
    # We'll replace specs for series that match exactly series name or startswith
    def repl(match):
        nonlocal updated
        obj = match.group(0)
        series_match = re.search(r"series:\s*['\"]([^'\"]+)['\"]", obj)
        if not series_match:
            return obj
        series_name = series_match.group(1).strip()
        # find csv entry
        csv_entry = None
        for e in csv_series_list:
            # match exact or startswith
            if e['series'] == series_name or series_name.startswith(e['series']) or e['series'].startswith(series_name):
                csv_entry = e
                break
        if csv_entry:
            # replace specs value
            new_specs = csv_entry['specs'].replace("\n", "\\n")
            # escape single quotes
            new_specs_esc = new_specs.replace("'", "\\'")
            obj2 = re.sub(r"specs:\s*(['\"]).*?\1", "specs: '"+new_specs_esc+"'", obj, flags=re.S)
            if obj2 != obj:
                updated += 1
            return obj2
        else:
            missing.append(series_name)
            return obj
    s2 = re.sub(r"\{[^{}]*?series:\s*['\"][^'\"]+['\"][^{}]*?\}", repl, s, flags=re.S)
    if updated > 0:
        open(path, 'w', encoding='utf-8').write(s2)
    return {'updated': updated, 'missing': sorted(set(missing))}

report = {}
# For each known category, update corresponding HTML
for cat, data in cats.items():
    # normalize category key
    key = cat.replace('"', '').strip()
    fname = map_cat_to_file.get(key)
    if not fname:
        if 'Thru Hole' in key or 'Thru-hole' in key:
            fname = 'inductors_shielded_thru_hole.html' if 'Shielded' in key else 'inductors_unshielded_thru_hole.html'
        elif 'Shielded, SMT' in key:
            fname = 'inductors_shielded_smt.html'
        elif 'Unshielded, SMT' in key:
            fname = 'inductors_unshielded_smt.html'
        else:
            # skip unknown categories
            continue
    res = update_file(fname, data['series'])
    report[fname] = res

# Print report
for f, r in report.items():
    print(f"File: {f}")
    if 'error' in r:
        print('  Error:', r['error'])
    else:
        print(f"  Updated entries: {r['updated']}")
        if r['missing']:
            print(f"  Series in page not found in CSV: {len(r['missing'])}")
            for m in r['missing'][:10]:
                print('   -', m)
        else:
            print('  All page series matched to CSV entries.')

print('\nDone.')
