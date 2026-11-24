import subprocess
import os
import cv2
import numpy as np

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE = r"d:\Jewellery"

with open(os.path.join(WORKSPACE, "index.html"), "r", encoding="utf-8") as f:
    base_html = f.read()

test_script = """
<script type="module">
import { defaultProductModal } from './js/components/ProductModal.js';
import { defaultProductService } from './js/services/productService.js';

function openWhenReady() {
  setTimeout(() => {
    const prod = defaultProductService.getProductById('PROD-001');
    console.log('Opening modal for:', prod ? prod.id : 'null');
    if (prod) {
      defaultProductModal.open(prod, 'gallery');
    }
  }, 300);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', openWhenReady);
} else {
  openWhenReady();
}
</script>
"""

temp_path = os.path.join(WORKSPACE, "temp_test_modal.html")
with open(temp_path, "w", encoding="utf-8") as f:
    f.write(base_html.replace("</body>", f"{test_script}\n</body>"))

dest = os.path.join(WORKSPACE, "reports", "final-review-screenshots", "04_final_desktop_product_modal.png")
cmd = [
    CHROME_PATH,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--hide-scrollbars",
    "--allow-file-access-from-files",
    "--window-size=1440,900",
    "--virtual-time-budget=2500",
    f"--screenshot={dest}",
    "file:///" + temp_path.replace("\\", "/")
]
subprocess.run(cmd, capture_output=True)

if os.path.exists(temp_path):
    os.remove(temp_path)

if os.path.exists(dest):
    im = cv2.imread(dest)
    uniq = len(np.unique(im.reshape(-1, 3), axis=0))
    print(f"Modal captured! Shape: {im.shape}, unique colors: {uniq}, std: {im.std():.1f}")
