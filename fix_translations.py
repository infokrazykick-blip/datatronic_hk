#!/usr/bin/env python3
"""
Script to fix translations in product subpages:
1. Set jp_name and cn_name to same as en_name (English only for product names)
2. Set description_jp and description_cn to same as description_en (English only for descriptions)
3. Ensure i18next has Subcategories translation in all languages
"""

import os
import re
import glob

# List of all product subpages to process
product_pages = [
    'inductors_shielded_smt.html',
    'inductors_shielded_thru_hole.html',
    'inductors_unshielded_smt.html',
    'inductors_unshielded_thru_hole.html',
    'comm_telecom_smt.html',
    'comm_telecom_thru_hole.html',
    'sp_current_sense_smt.html',
    'sp_current_sense_thru_hole.html',
    'sp_gate_drive_smt.html',
    'sp_gate_drive_thru_hole.html',
    'pt_three_phase.html',
    'pt_step_control.html',
    'pt_400hz.html',
    'pt_audio.html',
    'pt_distribution.html',
    'pt_step_down.html',
    'pt_isolation.html',
    'pt_shielded.html',
    'pt_auto.html',
    'pt_ferro.html',
    'wb_hf_wirewound.html',
    'wb_air_core.html',
    'wb_rf.html',
    'maglev_coils.html',
    'solenoid_coils.html',
    'fluid.html',
    'speed_sensor.html',
    'position_sensor.html',
    'telemetry_coils.html',
    'perfect_layer_coils.html',
    'pickup_coils.html',
    'implantable_coils.html',
    'medical_application_coils.html',
    'lighting_custom.html',
    'lighting_flap.html',
    'lighting.html',
    'balancing_transformer.html',
]

def fix_product_data(content):
    """Fix productData to use English for all name and description fields"""
    
    # Pattern to match productData object
    # Find en_name value
    en_name_match = re.search(r"en_name:\s*'([^']*)'", content)
    description_en_match = re.search(r"description_en:\s*'([^']*)'", content)
    
    if en_name_match and description_en_match:
        en_name = en_name_match.group(1)
        description_en = description_en_match.group(1)
        
        # Replace jp_name with en_name value
        content = re.sub(
            r"jp_name:\s*'[^']*'",
            f"jp_name: '{en_name}'",
            content
        )
        
        # Replace cn_name with en_name value
        content = re.sub(
            r"cn_name:\s*'[^']*'",
            f"cn_name: '{en_name}'",
            content
        )
        
        # Replace description_jp with description_en value
        content = re.sub(
            r"description_jp:\s*'[^']*'",
            f"description_jp: '{description_en}'",
            content
        )
        
        # Replace description_cn with description_en value
        content = re.sub(
            r"description_cn:\s*'[^']*'",
            f"description_cn: '{description_en}'",
            content
        )
    
    return content

def fix_i18next_subcategories(content):
    """Ensure i18next has Subcategories translation"""
    
    # Check if Subcategories is missing in en translation
    if 'Subcategories: "Subcategories"' not in content and 'Subcategories: "サブカテゴリ"' not in content:
        # Add Subcategories to en translation
        content = re.sub(
            r'(download: "Download PDF")\s*}\s*}\s*,\s*ja:',
            r'\1, Subcategories: "Subcategories" } }, ja:',
            content
        )
        
        # Add Subcategories to ja translation
        content = re.sub(
            r'(download: "PDFをダウンロード")\s*}\s*}\s*,\s*cn:',
            r'\1, Subcategories: "サブカテゴリ" } }, cn:',
            content
        )
        
        # Add Subcategories to cn translation
        content = re.sub(
            r'(download: "下载PDF")\s*}\s*}\s*}\s*\)',
            r'\1, Subcategories: "子分类" } } } )',
            content
        )
    
    return content

def process_file(filepath):
    """Process a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix productData
        content = fix_product_data(content)
        
        # Fix i18next Subcategories
        content = fix_i18next_subcategories(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    modified_count = 0
    for page in product_pages:
        filepath = os.path.join(base_dir, page)
        if os.path.exists(filepath):
            if process_file(filepath):
                print(f"✅ Modified: {page}")
                modified_count += 1
            else:
                print(f"⏭️  No changes: {page}")
        else:
            print(f"❌ Not found: {page}")
    
    print(f"\n📊 Summary: {modified_count} files modified")

if __name__ == '__main__':
    main()
