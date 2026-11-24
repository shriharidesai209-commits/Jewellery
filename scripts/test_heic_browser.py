import subprocess
import os
import re

test_html = """<!DOCTYPE html>
<html>
<body>
<img src="assets/raw-jewellery/extracted/07_Fabric_Background_Reference/IMG_0037.HEIC" id="test-heic" width="300">
<script>
window.addEventListener('DOMContentLoaded', () => {
  const img = document.getElementById('test-heic');
  setTimeout(() => {
    const pre = document.createElement('pre');
    pre.id = 'res';
    pre.textContent = JSON.stringify({
      complete: img.complete,
      naturalWidth: img.naturalWidth,
      naturalHeight: img.naturalHeight
    });
    document.body.appendChild(pre);
  }, 500);
});
</script>
</body>
</html>"""

with open('temp_heic_test.html', 'w', encoding='utf-8') as f:
    f.write(test_html)

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu',
    '--allow-file-access-from-files',
    '--virtual-time-budget=1500',
    '--dump-dom',
    'file:///d:/Jewellery/temp_heic_test.html'
]
res = subprocess.run(cmd, capture_output=True, text=True)
m = re.search(r'<pre id="res">(.*?)</pre>', res.stdout, re.DOTALL)
print('HEIC browser support result:', m.group(1) if m else 'Not found')
if os.path.exists('temp_heic_test.html'):
    os.remove('temp_heic_test.html')
