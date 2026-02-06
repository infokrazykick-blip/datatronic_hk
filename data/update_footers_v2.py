import os
import re

# New Footer structure with centered feel and custom spacing
new_footer = """    <footer class="site-footer">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-3 footer-logo">
                    <img src="images/logo.png" alt="Datatronic Logo">
                    <p>Award-winning manufacturer of custom magnetic components since 1971.</p>
                </div>
                <div class="col-md-2 footer-links offset-md-1">
                    <strong>Quick Links</strong>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="products.html">All Products</a></li>
                        <li><a href="applications.html">Applications</a></li>
                    </ul>
                </div>
                <div class="col-md-2 footer-links">
                    <strong>Products</strong>
                    <ul>
                        <li><a href="medical.html">Medical</a></li>
                        <li><a href="Aerospace.html">Aerospace</a></li>
                        <li><a href="Industrial.html">Industrial</a></li>
                        <li><a href="Vehicle.html">Vehicle</a></li>
                    </ul>
                </div>
                <div class="col-md-3 footer-contact">
                    <strong>Contact Us</strong>
                    <p>19/F, North Point Industrial Building,<br>499 King's Road, Hong Kong<br>
                    Email: datatron@datatronic.com.hk<br>
                    Phone: +852-2564-8477</p>
                </div>
            </div>
            <div class="row mt-4">
                <div class="col-12 text-center">
                    <hr style="border-top: 1px solid #444;">
                    <p class="mb-0" style="font-size: 0.8rem; color: #888;">&copy; 2024 Datatronic Ltd. All rights reserved.</p>
                </div>
            </div>
        </div>
    </footer>"""

footer_pattern = re.compile(r'<footer class="site-footer">.*?</footer>', re.DOTALL)

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if footer_pattern.search(content):
        new_content = footer_pattern.sub(new_footer, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

count = 0
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        if update_file(filename):
            count += 1

print(f"Updated footer in {count} files.")
