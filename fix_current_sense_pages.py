#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re

workspace = "/Volumes/Extreme Pro/Datatronic/06-Website/datatronic.hk"
files = ["fluid.html","speed_sensor.html","position_sensor.html","telemetry_coils.html"]

modified = []
errors = []
for fn in files:
    path = os.path.join(workspace, fn)
    if not os.path.exists(path):
        errors.append((fn, 'not found'))
        continue
    s = open(path, 'r', encoding='utf-8').read()
    orig = s
    # remove border-top in navigation-links if present
    s = s.replace('border-top: 1px solid #e0e0e0;', '')

    # find subcategories start
    sub_pat = re.compile(r'<div[^>]*margin-bottom:\s*2rem;[^>]*>\s*<h3[^>]*>.*?Subcategories.*?</h3>', re.I|re.S)
    sub_m = sub_pat.search(s)
    # find available documents header
    avail_pat = re.compile(r'(<h[23][^>]*>\s*(?:<i[^>]*></i>\s*)?(?:<span[^>]*data-i18n="available_documents"[^>]*>.*?</span>|Available Documents).*?</h[23]>)', re.I|re.S)
    avail_m = avail_pat.search(s)
    if sub_m and avail_m:
        # ensure there's a closing </div> for the Subcategories wrapper before Available Documents
        sub_end = sub_m.end()
        avail_start = avail_m.start()
        between = s[sub_end:avail_start]
        if '</div>' not in between:
            # insert closing tags to close the grid and the wrapper
            insert_at = avail_start
            s = s[:insert_at] + '\n                </div>\n                </div>\n\n' + s[insert_at:]
            # adjust avail_m positions by re-search
            avail_m = avail_pat.search(s)
            if not avail_m:
                errors.append((fn, 'available header disappeared after insertion'))
                continue
        # ensure Available Documents block is wrapped in a container (margin-top)
        # check if there's a div with margin-top right before avail header
        prefix = s[max(0, avail_m.start()-40):avail_m.start()]
        if 'margin-top' not in prefix:
            # find pdf-list end
            pdf_list_pat = re.compile(r'<div[^>]*class="pdf-list"[^>]*>.*?</div>', re.I|re.S)
            pdf_m = pdf_list_pat.search(s, avail_m.end())
            if pdf_m:
                # wrap from avail_m.start() to pdf_m.end()
                a = avail_m.start()
                b = pdf_m.end()
                wrap = '                <div style="margin-top: 3rem;">\n'
                wrap_end = '\n                </div>\n\n'
                s = s[:a] + wrap + s[a:b] + wrap_end + s[b:]
            else:
                # no pdf-list found; still wrap the header
                a = avail_m.start()
                s = s[:a] + '                <div style="margin-top: 3rem;">\n' + s[a:]
                # try to close later by adding after first following </div></div> sequence
                close_pat = re.compile(r'</div>\s*</div>', re.I)
                cm = close_pat.search(s, a)
                if cm:
                    insert_pos = cm.end()
                    s = s[:insert_pos] + '\n                </div>\n' + s[insert_pos:]
    else:
        # If no subcategories or no available header, try to ensure product-header closed properly
        # If product-header is immediately followed by subcategories wrapper style, OK; otherwise skip
        pass

    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)
        modified.append(fn)

print('Modified:', modified)
print('Errors:', errors)
