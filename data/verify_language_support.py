#!/usr/bin/env python3
"""
Language Verification Script
=============================
This script verifies that all product subpages have proper multi-language support.

Checks:
1. productData object exists with en_name, jp_name, cn_name
2. description translations exist
3. i18next initialization is present
4. All required data-i18n attributes are in place
5. Language change function works

Usage:
    python verify_language_support.py
"""

import os
import re
import json
from pathlib import Path

# Configuration
WORKSPACE_DIR = Path("/Volumes/Extreme Pro/Datatronic/06-Website/datatronic.hk")

# Product subpages to verify
PRODUCT_PAGES = [
    "inductors_shielded_smt.html",
    "inductors_shielded_thru_hole.html",
    "inductors_unshielded_smt.html",
    "inductors_unshielded_thru_hole.html",
    "comm_magnetic.html",
    "comm_telecom_smt.html",
    "comm_telecom_thru_hole.html",
    "switching_power.html",
    "sp_current_sense_smt.html",
    "sp_current_sense_thru_hole.html",
    "sp_gate_drive_smt.html",
    "sp_gate_drive_thru_hole.html",
    "transformers_choke.html",
    "balancing_transformer.html",
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
    "current_sense.html",
    "fluid.html",
    "maglev_coils.html",
    "solenoid_coils.html",
    "speed_sensor.html",
    "position_sensor.html",
    "telemetry_coils.html",
    "perfect_layer_coils.html",
    "pickup_coils.html",
    "lighting.html",
    "lighting_custom.html",
    "lighting_flap.html",
    "medical.html",
    "medical_application_coils.html",
    "implantable_coils.html",
]

# Required data-i18n attributes
REQUIRED_I18N_ATTRS = [
    "home",
    "about_us",
    "products",
    "applications",
    "contact_us",
    "back_to_products",
]

# Optional but recommended data-i18n attributes
RECOMMENDED_I18N_ATTRS = [
    "download",
    "available_documents",
    "Subcategories",
]


class LanguageVerifier:
    def __init__(self):
        self.results = []
        self.total_pages = 0
        self.pages_passed = 0
        self.pages_with_issues = 0
        
    def verify_product_data(self, content, page):
        """Verify productData object has all language variants."""
        issues = []
        
        # Find productData object
        match = re.search(r'const\s+productData\s*=\s*\{([^;]+)\};', content, re.DOTALL)
        if not match:
            issues.append("❌ Missing productData object")
            return issues
            
        data_str = match.group(1)
        
        # Check for name variants
        name_checks = [
            ("en_name", "English name"),
            ("jp_name", "Japanese name"),
            ("cn_name", "Chinese name"),
        ]
        
        for key, label in name_checks:
            if f"'{key}'" not in data_str and f'"{key}"' not in data_str and f"{key}:" not in data_str:
                # Also check for alternative keys
                if key == "jp_name" and ("ja_name" in data_str):
                    continue  # ja_name is acceptable alternative
                issues.append(f"⚠️ Missing {label} ({key}) in productData")
        
        # Check for description variants
        desc_checks = [
            ("description_en", "English description"),
            ("description_jp", "Japanese description"),
            ("description_cn", "Chinese description"),
        ]
        
        for key, label in desc_checks:
            if f"'{key}'" not in data_str and f'"{key}"' not in data_str and f"{key}:" not in data_str:
                if key == "description_jp" and ("description_ja" in data_str):
                    continue
                issues.append(f"⚠️ Missing {label} ({key}) in productData")
                
        return issues
    
    def verify_i18next_init(self, content, page):
        """Verify i18next is properly initialized."""
        issues = []
        
        if "i18next.init" not in content:
            issues.append("❌ Missing i18next initialization")
            return issues
            
        # Check for language resources
        if '"en"' not in content and "'en'" not in content:
            issues.append("⚠️ Missing English (en) language resources")
        if '"ja"' not in content and "'ja'" not in content:
            if '"jp"' not in content and "'jp'" not in content:
                issues.append("⚠️ Missing Japanese language resources")
        if '"cn"' not in content and "'cn'" not in content:
            issues.append("⚠️ Missing Chinese (cn) language resources")
            
        return issues
    
    def verify_i18n_attributes(self, content, page):
        """Verify required data-i18n attributes are present."""
        issues = []
        
        for attr in REQUIRED_I18N_ATTRS:
            if f'data-i18n="{attr}"' not in content and f"data-i18n='{attr}'" not in content:
                issues.append(f"⚠️ Missing data-i18n=\"{attr}\"")
                
        # Check recommended attributes
        missing_recommended = []
        for attr in RECOMMENDED_I18N_ATTRS:
            if f'data-i18n="{attr}"' not in content and f"data-i18n='{attr}'" not in content:
                missing_recommended.append(attr)
                
        if missing_recommended:
            issues.append(f"ℹ️ Missing recommended i18n: {', '.join(missing_recommended)}")
            
        return issues
    
    def verify_language_change(self, content, page):
        """Verify language change function exists."""
        issues = []
        
        if "function changeLanguage" not in content and "changeLanguage" not in content:
            issues.append("❌ Missing changeLanguage function")
            
        if "i18next.changeLanguage" not in content:
            issues.append("⚠️ May be missing i18next.changeLanguage call")
            
        return issues
    
    def verify_update_content(self, content, page):
        """Verify updateContent function for dynamic content."""
        issues = []
        
        # Check if page has dynamic content that needs updating
        has_product_title = 'id="productTitle"' in content
        has_product_desc = 'id="productDescription"' in content
        
        if has_product_title or has_product_desc:
            if "function updateContent" not in content and "updateContent" not in content:
                issues.append("⚠️ Has dynamic content but missing updateContent function")
            else:
                # Check if updateContent uses language
                if "i18next.language" not in content and "currentLang" not in content:
                    issues.append("⚠️ updateContent may not be using current language")
                    
        return issues
    
    def verify_language_changed_listener(self, content, page):
        """Verify languageChanged event listener."""
        issues = []
        
        if "updateContent" in content:
            if "i18next.on('languageChanged'" not in content and 'i18next.on("languageChanged"' not in content:
                issues.append("⚠️ Missing languageChanged event listener")
                
        return issues
    
    def verify_page(self, page):
        """Verify a single page for language support."""
        file_path = WORKSPACE_DIR / page
        
        if not file_path.exists():
            return {
                "page": page,
                "status": "ERROR",
                "issues": ["❌ File not found"]
            }
            
        try:
            content = file_path.read_text(encoding="utf-8")
            
            all_issues = []
            
            # Run all verification checks
            all_issues.extend(self.verify_product_data(content, page))
            all_issues.extend(self.verify_i18next_init(content, page))
            all_issues.extend(self.verify_i18n_attributes(content, page))
            all_issues.extend(self.verify_language_change(content, page))
            all_issues.extend(self.verify_update_content(content, page))
            all_issues.extend(self.verify_language_changed_listener(content, page))
            
            # Determine status
            has_errors = any(issue.startswith("❌") for issue in all_issues)
            has_warnings = any(issue.startswith("⚠️") for issue in all_issues)
            
            if has_errors:
                status = "FAIL"
            elif has_warnings:
                status = "WARN"
            else:
                status = "PASS"
                
            return {
                "page": page,
                "status": status,
                "issues": all_issues
            }
            
        except Exception as e:
            return {
                "page": page,
                "status": "ERROR",
                "issues": [f"❌ Error reading file: {str(e)}"]
            }
    
    def run(self):
        """Run verification on all pages."""
        print("\n" + "=" * 70)
        print("LANGUAGE SUPPORT VERIFICATION")
        print("=" * 70 + "\n")
        
        self.total_pages = len(PRODUCT_PAGES)
        
        for page in PRODUCT_PAGES:
            result = self.verify_page(page)
            self.results.append(result)
            
            # Print result
            status_icon = {
                "PASS": "✅",
                "WARN": "⚠️",
                "FAIL": "❌",
                "ERROR": "🔴"
            }.get(result["status"], "❓")
            
            if result["status"] == "PASS":
                self.pages_passed += 1
                print(f"{status_icon} {page}")
            else:
                self.pages_with_issues += 1
                print(f"{status_icon} {page}")
                for issue in result["issues"]:
                    print(f"   {issue}")
                    
        self.print_summary()
        
    def print_summary(self):
        """Print summary report."""
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        
        print(f"\n📊 Statistics:")
        print(f"   Total pages: {self.total_pages}")
        print(f"   Passed: {self.pages_passed} ({self.pages_passed/self.total_pages*100:.1f}%)")
        print(f"   Issues: {self.pages_with_issues} ({self.pages_with_issues/self.total_pages*100:.1f}%)")
        
        # Group by status
        status_counts = {}
        for result in self.results:
            status = result["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
            
        print(f"\n📈 By Status:")
        for status, count in sorted(status_counts.items()):
            icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌", "ERROR": "🔴"}.get(status, "❓")
            print(f"   {icon} {status}: {count}")
            
        # List pages that need attention
        needs_attention = [r for r in self.results if r["status"] in ("FAIL", "ERROR")]
        if needs_attention:
            print(f"\n🔧 Pages needing immediate attention:")
            for result in needs_attention:
                print(f"   - {result['page']}")
                
        # List pages with warnings
        with_warnings = [r for r in self.results if r["status"] == "WARN"]
        if with_warnings:
            print(f"\n⚠️ Pages with warnings ({len(with_warnings)}):")
            for result in with_warnings[:10]:  # Show first 10
                print(f"   - {result['page']}")
            if len(with_warnings) > 10:
                print(f"   ... and {len(with_warnings) - 10} more")
                
        print("\n" + "=" * 70)


def main():
    verifier = LanguageVerifier()
    verifier.run()


if __name__ == "__main__":
    main()
