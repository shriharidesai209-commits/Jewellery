#!/usr/bin/env python3
"""
Captures screenshots of interactive storefront states:
1. Product Detail Modal with multi-angle selector and zoom
2. Private Viewing Drawer with selected pieces and salon booking form
3. Live Search Modal with real-time query results
"""

import os
import subprocess
import time

WORKSPACE = r"d:\Jewellery"
OUT_DIR = os.path.join(WORKSPACE, "reports", "screenshots")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

modal_script = """
<script type="module">
  import { defaultProductModal } from './js/components/ProductModal.js';
  import { defaultProductService } from './js/services/productService.js';
  window.addEventListener('DOMContentLoaded', () => {
    const p = defaultProductService.getProductById('PROD-003');
    if (p) {
      defaultProductModal.open(p, 'listing');
    }
  });
</script>
"""

drawer_script = """
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

search_script = """
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

with open(os.path.join(WORKSPACE, "index.html"), "r", encoding="utf-8") as f:
    base_html = f.read()

states = [
    ("storefront-product-modal.png", modal_script, 1440, 1100),
    ("storefront-viewing-drawer.png", drawer_script, 1440, 1100),
    ("storefront-search-modal.png", search_script, 1440, 1000)
]

for filename, inject_script, w, h in states:
    temp_html_path = os.path.join(WORKSPACE, f"temp_{filename}.html")
    injected_html = base_html.replace("</body>", f"{inject_script}\n</body>")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(injected_html)

    dest = os.path.join(OUT_DIR, filename)
    file_url = "file:///" + temp_html_path.replace("\\", "/")
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        "--allow-file-access-from-files",
        f"--window-size={w},{h}",
        "--virtual-time-budget=2500",
        f"--screenshot={dest}",
        file_url
    ]
    subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    if os.path.exists(dest):
        print(f"  [CAPTURED] {filename} ({w}x{h}, {round(os.path.getsize(dest)/1024, 1)} KB)")

print("Interactive state screenshot capture complete.")
