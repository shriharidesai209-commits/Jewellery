#!/usr/bin/env python3
"""
Comprehensive Live Visual Review & Capture Script.
Generates all screenshots requested by the user:
1. Actual Desktop Homepage (1440x900)
2. Actual Complete Full-Page Desktop (1440x3300)
3. Actual Mobile Version (390x844)
4. Actual Product Inspection Modal (1440x1100)
5. Actual Private Viewing Drawer (1440x1100)
6. Actual Live Search Modal (1440x1000)
7. Category Filtering: Earrings (1440x1100)
8. Category Filtering: Necklaces & Chokers (1440x1100)
9. Verification of all 5 approved jewellery products & their V2 assets
"""

import os
import subprocess
import time
import json

WORKSPACE = r"d:\Jewellery"
OUT_DIR = os.path.join(WORKSPACE, "reports", "screenshots")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(WORKSPACE, "index.html"), "r", encoding="utf-8") as f:
    base_html = f.read()

# Interactive test snippets
modal_snippet = """
<script type="module">
  import { defaultProductModal } from './js/components/ProductModal.js';
  import { defaultProductService } from './js/services/productService.js';
  window.addEventListener('DOMContentLoaded', () => {
    const p = defaultProductService.getProductById('PROD-003');
    if (p) defaultProductModal.open(p, 'listing');
  });
</script>
"""

drawer_snippet = """
<script type="module">
  import { defaultViewingDrawer } from './js/components/ViewingDrawer.js';
  import { defaultProductService } from './js/services/productService.js';
  window.addEventListener('DOMContentLoaded', () => {
    const p1 = defaultProductService.getProductById('PROD-001');
    const p3 = defaultProductService.getProductById('PROD-003');
    if (p1) defaultViewingDrawer.addItem(p1);
    if (p3) defaultViewingDrawer.addItem(p3);
    defaultViewingDrawer.open();
  });
</script>
"""

search_snippet = """
<script type="module">
  import { defaultSearchModal } from './js/components/SearchModal.js';
  window.addEventListener('DOMContentLoaded', () => {
    defaultSearchModal.open();
    const input = document.querySelector('#search-query-input');
    if (input) {
      input.value = 'Choker';
      input.dispatchEvent(new Event('input', { bubbles: true }));
    }
  });
</script>
"""

filter_earrings_snippet = """
<style>
  header, .announcement-bar, .hero-storefront, .section-spotlight, .section-collections, .section-philosophy, .section-craftsmanship {
    display: none !important;
  }
</style>
<script type="module">
  window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
      const btn = document.querySelector('[data-category="Earrings"]');
      if (btn) btn.click();
    }, 400);
  });
</script>
"""

filter_necklaces_snippet = """
<style>
  header, .announcement-bar, .hero-storefront, .section-spotlight, .section-collections, .section-philosophy, .section-craftsmanship {
    display: none !important;
  }
</style>
<script type="module">
  window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
      const btn = document.querySelector('[data-category="Necklaces & Chokers"]');
      if (btn) btn.click();
    }, 400);
  });
</script>
"""

tasks = [
    # filename, width, height, snippet, virtual_time
    ("actual-desktop-homepage.png", 1440, 900, None, 1000),
    ("actual-desktop-fullpage.png", 1440, 3300, None, 1500),
    ("actual-mobile-390px.png", 390, 844, None, 1000),
    ("actual-product-modal.png", 1440, 1100, modal_snippet, 2000),
    ("actual-viewing-drawer.png", 1440, 1100, drawer_snippet, 2000),
    ("actual-live-search.png", 1440, 1000, search_snippet, 2000),
    ("actual-filter-earrings.png", 1440, 1100, filter_earrings_snippet, 2000),
    ("actual-filter-necklaces.png", 1440, 1100, filter_necklaces_snippet, 2000)
]

print("--> Starting Live Visual Review Captures...")
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
    subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    if os.path.exists(dest):
        size_kb = round(os.path.getsize(dest) / 1024, 1)
        print(f"  [SUCCESS] {filename} ({w}x{h}, {size_kb} KB)")
    else:
        print(f"  [FAILED] Could not capture {filename}")

# Asset verification audit
print("\n--> Verifying 5 Approved Jewellery Products & V2 Assets...")
with open(os.path.join(WORKSPACE, "data", "products.json"), "r", encoding="utf-8") as f:
    catalog = json.load(f)

products = catalog.get("products", [])
print(f"  Total catalogue products: {len(products)}")
for p in products:
    pid = p.get("id")
    pname = p.get("name")
    cat = p.get("category")
    images = p.get("images", {})
    audit = p.get("auditStatus")
    print(f"\n  Product: [{pid}] {pname}")
    print(f"    Category: {cat} | Audit Status: {audit}")
    for role, paths in images.items():
        if not isinstance(paths, dict):
            continue
        for fmt, rel_path in paths.items():
            if not isinstance(rel_path, str):
                continue
            full_path = os.path.join(WORKSPACE, rel_path.replace("/", "\\"))
            exists = os.path.exists(full_path)
            fsize = os.path.getsize(full_path) if exists else 0
            is_v2 = "processed-jewellery-v2" in rel_path
            is_v1 = "processed-jewellery/" in rel_path
            status = "OK" if (exists and is_v2 and not is_v1) else "FAIL"
            print(f"    - {role}.{fmt}: {rel_path} [{status}, {fsize} bytes]")

print("\nVisual review capture and asset verification complete.")
