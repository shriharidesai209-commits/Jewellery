#!/usr/bin/env python3
"""
Captures high-fidelity screenshots of the live Maison Aurum Storefront.
Supports desktop, tablet, and mobile viewports.
"""

import os
import subprocess
import time

WORKSPACE = r"d:\Jewellery"
OUT_DIR = os.path.join(WORKSPACE, "reports", "screenshots")
INDEX_URL = "file:///" + os.path.join(WORKSPACE, "index.html").replace("\\", "/")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(OUT_DIR, exist_ok=True)

viewports = [
    ("storefront-desktop-hero.png", 1440, 1100),
    ("storefront-desktop-tall.png", 1440, 3200),
    ("storefront-tablet.png", 820, 1180),
    ("storefront-mobile.png", 390, 844)
]

print("--> Capturing luxury storefront screenshots...")
for filename, w, h in viewports:
    dest = os.path.join(OUT_DIR, filename)
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={w},{h}",
        f"--screenshot={dest}",
        INDEX_URL
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(dest):
        size = os.path.getsize(dest)
        print(f"  [CAPTURED] {filename} ({w}x{h}, {round(size/1024, 1)} KB)")
    else:
        print(f"  [ERROR] Failed to capture {filename}: {res.stderr}")

print("Screenshot capture complete.")
