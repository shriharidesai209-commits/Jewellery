import subprocess
import os
import re

script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
  const log = [];
  document.querySelectorAll('img').forEach((img, idx) => {
    img.addEventListener('error', (e) => {
      log.push({
        idx,
        type: 'error',
        src: img.src,
        currentSrc: img.currentSrc,
        error: e.message || 'Image loading failed'
      });
    });
    img.addEventListener('load', (e) => {
      log.push({
        idx,
        type: 'load',
        src: img.src,
        currentSrc: img.currentSrc,
        naturalWidth: img.naturalWidth
      });
    });
  });

  setTimeout(() => {
    const pre = document.createElement('pre');
    pre.id = 'img-events-log';
    pre.textContent = JSON.stringify(log, null, 2);
    document.body.appendChild(pre);
  }, 1500);
});
</script>
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read().replace('</body>', script + '</body>')

with open('temp_error_test.html', 'w', encoding='utf-8') as f:
    f.write(html)

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu',
    '--allow-file-access-from-files',
    '--window-size=1440,1200',
    '--virtual-time-budget=2000',
    '--dump-dom',
    'file:///d:/Jewellery/temp_error_test.html'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')

if os.path.exists('temp_error_test.html'):
    os.remove('temp_error_test.html')

m = re.search(r'<pre id="img-events-log">(.*?)</pre>', res.stdout, re.DOTALL)
if m:
    print(m.group(1))
else:
    print('No img-events-log found')
