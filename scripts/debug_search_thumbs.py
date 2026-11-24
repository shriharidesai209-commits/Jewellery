import subprocess
import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

script = """
<script type="module">
import { defaultSearchModal } from './js/components/SearchModal.js';
defaultSearchModal.open();
const input = document.getElementById('search-query-input');
input.value = 'Choker';
input.dispatchEvent(new Event('input'));

setTimeout(() => {
  const thumbs = Array.from(document.querySelectorAll('.search-result-thumb')).map(t => ({
    src: t.src,
    currentSrc: t.currentSrc,
    naturalWidth: t.naturalWidth,
    naturalHeight: t.naturalHeight,
    rect: t.getBoundingClientRect()
  }));
  const pre = document.createElement('pre');
  pre.id = 'search-thumbs';
  pre.textContent = JSON.stringify(thumbs, null, 2);
  document.body.appendChild(pre);
}, 600);
</script>
"""

with open('temp_search_dom.html', 'w', encoding='utf-8') as f:
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
    'file:///d:/Jewellery/temp_search_dom.html'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')

if os.path.exists('temp_search_dom.html'):
    os.remove('temp_search_dom.html')

m = re.search(r'<pre id="search-thumbs">(.*?)</pre>', res.stdout, re.DOTALL)
if m:
    print(m.group(1))
else:
    print('No search-thumbs found')
