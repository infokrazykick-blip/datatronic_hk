"""
Run this script locally (on your machine) to fetch the full sitemap URL list and download linked assets (images, PDFs).

Usage:
  python3 migrate/fetch_sitemap_and_assets.py

Requirements: Python 3, requests, lxml
  pip3 install requests lxml

Outputs:
  - migrate/sitemap-urls-full.csv  (all URLs from sitemap)
  - migrate/assets.txt             (list of discovered media URLs)
  - migrate/downloaded/           (downloads of media files)

NOTE: This repository's environment couldn't run the script due to an Xcode license prompt; please run locally and share the outputs or commit them to the repo.
"""

import os
import re
import csv
import requests
from lxml import etree

os.makedirs('migrate/downloaded', exist_ok=True)

def fetch_xml(url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return etree.fromstring(r.content)

# sitemap index
index = fetch_xml('https://datatronic.com.hk/sitemap.xml')
sitemaps = [el.text for el in index.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
urls = []
for sm in sitemaps:
    try:
        tree = fetch_xml(sm)
        for loc in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            urls.append(loc.text)
    except Exception as e:
        print('Error fetching', sm, e)

# dedupe
seen=set(); uniq=[]
for u in urls:
    if u not in seen:
        seen.add(u); uniq.append(u)

with open('migrate/sitemap-urls-full.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['url'])
    for u in uniq:
        w.writerow([u])
print('Wrote', len(uniq), 'URLs to migrate/sitemap-urls-full.csv')

# find assets (images & pdfs) by scanning each URL page
assets=set()
for u in uniq:
    try:
        r = requests.get(u, timeout=10).text
        for m in re.findall(r'https?://[\w\-./]+?\.(?:pdf|jpg|jpeg|png|gif)', r, flags=re.I):
            assets.add(m)
    except Exception:
        pass

with open('migrate/assets.txt','w') as f:
    for a in sorted(assets):
        f.write(a + '\n')
print('Found', len(assets), 'assets written to migrate/assets.txt')

# Optionally download assets (uncomment to enable)
#for a in sorted(assets):
#    try:
#        r = requests.get(a, timeout=10)
#        fn = os.path.basename(a.split('?')[0])
#        with open(os.path.join('migrate/downloaded', fn), 'wb') as f:
#            f.write(r.content)
#    except Exception as e:
#        print('Failed to download', a, e)
