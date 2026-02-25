#!/usr/bin/env python3
import re
from pathlib import Path
p = Path('inductors_unshielded_thru_hole.html')
s = p.read_text(encoding='utf-8')
# canonical DR362 specs
new_specs = "Low EMI Toroid\nHigh Current Capacity\nOperating Temp. -55°C to +200°C\nHorizontal or Vertical Mount\nSize: 21.8mm x 11.4mm"
# replace DR362-1 specs
s_new = re.sub(r"(series:\s*'DR362-1 Series',\s*filename:\s*'[^']+',\s*specs:\s*)'[^']*'",
               r"\1'" + new_specs.replace("'","\\'") + r"'",
               s, count=1)
# replace DR362-2 specs
s_new = re.sub(r"(series:\s*'DR362-2 Series',\s*filename:\s*'[^']+',\s*specs:\s*)'[^']*'",
               r"\1'" + new_specs.replace("'","\\'") + r"'",
               s_new, count=1)
if s_new == s:
    print('No replacements made.')
else:
    p.write_text(s_new, encoding='utf-8')
    print('Updated file:', p)
