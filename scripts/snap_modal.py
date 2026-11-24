import subprocess
import os
import cv2
import numpy as np

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

script = """
<script type="module">
import { defaultProductModal } from './js/components/ProductModal.js';
import { defaultProductService } from './js/services/productService.js';

const p = defaultProductService.getProductById('PROD-001');
if (p) {
  defaultProductModal.open(p, 'gallery');
}
</script>
"""

dest = os.path.join(r"d:\Jewellery\reports\final-review-screenshots", "04_final_desktop_product_modal.png")
temp_path = "temp_snap_modal.html"
with open(temp_path, 'w', encoding='utf-8') as f:
    f.write(html.replace('</body>', script + '</body>'))

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu',
    '--hide-scrollbars',
    '--allow-file-access-from-files',
    '--window-size=1440,900',
    '--virtual-time-budget=2500',
    f'--screenshot={dest}',
    'file:///d:/Jewellery/' + temp_path
]
subprocess.run(cmd, capture_output=True)

if os.path.exists(temp_path):
    os.remove(temp_path)

im = cv2.imread(dest)
print("Modal screenshot captured! Shape:", im.shape)
uniq = len(np.unique(im.reshape(-1, 3), axis=0))
print("Unique colors in modal screenshot:", uniq)
print("Std deviation:", im.std())

# Let's crop the modal image stage
# Modal dialog is centered, visual column is left side of dialog:
# roughly x: 250 to 700, y: 150 to 750
modal_img = im[150:750, 250:700]
cv2.imwrite('debug_modal_image_crop.png', modal_img)
uniq_img = len(np.unique(modal_img.reshape(-1, 3), axis=0))
print("Unique colors in modal_img stage:", uniq_img)
