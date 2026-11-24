import subprocess
import os

html = """<!DOCTYPE html>
<html>
<body>
<img id="test-img" src="processed-jewellery-v2/enhanced/product-001/listing.jpg" onerror="console.log('IMG_ERR:' + this.src)" onload="console.log('IMG_OK:' + this.naturalWidth + 'x' + this.naturalHeight)">
<picture id="test-pic">
  <source srcset="processed-jewellery-v2/enhanced/product-001/listing.webp" type="image/webp">
  <img id="test-pic-img" src="processed-jewellery-v2/enhanced/product-001/listing.jpg" onerror="console.log('PIC_ERR:' + this.src)" onload="console.log('PIC_OK:' + this.naturalWidth + 'x' + this.naturalHeight)">
</picture>
</body>
</html>"""

with open('test_img_load.html', 'w', encoding='utf-8') as f:
    f.write(html)

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu',
    '--allow-file-access-from-files',
    '--virtual-time-budget=2000',
    '--enable-logging=stderr',
    '--v=1',
    'file:///d:/Jewellery/test_img_load.html'
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
for l in (res.stderr + res.stdout).splitlines():
    if 'IMG_' in l or 'PIC_' in l or 'CONSOLE' in l:
        print(l)
