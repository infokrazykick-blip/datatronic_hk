import os
import re

# Pattern to find local footer styles in <style> blocks
# This matches footer { ... } inside <style> tags
style_footer_pattern = re.compile(r'footer\s*{[^}]*}', re.DOTALL)

def clean_file(filepath):
    content = None
    applied_encoding = 'utf-8'
    for enc in ['utf-8', 'latin-1', 'gb2312', 'big5']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
                applied_encoding = enc
            break
        except:
            continue
    
    if content is None:
        return False
    
    if style_footer_pattern.search(content):
        # Remove the local style
        new_content = style_footer_pattern.sub('', content)
        with open(filepath, 'w', encoding=applied_encoding) as f:
            f.write(new_content)
        return True
    return False

count = 0
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        if clean_file(filename):
            count += 1

print(f"Cleaned local footer styles in {count} files.")
