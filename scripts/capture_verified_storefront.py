import os
import subprocess
import cv2
import numpy as np
import json

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE = r"d:\Jewellery"
OUT_DIR = os.path.join(WORKSPACE, "reports", "final-review-screenshots")
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(WORKSPACE, "index.html"), "r", encoding="utf-8") as f:
    base_html = f.read()

# Styles for clean section isolation
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

modal_product_script = """
<script type="module">
import { defaultProductModal } from './js/components/ProductModal.js';
import { defaultProductService } from './js/services/productService.js';
window.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const prod = defaultProductService.getProductById('PROD-001');
    if (prod) {
      defaultProductModal.open(prod, 'gallery');
    }
  }, 800);
});
</script>
"""

modal_search_script = """
<script type="module">
import { defaultSearchModal } from './js/components/SearchModal.js';
window.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    defaultSearchModal.open();
    const input = document.getElementById('search-query-input');
    if (input) {
      input.value = 'Choker';
      input.dispatchEvent(new Event('input'));
    }
  }, 800);
});
</script>
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
    {
        "name": "01_final_desktop_hero.png",
        "w": 1440,
        "h": 960,
        "inject": desktop_hero_style,
        "pos": "head",
        "time": 2500,
        "type": "desktop"
    },
    {
        "name": "02_final_desktop_craftsmanship.png",
        "w": 1440,
        "h": 850,
        "inject": desktop_craft_style,
        "pos": "head",
        "time": 2500,
        "type": "desktop"
    },
    {
        "name": "03_final_desktop_catalogue.png",
        "w": 1440,
        "h": 1150,
        "inject": desktop_catalogue_style,
        "pos": "head",
        "time": 3000,
        "type": "desktop"
    },
    {
        "name": "04_final_desktop_product_modal.png",
        "w": 1440,
        "h": 900,
        "inject": modal_product_script,
        "pos": "body",
        "time": 3000,
        "type": "desktop"
    },
    {
        "name": "05_final_desktop_search_modal.png",
        "w": 1440,
        "h": 900,
        "inject": modal_search_script,
        "pos": "body",
        "time": 3000,
        "type": "desktop"
    },
    {
        "name": "06_final_mobile_hero_390.png",
        "w": 390,
        "h": 844,
        "inject": mobile_hero_style,
        "pos": "head",
        "time": 2500,
        "type": "mobile"
    },
    {
        "name": "07_final_mobile_craftsmanship_390.png",
        "w": 390,
        "h": 950,
        "inject": mobile_craft_style,
        "pos": "head",
        "time": 2500,
        "type": "mobile"
    },
    {
        "name": "08_final_mobile_catalogue_390.png",
        "w": 390,
        "h": 1100,
        "inject": mobile_catalogue_style,
        "pos": "head",
        "time": 3000,
        "type": "mobile"
    }
]

print("--> Starting Capture of All 8 Storefront Deliverables...")
results = []

for t in tasks:
    filename = t["name"]
    w = t["w"]
    h = t["h"]
    inj = t["inject"]
    pos = t["pos"]
    vtime = t["time"]

    temp_path = os.path.join(WORKSPACE, f"temp_cap_{filename}.html")
    if pos == "body":
        content = base_html.replace("</body>", f"{inj}\n</body>")
    else:
        content = base_html.replace("</head>", f"{inj}\n</head>")

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
        im = cv2.imread(dest)
        if t["type"] == "mobile" and im.shape[1] > 390:
            im = im[:, 0:390]
            cv2.imwrite(dest, im)

        uniq = len(np.unique(im.reshape(-1, 3), axis=0))
        std = float(im.std())
        size_kb = round(os.path.getsize(dest) / 1024, 1)

        print(f"  [CAPTURED] {filename} -> {im.shape[1]}x{im.shape[0]} px | {size_kb} KB | Unique Colors: {uniq} | Std: {std:.1f}")
        results.append({
            "filename": filename,
            "width": im.shape[1],
            "height": im.shape[0],
            "size_kb": size_kb,
            "unique_colors": uniq,
            "std": std
        })
    else:
        print(f"  [ERROR] Failed to capture {filename}")

with open(os.path.join(WORKSPACE, "reports", "capture_summary.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\n--> All captures completed successfully!")
