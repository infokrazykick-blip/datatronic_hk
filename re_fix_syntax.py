import os
import re

def fix_html_syntax(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix: <h2 ... data-i18n="..." >Text</h2>  (was missing >)
    # The erroneous pattern looks like: data-i18n="text"Text
    # Or: style="..."Text
    
    # Regex to find tags that end prematurely or are followed by text without a closing bracket
    # We look for common attributes followed by a closing quote and then immediately text or another tag
    # But specifically targeting where my script failed.
    
    # Pattern: data-i18n="something"Some Text
    # Replace with: data-i18n="something">Some Text
    pattern = r'(data-i18n="[^"]*")([^>"\s][^<]*)'
    fixed_content = re.sub(pattern, r'\1>\2', content)
    
    # Pattern: style="..."Some Text
    pattern_style = r'(style="[^"]*")([^>"\s][^<]*)'
    fixed_content = re.sub(pattern_style, r'\1>\2', fixed_content)

    if fixed_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        return True
    return False

files = ["about.html", "products1.html"]
for f in files:
    if os.path.exists(f):
        if fix_html_syntax(f):
            print(f"Fixed syntax in {f}")
