import subprocess
import os
import re

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

const check = document.getElementById('product-detail-modal');
const pre = document.createElement('pre');
pre.id = 'modal-debug';
pre.textContent = JSON.stringify({
  found: !!check,
  className: check ? check.className : null,
  innerHTML: check ? check.innerHTML.substring(0, 300) : null
}, null, 2);
document.body.appendChild(pre);
</script>
"""

with open('temp_test_modal.html', 'w', encoding='utf-8') as f:
    f.write(html.replace('</body>', script + '</body>'))

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu',
    '--allow-file-access-from-files',
    '--window-size=1440,900',
    '--virtual-time-budget=2500',
    '--dump-dom',
    'file:///d:/Jewellery/temp_test_modal.html'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')

if os.path.exists('temp_test_modal.html'):
    os.remove('temp_test_modal.html')

m = re.search(r'<pre id="modal-debug">(.*?)</pre>', res.stdout, re.DOTALL)
if m:
    print(m.group(1))
else:
    print('No modal-debug found in DOM')
