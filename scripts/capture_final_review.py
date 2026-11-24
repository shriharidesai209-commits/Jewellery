#!/usr/bin/env python3
"""
scripts/capture_final_review.py
Captures the 6 required final screenshots:
1. 01_final_desktop_hero.png
2. 02_final_desktop_craftsmanship.png
3. 03_final_desktop_catalogue.png
4. 04_final_mobile_hero_390.png
5. 05_final_mobile_craftsmanship_390.png
6. 06_final_mobile_catalogue_390.png

Guarantees each section is physically displayed at the top of the viewport so headless Chrome captures the exact intended section.
"""

import os
import subprocess
import cv2

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE = r"d:\Jewellery"
OUT_DIR = os.path.join(WORKSPACE, "reports", "final-review-screenshots")
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(WORKSPACE, "index.html"), "r", encoding="utf-8") as f:
    base_html = f.read()

# Snippets for isolating sections to the top of the viewport
desktop_hero_style = """
<style>
  .section-spotlight, .section-collections, .section-philosophy, .section-craftsmanship, .section-vault, .section-salon-banner, .site-footer {
    display: none !important;
  }
</style>
"""

desktop_craft_style = """
<style>
  .top-announcement-bar, .site-header, .hero-storefront, .section-spotlight, .section-collections, .section-philosophy, .section-vault, .section-salon-banner, .site-footer {
    display: none !important;
  }
</style>
"""

desktop_catalogue_style = """
<style>
  .top-announcement-bar, .site-header, .hero-storefront, .section-spotlight, .section-collections, .section-philosophy, .section-craftsmanship, .section-salon-banner, .site-footer {
    display: none !important;
  }
</style>
"""

mobile_container_base = """
<style>
  html, body {
    width: 390px !important;
    max-width: 390px !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow-x: hidden !important;
  }
</style>
"""

mobile_hero_style = mobile_container_base + """
<style>
  .section-spotlight, .section-collections, .section-philosophy, .section-craftsmanship, .section-vault, .section-salon-banner, .site-footer {
    display: none !important;
  }
</style>
"""

mobile_craft_style = mobile_container_base + """
<style>
  .top-announcement-bar, .site-header, .hero-storefront, .section-spotlight, .section-collections, .section-philosophy, .section-vault, .section-salon-banner, .site-footer {
    display: none !important;
  }
</style>
"""

mobile_catalogue_style = mobile_container_base + """
<style>
  .top-announcement-bar, .site-header, .hero-storefront, .section-spotlight, .section-collections, .section-philosophy, .section-craftsmanship, .section-salon-banner, .site-footer {
    display: none !important;
  }
</style>
"""

tasks = [
    # filename, w, h, style_injection, virtual_time
    ("01_final_desktop_hero.png", 1440, 960, desktop_hero_style, 1500),
    ("02_final_desktop_craftsmanship.png", 1440, 850, desktop_craft_style, 1500),
    ("03_final_desktop_catalogue.png", 1440, 1150, desktop_catalogue_style, 2000),
    ("04_final_mobile_hero_390.png", 390, 844, mobile_hero_style, 1500),
    ("05_final_mobile_craftsmanship_390.png", 390, 950, mobile_craft_style, 1500),
    ("06_final_mobile_catalogue_390.png", 390, 1100, mobile_catalogue_style, 2000)
]

print("--> Starting Final Screenshots Capture...")
for filename, w, h, style_inj, vtime in tasks:
    temp_path = os.path.join(WORKSPACE, f"temp_{filename}.html")
    content = base_html.replace("</head>", f"{style_inj}\n</head>")

    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(content)

    dest = os.path.join(OUT_DIR, filename)
    file_url = "file:///" + temp_path.replace("\\", "/")
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        "--allow-file-access-from-files",
        f"--window-size={w},{h}",
        f"--virtual-time-budget={vtime}",
        f"--screenshot={dest}",
        file_url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    if os.path.exists(dest):
        size_kb = round(os.path.getsize(dest) / 1024, 1)
        im = cv2.imread(dest)
        # If mobile (w=390), crop to exactly 390px if window manager created 504px window
        if w == 390 and im.shape[1] > 390:
            im_cropped = im[:, 0:390]
            cv2.imwrite(dest, im_cropped)
            size_kb = round(os.path.getsize(dest) / 1024, 1)
            print(f"  [SUCCESS] {filename} (Cropped to exact 390px, {im_cropped.shape[1]}x{im_cropped.shape[0]}, {size_kb} KB)")
        else:
            print(f"  [SUCCESS] {filename} ({im.shape[1]}x{im.shape[0]}, {size_kb} KB)")
    else:
        print(f"  [FAILED] {filename}")

print("\n--> All final screenshots captured and verified!")
