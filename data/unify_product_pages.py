#!/usr/bin/env python3
"""
Product Page Unification Script
================================
This script unifies all product subpages to match the standard template (inductors_shielded_smt.html).

Features:
- Backup all HTML files before modification
- Dry-run mode to preview changes
- Extract common styles to common.css
- Unify color variables
- Fix HTML syntax errors
- Add missing ID attributes
- Generate language verification report

Usage:
    python unify_product_pages.py --dry-run    # Preview changes
    python unify_product_pages.py              # Execute changes
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path
import argparse

# Configuration
WORKSPACE_DIR = Path("/Volumes/Extreme Pro/Datatronic/06-Website/datatronic.hk")
BACKUP_DIR = WORKSPACE_DIR / "backup"
COMMON_CSS_PATH = WORKSPACE_DIR / "css" / "common.css"

# Standard template reference
STANDARD_TEMPLATE = "inductors_shielded_smt.html"

# Product subpages to process
PRODUCT_PAGES = [
    # Power Inductors
    "inductors_shielded_smt.html",
    "inductors_shielded_thru_hole.html",
    "inductors_unshielded_smt.html",
    "inductors_unshielded_thru_hole.html",
    
    # Communication
    "comm_magnetic.html",
    "comm_telecom_smt.html",
    "comm_telecom_thru_hole.html",
    
    # Switching Power
    "switching_power.html",
    "sp_current_sense_smt.html",
    "sp_current_sense_thru_hole.html",
    "sp_gate_drive_smt.html",
    "sp_gate_drive_thru_hole.html",
    
    # Transformers
    "transformers_choke.html",
    "balancing_transformer.html",
    
    # Power Transformers (PT series - keep images, unify card style)
    "power_transformers.html",
    "pt_400hz.html",
    "pt_audio.html",
    "pt_auto.html",
    "pt_distribution.html",
    "pt_ferro.html",
    "pt_isolation.html",
    "pt_shielded.html",
    "pt_step_control.html",
    "pt_step_down.html",
    "pt_three_phase.html",
    
    # Current Sense
    "current_sense.html",
    
    # Wideband
    "fluid.html",
    "maglev_coils.html",
    "solenoid_coils.html",
    "speed_sensor.html",
    "position_sensor.html",
    "telemetry_coils.html",
    "perfect_layer_coils.html",
    "pickup_coils.html",
    
    # Lighting
    "lighting.html",
    "lighting_custom.html",
    "lighting_flap.html",
    
    # Medical
    "medical.html",
    "medical_application_coils.html",
    "implantable_coils.html",
]

# CSS styles to add to common.css for product pages
PRODUCT_PAGE_STYLES = """
/* ===== Product Subpage Styles ===== */
/* These styles are shared across all product subpages */

/* Product Page Container */
.product-page-section {
    margin-bottom: 3em;
    padding: 3rem 1rem;
    background-color: white;
}

.product-page-container {
    max-width: 1200px;
    margin: 2em auto;
    padding: 0 1em;
}

/* Product Header */
.product-header {
    border-bottom: 3px solid rgb(216, 26, 41);
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
}

.product-title {
    font-size: 2rem;
    font-weight: bold;
    color: #333130;
    margin-bottom: 0.5rem;
}

.product-description {
    font-size: 1rem;
    color: #666;
    margin-bottom: 1rem;
}

/* PDF Count Badge */
.pdf-count {
    display: inline-block;
    background-color: #f0f0f0;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    color: #666;
    margin-top: 1rem;
}

/* Back to Products Button */
.back-to-products {
    display: inline-block;
    margin-bottom: 2rem;
    padding: 0.75rem 1.5rem;
    background-color: #f0f0f0;
    color: #333130;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.back-to-products:hover {
    background-color: rgb(216, 26, 41);
    color: white;
    text-decoration: none;
}

/* PDF List Grid */
.pdf-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

/* PDF Item Card */
.pdf-item {
    background-color: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.3s ease;
    border-left: 4px solid rgb(216, 26, 41);
}

.pdf-item:hover {
    box-shadow: 0 4px 12px rgba(216, 26, 41, 0.15);
    transform: translateY(-2px);
}

.pdf-series-name {
    font-size: 1rem;
    font-weight: 600;
    color: #333130;
    margin-bottom: 0.5rem;
    word-break: break-word;
}

.pdf-filename {
    font-size: 0.85rem;
    color: #999;
    margin-bottom: 1rem;
    font-family: 'Courier New', monospace;
    word-break: break-all;
}

/* PDF Download Button */
.pdf-download-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background-color: rgb(216, 26, 41);
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-size: 0.95rem;
    font-weight: 500;
    transition: background-color 0.3s ease;
}

.pdf-download-btn:hover {
    background-color: #b91f30;
    color: white;
    text-decoration: none;
}

/* Product Card (for PT series with images) */
.product-card {
    background-color: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.3s ease;
    border-left: 4px solid rgb(216, 26, 41);
    text-decoration: none;
    color: inherit;
}

.product-card:hover {
    box-shadow: 0 4px 12px rgba(216, 26, 41, 0.15);
    transform: translateY(-2px);
    text-decoration: none;
    color: inherit;
}

.product-card-image {
    width: 100%;
    height: 160px;
    object-fit: contain;
    margin-bottom: 1rem;
    background-color: white;
    border-radius: 4px;
}

.product-card-title {
    font-size: 1rem;
    font-weight: 600;
    color: #333130;
    margin-bottom: 0.5rem;
}

.product-card-description {
    font-size: 0.85rem;
    color: #666;
    line-height: 1.4;
}

/* Products Grid (for image cards) */
.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

/* Subcategories Section */
.subcategories-section {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background-color: #f9f9f9;
    border-radius: 8px;
}

.subcategories-title {
    font-size: 1.3rem;
    color: #333130;
    margin-bottom: 1.5rem;
}

.subcategories-title i {
    color: rgb(216, 26, 41);
    margin-right: 0.5rem;
}

.subcategories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
}

.subcategory-link {
    padding: 1rem;
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    text-decoration: none;
    color: #333130;
    transition: all 0.3s ease;
    display: block;
}

.subcategory-link:hover {
    border-color: rgb(216, 26, 41);
    box-shadow: 0 2px 8px rgba(216, 26, 41, 0.1);
    text-decoration: none;
    color: #333130;
}

.subcategory-link h4 {
    margin: 0 0 0.5rem;
    color: #333130;
    font-weight: 600;
}

/* Navigation Links */
.navigation-links {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 0;
    margin-top: 3rem;
}

.nav-link-prev,
.nav-link-next {
    color: #666;
    text-decoration: none;
    font-weight: 500;
    font-size: 1rem;
    transition: color 0.3s ease;
}

.nav-link-prev:hover,
.nav-link-next:hover {
    color: rgb(216, 26, 41);
    text-decoration: none;
}

/* Section Headers */
.documents-header {
    font-size: 1.3rem;
    margin-bottom: 1.5rem;
    color: #333130;
}

.documents-header i {
    color: rgb(216, 26, 41);
    margin-right: 0.5rem;
}

/* Product Page Responsive */
@media (max-width: 768px) {
    .pdf-list,
    .products-grid {
        grid-template-columns: 1fr;
    }
    
    .product-title {
        font-size: 1.5rem;
    }
    
    .navigation-links {
        flex-direction: column;
        gap: 1rem;
    }
    
    .nav-link-prev,
    .nav-link-next {
        width: 100%;
        text-align: center;
    }
    
    .subcategories-grid {
        grid-template-columns: 1fr;
    }
}
"""

# Color replacements to unify
COLOR_REPLACEMENTS = [
    ("#D81A29", "rgb(216, 26, 41)"),
    ("#d81a29", "rgb(216, 26, 41)"),
    ("rgba(216,26,41,", "rgba(216, 26, 41,"),
]

# Inline styles to remove (will use common.css instead)
INLINE_STYLES_TO_REMOVE = [
    r"\.product-header\s*\{[^}]+\}",
    r"\.product-title\s*\{[^}]+\}",
    r"\.product-description\s*\{[^}]+\}",
    r"\.pdf-list\s*\{[^}]+\}",
    r"\.pdf-item\s*\{[^}]+\}",
    r"\.pdf-item:hover\s*\{[^}]+\}",
    r"\.pdf-series-name\s*\{[^}]+\}",
    r"\.pdf-filename\s*\{[^}]+\}",
    r"\.pdf-download-btn\s*\{[^}]+\}",
    r"\.pdf-download-btn:hover\s*\{[^}]+\}",
    r"\.back-to-products\s*\{[^}]+\}",
    r"\.back-to-products:hover\s*\{[^}]+\}",
    r"\.navigation-links\s*\{[^}]+\}",
    r"\.nav-link-prev,\s*\.nav-link-next\s*\{[^}]+\}",
    r"\.nav-link-prev:hover,\s*\.nav-link-next:hover\s*\{[^}]+\}",
    r"\.pdf-count\s*\{[^}]+\}",
]


class ProductPageUnifier:
    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.changes_log = []
        self.errors = []
        self.language_issues = []
        
    def log_change(self, page, change_type, description):
        """Log a change for reporting."""
        self.changes_log.append({
            "page": page,
            "type": change_type,
            "description": description
        })
        
    def log_error(self, page, error):
        """Log an error."""
        self.errors.append({
            "page": page,
            "error": str(error)
        })

    def backup_files(self):
        """Backup all HTML files to backup directory."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / timestamp
        
        if self.dry_run:
            print(f"[DRY-RUN] Would create backup at: {backup_path}")
            return backup_path
            
        backup_path.mkdir(parents=True, exist_ok=True)
        
        for page in PRODUCT_PAGES:
            src = WORKSPACE_DIR / page
            if src.exists():
                dst = backup_path / page
                shutil.copy2(src, dst)
                print(f"  Backed up: {page}")
        
        # Also backup common.css
        if COMMON_CSS_PATH.exists():
            shutil.copy2(COMMON_CSS_PATH, backup_path / "common.css")
            print(f"  Backed up: css/common.css")
            
        print(f"\n✅ Backup completed: {backup_path}\n")
        return backup_path

    def update_common_css(self):
        """Add product page styles to common.css."""
        if not COMMON_CSS_PATH.exists():
            self.log_error("common.css", "File not found")
            return False
            
        content = COMMON_CSS_PATH.read_text(encoding="utf-8")
        
        # Check if product styles already exist
        if "Product Subpage Styles" in content:
            print("  Product styles already in common.css, skipping...")
            return True
            
        if self.dry_run:
            print(f"[DRY-RUN] Would add {len(PRODUCT_PAGE_STYLES)} characters to common.css")
            self.log_change("common.css", "ADD_STYLES", "Add product page styles")
            return True
            
        # Append product page styles
        new_content = content + "\n" + PRODUCT_PAGE_STYLES
        COMMON_CSS_PATH.write_text(new_content, encoding="utf-8")
        self.log_change("common.css", "ADD_STYLES", "Added product page styles")
        print("  ✅ Added product page styles to common.css")
        return True

    def fix_color_variables(self, content, page):
        """Unify color variables to standard format."""
        original = content
        for old_color, new_color in COLOR_REPLACEMENTS:
            if old_color in content:
                content = content.replace(old_color, new_color)
                self.log_change(page, "COLOR_FIX", f"Replaced {old_color} with {new_color}")
        return content

    def fix_accent_color(self, content, page):
        """Ensure --accent-color is #4A4A4A."""
        pattern = r"--accent-color:\s*#[A-Fa-f0-9]{6}"
        if re.search(pattern, content):
            new_content = re.sub(pattern, "--accent-color: #4A4A4A", content)
            if new_content != content:
                self.log_change(page, "ACCENT_COLOR", "Unified --accent-color to #4A4A4A")
                return new_content
        return content

    def fix_syntax_errors(self, content, page):
        """Fix known HTML syntax errors."""
        # Fix pickup_coils.html style tag error: < style=...
        if "< style=" in content:
            content = re.sub(r'<\s+style=', '<div style=', content)
            self.log_change(page, "SYNTAX_FIX", "Fixed malformed < style= tag")
        
        # Fix other common issues
        # Remove duplicate closing tags
        content = re.sub(r'</div>\s*</div>\s*</div>\s*</div>\s*</div>', '</div></div></div>', content)
        
        return content

    def add_missing_ids(self, content, page):
        """Add missing ID attributes to product elements."""
        changes_made = False
        
        # Check for productTitle ID
        if 'class="product-title"' in content and 'id="productTitle"' not in content:
            content = content.replace('class="product-title"', 'class="product-title" id="productTitle"')
            self.log_change(page, "ADD_ID", "Added id='productTitle'")
            changes_made = True
            
        # Check for productDescription ID
        if 'class="product-description"' in content and 'id="productDescription"' not in content:
            content = content.replace('class="product-description"', 'class="product-description" id="productDescription"')
            self.log_change(page, "ADD_ID", "Added id='productDescription'")
            changes_made = True
            
        # Check for pdfCount ID
        if 'class="pdf-count"' in content and 'id="pdfCount"' not in content:
            content = content.replace('class="pdf-count"', 'class="pdf-count" id="pdfCount"')
            self.log_change(page, "ADD_ID", "Added id='pdfCount'")
            changes_made = True
            
        # Check for pdfList ID
        if 'class="pdf-list"' in content and 'id="pdfList"' not in content:
            content = content.replace('class="pdf-list"', 'class="pdf-list" id="pdfList"')
            self.log_change(page, "ADD_ID", "Added id='pdfList'")
            changes_made = True
            
        return content

    def remove_navigation_border(self, content, page):
        """Remove border-top from navigation-links."""
        if "navigation-links" in content and "border-top" in content:
            # Remove border-top from inline styles
            pattern = r'(\.navigation-links\s*\{[^}]*?)border-top:\s*[^;]+;'
            if re.search(pattern, content):
                content = re.sub(pattern, r'\1', content)
                self.log_change(page, "STYLE_FIX", "Removed border-top from navigation-links")
        return content

    def remove_duplicate_inline_styles(self, content, page):
        """Remove inline styles that are now in common.css."""
        original = content
        
        for pattern in INLINE_STYLES_TO_REMOVE:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, "", content)
                
        # Clean up empty lines in style block
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original:
            self.log_change(page, "REMOVE_STYLES", "Removed duplicate inline styles (now in common.css)")
            
        return content

    def check_language_support(self, content, page):
        """Check if page has proper i18n support."""
        issues = []
        
        # Check for productData object
        if "const productData" not in content:
            issues.append("Missing productData object")
        else:
            # Check for language variants
            if "en_name" not in content:
                issues.append("Missing en_name in productData")
            if "jp_name" not in content and "ja_name" not in content:
                issues.append("Missing jp_name in productData")
            if "cn_name" not in content:
                issues.append("Missing cn_name in productData")
                
        # Check for i18next initialization
        if "i18next.init" not in content:
            issues.append("Missing i18next initialization")
            
        # Check for data-i18n attributes
        if 'data-i18n="back_to_products"' not in content:
            issues.append("Missing data-i18n on back button")
        if 'data-i18n="download"' not in content and '.pdf-download-btn' in content:
            issues.append("Missing data-i18n on download button")
            
        if issues:
            self.language_issues.append({
                "page": page,
                "issues": issues
            })
            
        return len(issues) == 0

    def unify_product_card_class(self, content, page):
        """Ensure PT series pages use unified product-card class."""
        if page.startswith("pt_"):
            # Check if using old class names
            if ".products-grid" in content and "grid-template-columns: 1fr 1fr" in content:
                # Update to use standard grid
                content = re.sub(
                    r'\.products-grid\s*\{\s*[^}]*grid-template-columns:\s*1fr\s+1fr[^}]*\}',
                    '',
                    content
                )
                self.log_change(page, "STYLE_FIX", "Unified products-grid to standard layout")
        return content

    def process_page(self, page):
        """Process a single product page."""
        file_path = WORKSPACE_DIR / page
        
        if not file_path.exists():
            self.log_error(page, "File not found")
            return False
            
        try:
            content = file_path.read_text(encoding="utf-8")
            original_content = content
            
            # Apply all fixes
            content = self.fix_syntax_errors(content, page)
            content = self.fix_color_variables(content, page)
            content = self.fix_accent_color(content, page)
            content = self.add_missing_ids(content, page)
            content = self.remove_navigation_border(content, page)
            content = self.remove_duplicate_inline_styles(content, page)
            content = self.unify_product_card_class(content, page)
            
            # Check language support
            self.check_language_support(content, page)
            
            # Write changes if not dry-run
            if content != original_content:
                if self.dry_run:
                    print(f"  [DRY-RUN] Would modify: {page}")
                else:
                    file_path.write_text(content, encoding="utf-8")
                    print(f"  ✅ Modified: {page}")
                return True
            else:
                print(f"  ⏭️  No changes needed: {page}")
                return True
                
        except Exception as e:
            self.log_error(page, str(e))
            return False

    def generate_report(self):
        """Generate a summary report."""
        print("\n" + "=" * 60)
        print("UNIFICATION REPORT")
        print("=" * 60)
        
        print(f"\n📊 Summary:")
        print(f"   - Total pages processed: {len(PRODUCT_PAGES)}")
        print(f"   - Changes logged: {len(self.changes_log)}")
        print(f"   - Errors: {len(self.errors)}")
        print(f"   - Language issues: {len(self.language_issues)}")
        
        if self.changes_log:
            print(f"\n📝 Changes by type:")
            change_types = {}
            for change in self.changes_log:
                t = change["type"]
                change_types[t] = change_types.get(t, 0) + 1
            for t, count in sorted(change_types.items()):
                print(f"   - {t}: {count}")
                
        if self.errors:
            print(f"\n❌ Errors:")
            for error in self.errors:
                print(f"   - {error['page']}: {error['error']}")
                
        if self.language_issues:
            print(f"\n🌐 Language support issues:")
            for item in self.language_issues:
                print(f"   - {item['page']}:")
                for issue in item['issues']:
                    print(f"     • {issue}")
                    
        print("\n" + "=" * 60)

    def run(self):
        """Main execution method."""
        mode = "DRY-RUN" if self.dry_run else "EXECUTE"
        print(f"\n{'=' * 60}")
        print(f"Product Page Unification Script - {mode} MODE")
        print(f"{'=' * 60}\n")
        
        # Step 1: Backup files
        print("📦 Step 1: Backing up files...")
        self.backup_files()
        
        # Step 2: Update common.css
        print("🎨 Step 2: Updating common.css...")
        self.update_common_css()
        
        # Step 3: Process each product page
        print(f"\n📄 Step 3: Processing {len(PRODUCT_PAGES)} product pages...")
        for page in PRODUCT_PAGES:
            self.process_page(page)
            
        # Step 4: Generate report
        self.generate_report()
        
        if self.dry_run:
            print("\n💡 This was a DRY-RUN. No files were modified.")
            print("   Run without --dry-run to apply changes.")


def main():
    parser = argparse.ArgumentParser(
        description="Unify product subpages to match standard template"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    args = parser.parse_args()
    
    unifier = ProductPageUnifier(dry_run=args.dry_run)
    unifier.run()


if __name__ == "__main__":
    main()
