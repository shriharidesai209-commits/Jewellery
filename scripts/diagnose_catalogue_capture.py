import subprocess
import os
import re
import json

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE = r"d:\Jewellery"

with open(os.path.join(WORKSPACE, "index.html"), "r", encoding="utf-8") as f:
    base_html = f.read()

desktop_catalogue_style = """
<style>
  .top-announcement-bar, .site-header, .hero-storefront, .section-spotlight, .section-collections, .section-philosophy, .section-craftsmanship, .section-salon-banner, .site-footer {
    display: none !important;
  }
</style>
<script>
window.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const cards = Array.from(document.querySelectorAll('.product-card')).map(card => {
      const img = card.querySelector('img');
      const pic = card.querySelector('picture');
      const fallback = card.querySelector('.product-image-fallback');
      return {
        id: card.getAttribute('data-product-id'),
        hasImg: !!img,
        imgSrc: img ? img.src : null,
        imgNaturalWidth: img ? img.naturalWidth : null,
        imgComplete: img ? img.complete : null,
        imgDisplayed: img ? `${img.clientWidth}x${img.clientHeight}` : null,
        hasFallback: !!fallback,
        innerHTML: card.querySelector('.product-card-media').innerHTML.substring(0, 300)
      };
    });
    const pre = document.createElement('pre');
    pre.id = 'debug-cards';
    pre.textContent = JSON.stringify(cards, null, 2);
    document.body.appendChild(pre);
  }, 1200);
});
</script>
"""

temp_path = os.path.join(WORKSPACE, "temp_debug_cat.html")
content = base_html.replace("</head>", f"{desktop_catalogue_style}\n</head>")

with open(temp_path, "w", encoding="utf-8") as f:
    f.write(content)

file_url = "file:///" + temp_path.replace("\\", "/")
dest = os.path.join(WORKSPACE, "debug_cat_snap.png")

cmd = [
    CHROME_PATH,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--hide-scrollbars",
    "--allow-file-access-from-files",
    "--window-size=1440,1150",
    "--virtual-time-budget=2000",
    f"--screenshot={dest}",
    "--dump-dom",
    file_url
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")

if os.path.exists(temp_path):
    os.remove(temp_path)

m = re.search(r'<pre id="debug-cards">(.*?)</pre>', res.stdout, re.DOTALL)
if m:
    print("Debug Cards Report:")
    print(m.group(1))
else:
    print("Could not find debug-cards in dump-dom")
