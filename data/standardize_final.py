import os

files = [f for f in os.listdir('.') if f.endswith('.html')]
updated_count = 0

old_address = "499 King's Road, Hong Kong<br><br>"
new_address = "499 King's Road, North Point, Hong Kong<br><br>"

for filename in files:
    if filename.startswith('._'): continue
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    changed = False
    
    # fix 1: the address
    if old_address in content:
        content = content.replace(old_address, new_address)
        changed = True
        
    # fix 2: index.html sidebar tag and aria-hidden
    if filename == 'index.html':
        if '<div id="contactSidebar" class="collapsed">' in content:
            content = content.replace('<div id="contactSidebar" class="collapsed">', '<nav id="contactSidebar" class="collapsed" aria-hidden="false">')
            # Look for the closing div specifically after the ul
            content = content.replace('</ul>\n        </div>\n    </div>', '</ul>\n        </div>\n    </nav>')
            changed = True
            
    # fix 3: Remove reveal-hidden from any containers if they exist (based on user todo)
    if 'container reveal-hidden' in content:
        content = content.replace('container reveal-hidden', 'container')
        changed = True
    if 'container-fluid reveal-hidden' in content:
        content = content.replace('container-fluid reveal-hidden', 'container-fluid')
        changed = True
        
    if changed:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filename}")
        updated_count += 1

print(f"Total files updated: {updated_count}")
