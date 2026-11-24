import subprocess
import os
import cv2
import numpy as np

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

script = """
<script type="module">
import { defaultSearchModal } from './js/components/SearchModal.js';

defaultSearchModal.open();
const input = document.getElementById('search-query-input');
if (input) {
  input.value = 'Choker';
  input.dispatchEvent(new Event('input'));
}
</script>
"""

dest = os.path.join(r"d:\Jewellery\reports\final-review-screenshots", "05_final_desktop_search_modal.png")
temp_path = "temp_snap_search.html"
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
    '--virtual-time-budget=3000',
    f'--screenshot={dest}',
    'file:///d:/Jewellery/' + temp_path
]
subprocess.run(cmd, capture_output=True)

if os.path.exists(temp_path):
    os.remove(temp_path)

im = cv2.imread(dest)
print("Search screenshot captured! Shape:", im.shape)
uniq = len(np.unique(im.reshape(-1, 3), axis=0))
print("Unique colors in search screenshot:", uniq)
print("Std deviation:", im.std())

dialog_area = im[200:750, 300:1140]
cv2.imwrite('debug_search_dialog_crop.png', dialog_area)
uniq_dialog = len(np.unique(dialog_area.reshape(-1, 3), axis=0))
print("Unique colors in search dialog results:", uniq_dialog)
