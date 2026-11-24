import subprocess
import json
import re
import os

script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const cards = Array.from(document.querySelectorAll('.product-card')).map(card => {
      const media = card.querySelector('.product-card-media');
      const imgContainer = card.querySelector('.product-image-container');
      const img = card.querySelector('img');
      const fallback = card.querySelector('.product-image-fallback');
      
      const mRect = media ? media.getBoundingClientRect() : null;
      const iRect = imgContainer ? imgContainer.getBoundingClientRect() : null;
      const imgRect = img ? img.getBoundingClientRect() : null;
      const fRect = fallback ? fallback.getBoundingClientRect() : null;

      return {
        id: card.getAttribute('data-product-id'),
        mediaRect: mRect,
        containerRect: iRect,
        imgRect: imgRect,
        fallbackRect: fRect,
        imgSrc: img ? img.currentSrc || img.src : null,
        imgNatural: img ? `${img.naturalWidth}x${img.naturalHeight}` : null,
        hasFallback: !!fallback
      };
    });
    const pre = document.createElement('pre');
    pre.id = 'rects-report';
    pre.textContent = JSON.stringify(cards, null, 2);
    document.body.appendChild(pre);
  }, 1500);
});
</script>
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read().replace('</body>', script + '</body>')

with open('temp_rects.html', 'w', encoding='utf-8') as f:
    f.write(html)

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu',
    '--allow-file-access-from-files',
    '--window-size=1440,4000',
    '--virtual-time-budget=2500',
    '--dump-dom',
    'file:///d:/Jewellery/temp_rects.html'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')

if os.path.exists('temp_rects.html'):
    os.remove('temp_rects.html')

m = re.search(r'<pre id="rects-report">(.*?)</pre>', res.stdout, re.DOTALL)
if m:
    print(m.group(1))
else:
    print('No report found')
