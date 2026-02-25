#!/usr/bin/env python3
"""
Fix i18next language initialization across all HTML files
to use localStorage to persist language selection
"""

import os
import re
from pathlib import Path

def fix_i18next_init(file_path):
    """
    Modify i18next.init to use saved language from localStorage
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match various i18next.init styles
    # We need to handle both:
    # 1. i18next.init({
    #    lng: 'en',
    # 2. i18next.init({ lng: 'en',
    
    original_content = content
    
    # Pattern 1: Multi-line format with lng: 'en',
    pattern1 = r'i18next\.init\(\{\s*lng:\s*[\'"]en[\'"]\s*,'
    replacement1 = "const savedLng = window.getSavedLanguage ? window.getSavedLanguage() : (localStorage.getItem('preferredLanguage') || 'en');\n        i18next.init({\n            lng: savedLng,"
    content = re.sub(pattern1, replacement1, content)
    
    # Pattern 2: inline format
    pattern2 = r'i18next\.init\(\s*\{\s*lng:\s*[\'"]en[\'"]\s*,'
    replacement2 = "const savedLng = window.getSavedLanguage ? window.getSavedLanguage() : (localStorage.getItem('preferredLanguage') || 'en');\n            i18next.init({ lng: savedLng,"
    content = re.sub(pattern2, replacement2, content)
    
    # Only write if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_dir = Path("/Volumes/Extreme Pro/Datatronic/06-Website/website")
    
    # List of files to fix (from find command output, excluding index.html which we already fixed)
    files_to_fix = [
        "about.html", "awards.html", "products.html", "power_inductors.html",
        "applications.html", "catalogue.html", "contact.html", "fluid.html",
        "Implantable.html", "Industrial.html", "Equipment.html", "Vehicle.html",
        "Aerospace.html", "Telecommunication.html", "comm_magnetic.html",
        "inductors_unshielded_smt.html", "current_sense.html", "power_transformers.html",
        "switching_power.html", "transformers_choke.html", "wideband.html",
        "inductors_shielded_smt.html", "lighting.html", "medical.html",
        "inductors_shielded_thru_hole.html", "inductors_unshielded_thru_hole.html",
        "maglev_coils.html", "solenoid_coils.html", "speed_sensor.html",
        "position_sensor.html", "telemetry_coils.html", "perfect_layer_coils.html",
        "pickup_coils.html", "implantable_coils.html", "medical_application_coils.html",
        "lighting_custom.html", "lighting_flap.html", "comm_telecom_smt.html",
        "comm_telecom_thru_hole.html", "wb_hf_wirewound.html", "wb_air_core.html",
        "wb_rf.html", "pt_three_phase.html", "pt_step_control.html",
        "pt_400hz.html", "pt_audio.html", "pt_distribution.html",
        "pt_step_down.html", "pt_isolation.html", "pt_shielded.html",
        "pt_auto.html", "pt_ferro.html", "sp_current_sense_smt.html",
        "sp_current_sense_thru_hole.html", "sp_gate_drive_smt.html",
        "sp_gate_drive_thru_hole.html", "404.html"
    ]
    
    fixed_count = 0
    failed_count = 0
    
    for filename in files_to_fix:
        file_path = base_dir / filename
        if not file_path.exists():
            print(f"❌ Not found: {filename}")
            failed_count += 1
            continue
        
        try:
            if fix_i18next_init(file_path):
                print(f"✅ Fixed: {filename}")
                fixed_count += 1
            else:
                print(f"⚠️  No changes: {filename}")
        except Exception as e:
            print(f"❌ Error in {filename}: {e}")
            failed_count += 1
    
    print(f"\n📊 Summary: {fixed_count} fixed, {failed_count} failed")

if __name__ == "__main__":
    main()
