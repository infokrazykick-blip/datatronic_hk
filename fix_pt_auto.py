import re

with open('pt_auto.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find product-grid section
pattern = r'(<h2[^>]*?><i class="fas fa-cube"[^>]*?></i>\s*<span[^>]*?>Product Lineup</span>\s*</h2>\s*\n\s*<div class="product-grid">.*?</div>\s*</div>)'

replacement = '''<h2 style="font-size: 1.3rem; margin-bottom: 1.5rem; color: #333130;">
                    <i class="fas fa-file-pdf" style="color: rgb(216, 26, 41); margin-right: 0.5rem;"></i>
                    <span data-i18n="available_documents">Available Documents</span>
                </h2>
                <div class="pdf-list" id="pdfList">
                </div>
            </div>'''

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('pt_auto.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
