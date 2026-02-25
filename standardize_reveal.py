import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('._')]
updated_count = 0

for filename in files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    changed = False
    
    # 1. Update existing headers to use standardized classes for dynamic reveal
    # Case: h1 followed by p
    # We want to add class="section-title" to h1 and class="section-desc" to p/span if they are child of a text-center div
    
    # Simple regex to find h1 or h2 or h3 with data-i18n and add section-title if not present
    content = re.sub(r'<(h1|h2|h3)([^>]*data-i18n="[^"]+"[^>]*)>', 
                     lambda m: f'<{m.group(1)} class="section-title" {m.group(2)}>' if 'class=' not in m.group(2) else m.group(0).replace('class="', 'class="section-title '), 
                     content)
    
    # Simple regex to find p with data-i18n and section-desc if it matches lead or product-section-description
    content = re.sub(r'<(p|span)([^>]*data-i18n="[^"]+"[^>]*)>',
                     lambda m: f'<{m.group(1)} class="section-desc" {m.group(2)}>' if ('lead' in m.group(2) or 'product-section-description' in m.group(2) or 'section-desc' in m.group(2)) and 'section-desc' not in m.group(2) else m.group(0),
                     content)

    # 2. Specifically handle about.html reveal targets by adding reveal-item class
    if filename == 'about.html':
        # Targets: header.hero .container, .about-text h2, etc.
        targets = [
            '<div class="container">',
            '<h2 data-i18n="about_datatronic"',
            '<p data-i18n="about_desc1"',
            '<h4 data-i18n="locations_title"',
            '<li data-i18n="sales_office"',
            '<li data-i18n="research_centers"',
            '<li data-i18n="manufacturing_sites"',
            '<h1 data-i18n="brand_strength"',
            '<p data-i18n="brand_desc"',
            '<h1 data-i18n="on_time_delivery"',
            '<p data-i18n="on_time_desc"',
            '<h1 data-i18n="comprehensive_testing"',
            '<p data-i18n="comprehensive_desc"'
        ]
        for t in targets:
            if t in content and 'reveal-item' not in content[content.find(t):content.find(t)+100]:
                if 'class="' in t:
                    content = content.replace(t, t.replace('class="', 'class="reveal-item '))
                else:
                    tag = t.split(' ')[0][1:]
                    content = content.replace(t, f'<{tag} class="reveal-item" {t[len(tag)+2:]}')
        changed = True

    # 3. Clean up index.html local CSS/JS
    if filename == 'index.html':
        # Remove local reveal CSS
        css_pattern = r'/\* Scroll Animation Classes \*/.*?.is-divider.reveal-active \{.*?\}'
        content = re.sub(css_pattern, '', content, flags=re.DOTALL)
        
        # Remove local reveal JS
        js_pattern = r'// Scroll Reveal Animations for "About" and other sections.*?observer.observe\(el\);\s+\}\);'
        content = re.sub(js_pattern, '', content, flags=re.DOTALL)
        changed = True

    # 4. Remove local reveal JS from about.html
    if filename == 'about.html':
        js_pattern = r'// Scroll Reveal Animations.*?observer.observe\(el\);\s+\}\);'
        content = re.sub(js_pattern, '', content, flags=re.DOTALL)
        changed = True

    # Check if anything changed via regex
    with open(filename, 'r', encoding='utf-8') as f:
        orig = f.read()
    
    if content != orig:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Standardized: {filename}")
        updated_count += 1

print(f"Total files standardized: {updated_count}")
