import subprocess
import os
import cv2
import numpy as np

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE = r"d:\Jewellery"

with open(os.path.join(WORKSPACE, "index.html"), "r", encoding="utf-8") as f:
    base_html = f.read()

# Test scroll script: scrolls to #vault-section
scroll_test = """
<script>
window.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const el = document.getElementById('vault-section');
    if (el) {
      el.scrollIntoView();
    }
  }, 500);
});
</script>
"""

temp_path = os.path.join(WORKSPACE, "temp_scroll_test.html")
with open(temp_path, "w", encoding="utf-8") as f:
    f.write(base_html.replace("</head>", f"{scroll_test}\n</head>"))

dest = os.path.join(WORKSPACE, "test_scroll_snap.png")
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
    "file:///" + temp_path.replace("\\", "/")
]
subprocess.run(cmd, capture_output=True)

if os.path.exists(temp_path):
    os.remove(temp_path)

if os.path.exists(dest):
    im = cv2.imread(dest)
    print("test_scroll_snap shape:", im.shape)
    # Check unique colors and if cards are visible
    unique = len(np.unique(im.reshape(-1, 3), axis=0))
    print("Total unique colors in scroll snap:", unique)
else:
    print("test_scroll_snap failed")
