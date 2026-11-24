import subprocess
import json
import re
import os
import cv2
import numpy as np

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE = r"d:\Jewellery"

with open(os.path.join(WORKSPACE, "index.html"), "r", encoding="utf-8") as f:
    base_html = f.read()

script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const el = document.getElementById('vault-section');
    if (el) el.scrollIntoView();

    setTimeout(() => {
      const cards = Array.from(document.querySelectorAll('.product-card')).map(card => {
        const img = card.querySelector('img.product-image-element');
        const rect = img ? img.getBoundingClientRect() : null;
        return {
          id: card.getAttribute('data-product-id'),
          src: img ? img.currentSrc : null,
          rect: rect ? {
            x: Math.round(rect.x),
            y: Math.round(rect.y),
            w: Math.round(rect.width),
            h: Math.round(rect.height)
          } : null
        };
      });
      const pre = document.createElement('pre');
      pre.id = 'img-crop-rects';
      pre.textContent = JSON.stringify(cards);
      document.body.appendChild(pre);
    }, 600);
  }, 400);
});
</script>
"""

temp_path = os.path.join(WORKSPACE, "temp_img_crops.html")
with open(temp_path, "w", encoding="utf-8") as f:
    f.write(base_html.replace("</head>", f"{script}\n</head>"))

dest = os.path.join(WORKSPACE, "catalogue_live_scroll.png")
cmd = [
    CHROME_PATH,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--hide-scrollbars",
    "--allow-file-access-from-files",
    "--window-size=1440,1150",
    "--virtual-time-budget=2500",
    f"--screenshot={dest}",
    "--dump-dom",
    "file:///" + temp_path.replace("\\", "/")
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")

if os.path.exists(temp_path):
    os.remove(temp_path)

m = re.search(r'<pre id="img-crop-rects">(.*?)</pre>', res.stdout, re.DOTALL)
if m:
    cards = json.loads(m.group(1))
    im = cv2.imread(dest)
    print(f"Captured {dest}: {im.shape}")
    for idx, c in enumerate(cards):
        r = c["rect"]
        if r and r["y"] >= 0 and r["y"] + r["h"] <= im.shape[0]:
            crop = im[r["y"]:r["y"]+r["h"], r["x"]:r["x"]+r["w"]]
            crop_path = os.path.join(WORKSPACE, f"verified_card_img_{c['id']}.png")
            cv2.imwrite(crop_path, crop)
            uniq = len(np.unique(crop.reshape(-1, 3), axis=0))
            print(f"[{c['id']}] Box=({r['x']}, {r['y']}, {r['w']}x{r['h']}), Unique Colors: {uniq}, Std: {crop.std():.1f}, File: {crop_path}")
        else:
            print(f"[{c['id']}] Box is out of current 1150px viewport: {r}")
else:
    print("Failed to find rects")
