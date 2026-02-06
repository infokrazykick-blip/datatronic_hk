import os
import re

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix duplicate class attributes: class="..." ... class="..."
    # This regex looks for tags that have two separate class attributes and merges them.
    # Note: This is a bit simplified but should work for the patterns observed.
    
    def merge_classes(match):
        tag_start = match.group(1)
        class1 = match.group(2)
        middle = match.group(3)
        class2 = match.group(4)
        tag_end = match.group(5)
        
        # Merge classes, avoiding duplicates
        all_classes = (class1 + " " + class2).split()
        unique_classes = []
        for c in all_classes:
            if c not in unique_classes:
                unique_classes.append(c)
        
        return f'<{tag_start} class="{" ".join(unique_classes)}"{middle}{tag_end}'

    # Repeat until no more matches (handles up to 2 class attributes per tag)
    # <h2 class="reveal-item" data-i18n="..." class="section-title">
    pattern = r'<([a-z0-9]+[^>]*?)\s+class="([^"]*)"([^>]*?)\s+class="([^"]*)"([^>]*?)>'
    
    new_content = content
    while re.search(pattern, new_content, re.IGNORECASE):
        new_content = re.sub(pattern, merge_classes, new_content, flags=re.IGNORECASE)

    # 2. Remove redundant animation style blocks that are now in common.css
    # Look for the .reveal-hidden / .reveal-active block in <style>
    redundant_css_pattern = r'/\* Scroll Animation Classes.*?\*/\s*\.reveal-hidden\s*\{.*?\}.*?\.reveal-active\s*\{.*?\}.*?(?=\n\s*</style>|\n\s*/\*)'
    # Use a more flexible regex for the animation blocks often found in the files
    new_content = re.sub(r'\.reveal-hidden\s*\{[^}]*\}\s*/\*.*?\*/\s*\.reveal-image\s*\{[^}]*\}\s*\.reveal-active\s*\{[^}]*\}\s*/\*.*?\*/\s*\.reveal-active\.delay-\d\s*\{[^}]*\}', '', new_content, flags=re.DOTALL)
    new_content = re.sub(r'/\* Scroll Animation Classes \*/\s*\.reveal-hidden\s*\{[^}]*\}\s*\.reveal-active\s*\{[^}]*\}\s*/\* Staggered entry.*?\*/\s*\.section-title\.reveal-active\s*\{[^}]*\}\s*\.section-desc\.reveal-active,\s*\.product-section-description\.reveal-active\s*\{[^}]*\}\s*\.is-divider\.reveal-active\s*\{[^}]*\}', '', new_content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# List of files to check (from grep output + main pages)
files_to_fix = [
    "index.html", "about.html", "products.html", "catalogue.html", "awards.html", "contact.html", "applications.html",
    "Aerospace.html", "Medical.html", "Industrial.html", "Vehicle.html", "Telecommunication.html", "Equipment.html", "Implantable.html"
]

# Add more from the grep list if they exist
grep_list = [
    "balancing_transformer.html", "comm_magnetic.html", "comm_telecom_smt.html", "comm_telecom_thru_hole.html",
    "current_sense.html", "fluid.html", "implantable_coils.html", "inductors_shielded_smt.html",
    "inductors_shielded_thru_hole.html", "inductors_unshielded_smt.html", "inductors_unshielded_thru_hole.html",
    "lighting_custom.html", "lighting_flap.html", "maglev_coils.html", "medical_application_coils.html",
    "perfect_layer_coils.html", "pickup_coils.html", "position_sensor.html", "power_inductors.html",
    "power_transformers.html", "products1.html", "pt_three_phase.html", "solenoid_coils.html",
    "sp_current_sense_smt.html", "sp_current_sense_thru_hole.html", "sp_gate_drive_smt.html",
    "sp_gate_drive_thru_hole.html", "speed_sensor.html", "switching_power.html", "telemetry_coils.html",
    "transformers_choke.html", "wb_air_core.html", "wb_hf_wirewound.html", "wb_rf.html", "wideband.html"
]
files_to_fix.extend(grep_list)

count = 0
for f in files_to_fix:
    if os.path.exists(f):
        if fix_html_file(f):
            print(f"Fixed {f}")
            count += 1

print(f"Total files fixed: {count}")
