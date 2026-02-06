#!/usr/bin/env python3
"""
Download awards images from datatronic.com.hk and save to local images/awards/ directory
"""

import os
import urllib.request
import urllib.error
import time
from pathlib import Path

# Base URL for awards images
BASE_URL = "https://datatronic.com.hk/wp-content/uploads/2021/11/"
BASE_URL_2021020 = "https://datatronic.com.hk/wp-content/uploads/2021/11/"

# Image IDs to download (from HTML)
IMAGES = [
    # Industrial Application
    ("2021022561215-1.jpg", "Industrial"),
    ("2021022552247-1.jpg", "Industrial"),
    ("2021022580144-1.jpg", "Industrial"),
    ("2021022546848-1.jpg", "Industrial"),
    
    # Aerospace
    ("2021022517234-1.jpg", "Aerospace"),
    ("2021022572874-1.jpg", "Aerospace"),
    ("2021022531393-1.jpg", "Aerospace"),
    ("2021022531758-1.jpg", "Aerospace"),
    
    # Telecommunication
    ("2021022527542-2.jpg", "Telecom"),
    ("2021022547037-2.jpg", "Telecom"),
    ("2021020160075-2.jpg", "Telecom"),
    ("2021020118725-2.jpg", "Telecom"),
]

# Output directory
OUTPUT_DIR = "images/awards"

def ensure_dir():
    """Create output directory if it doesn't exist"""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    print(f"✓ Directory ready: {OUTPUT_DIR}")

def download_image(filename, category):
    """Download single image from remote server"""
    url = BASE_URL + filename
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Skip if already exists
    if os.path.exists(filepath):
        print(f"✓ Already exists: {filename}")
        return True
    
    try:
        print(f"⏳ Downloading {category:15} {filename}...", end=" ")
        urllib.request.urlretrieve(url, filepath)
        size_kb = os.path.getsize(filepath) / 1024
        print(f"✓ {size_kb:.1f}KB")
        time.sleep(0.5)  # Be nice to the server
        return True
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP {e.code}")
        # Try to remove partial file
        if os.path.exists(filepath):
            os.remove(filepath)
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False

def main():
    print("=" * 60)
    print("DATATRONIC AWARDS IMAGE DOWNLOADER")
    print("=" * 60)
    
    ensure_dir()
    print()
    
    success = 0
    failed = 0
    
    for filename, category in IMAGES:
        if download_image(filename, category):
            success += 1
        else:
            failed += 1
    
    print()
    print("=" * 60)
    print(f"RESULT: {success} downloaded, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        print("\n⚠️  Some images failed to download. This may be due to:")
        print("   - Network issues")
        print("   - File not available on remote server")
        print("   - Server blocking automated requests")

if __name__ == "__main__":
    main()
