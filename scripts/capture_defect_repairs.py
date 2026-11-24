#!/usr/bin/env python3
"""
scripts/capture_defect_repairs.py
Captures targeted verification screenshots from the running storefront.
Uses verified Chrome flags (--no-sandbox, --virtual-time-budget, --allow-file-access-from-files).
"""

import os
import subprocess
import time

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE = r"d:\Jewellery"
OUT_DIR = os.path.join(WORKSPACE, "reports", "defect-repair-screenshots")
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(WORKSPACE, "index.html"), "r", encoding="utf-8") as f:
    base_html = f.read()

# Snippet for scrolling to Craftsmanship section
craft_snippet = """
<script>
  window.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('craftsmanship-section');
    if (el) el.scrollIntoView();
  });
</script>
"""

# Snippet for scrolling to Catalogue Vault section
vault_snippet = """
<script>
  window.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('vault-section');
    if (el) el.scrollIntoView();
  });
</script>
"""

# Snippet for opening Modal on PROD-001
modal_p001_snippet = """
<script type="module">
  import { defaultProductModal } from './js/components/ProductModal.js';
  import { defaultProductService } from './js/services/productService.js';
  window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
      const p = defaultProductService.getProductById('PROD-001');
      if (p) defaultProductModal.open(p, 'listing');
    }, 400);
  });
</script>
"""

# Snippet for opening Modal on PROD-003
modal_p003_snippet = """
<script type="module">
  import { defaultProductModal } from './js/components/ProductModal.js';
  import { defaultProductService } from './js/services/productService.js';
  window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
      const p = defaultProductService.getProductById('PROD-003');
      if (p) defaultProductModal.open(p, 'detail');
    }, 400);
  });
</script>
"""

tasks = [
    # filename, width, height, snippet, virtual_time
    ("01_desktop_hero_1440.png", 1440, 900, None, 1500),
    ("02_craftsmanship_macros_1440.png", 1440, 950, craft_snippet, 2000),
    ("03_catalogue_vault_1440.png", 1440, 1200, vault_snippet, 2000),
    ("04_mobile_hero_390.png", 390, 844, None, 1500),
    ("05_mobile_craftsmanship_390.png", 390, 900, craft_snippet, 2000),
    ("06_mobile_catalogue_390.png", 390, 1100, vault_snippet, 2000),
    ("07_desktop_fullpage_1440.png", 1440, 3600, None, 2500),
    ("08_modal_prod001_1440.png", 1440, 1100, modal_p001_snippet, 2500),
    ("09_modal_prod003_macro_1440.png", 1440, 1100, modal_p003_snippet, 2500)
]

print("--> Starting Defect Repair Verification Screenshot Captures...")
for filename, w, h, snippet, vtime in tasks:
    temp_path = os.path.join(WORKSPACE, f"temp_{filename}.html")
    if snippet:
        content = base_html.replace("</body>", f"{snippet}\n</body>")
    else:
        content = base_html

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
        print(f"  [SUCCESS] {filename} ({w}x{h}, {size_kb} KB)")
    else:
        print(f"  [FAILED] Could not capture {filename}")
        if res.stderr:
            print("  Stderr:", res.stderr)

print("\n--> All verification captures completed!")
