import subprocess
import os
import json
import re

html_script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const images = Array.from(document.querySelectorAll('img')).map(img => ({
      src: img.getAttribute('src'),
      currentSrc: img.currentSrc,
      naturalWidth: img.naturalWidth,
      naturalHeight: img.naturalHeight,
      complete: img.complete,
      displayedWidth: img.clientWidth,
      displayedHeight: img.clientHeight,
      alt: img.alt,
      parentClass: img.parentElement ? img.parentElement.className : '',
      ancestorCard: img.closest('.product-card') ? img.closest('.product-card').getAttribute('data-product-id') : null
    }));
    
    const pre = document.createElement('pre');
    pre.id = 'img-audit';
    pre.textContent = JSON.stringify(images);
    document.body.appendChild(pre);
  }, 1000);
});
</script>
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read().replace('</body>', html_script + '</body>')

with open('temp_img_inspect.html', 'w', encoding='utf-8') as f:
    f.write(content)

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu',
    '--allow-file-access-from-files',
    '--virtual-time-budget=2000',
    '--dump-dom',
    'file:///d:/Jewellery/temp_img_inspect.html'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
if os.path.exists('temp_img_inspect.html'):
    os.remove('temp_img_inspect.html')

m = re.search(r'<pre id="img-audit">(.*?)</pre>', res.stdout, re.DOTALL)
if m:
    imgs = json.loads(m.group(1))
    print(f'Total <img> tags found: {len(imgs)}')
    for idx, img in enumerate(imgs):
        print(f'[{idx+1}] Card: {img["ancestorCard"]}, Alt: "{img["alt"]}"')
        print(f'     src: {img["src"]}')
        print(f'     currentSrc: {img["currentSrc"]}')
        print(f'     natural: {img["naturalWidth"]}x{img["naturalHeight"]}, displayed: {img["displayedWidth"]}x{img["displayedHeight"]}, complete: {img["complete"]}')
else:
    print('Failed to extract img-audit')
