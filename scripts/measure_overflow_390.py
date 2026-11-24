#!/usr/bin/env python3
"""
scripts/measure_overflow_390.py
Measures exact horizontal overflow at 390px viewport width.
Dumps all offending elements to a JSON file.
"""

import os
import subprocess
import json

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE = r"d:\Jewellery"
HTML_PATH = os.path.join(WORKSPACE, "index.html")

audit_js = """
<script>
window.addEventListener('DOMContentLoaded', () => {
  // Force 390px viewport styling for exact measurement
  setTimeout(() => {
    const vw = 390;
    const results = {
      windowInnerWidth: window.innerWidth,
      docScrollWidth: document.documentElement.scrollWidth,
      bodyScrollWidth: document.body.scrollWidth,
      overflowingElements: []
    };
    
    // Check all visible elements
    document.querySelectorAll('*').forEach(el => {
      // Ignore mobile nav drawer which is off-screen by design
      if (el.closest('#mobile-nav-drawer') || el.id === 'mobile-nav-drawer') return;
      if (el.closest('#viewing-drawer') || el.id === 'viewing-drawer') return;
      if (el.closest('#search-modal') || el.id === 'search-modal') return;
      if (el.closest('#product-modal') || el.id === 'product-modal') return;
      
      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden') return;
      
      if (rect.right > 390.5 || el.scrollWidth > 390.5) {
        results.overflowingElements.push({
          tag: el.tagName,
          id: el.id || '',
          className: (typeof el.className === 'string' ? el.className : ''),
          right: Math.round(rect.right),
          width: Math.round(rect.width),
          scrollWidth: el.scrollWidth,
          styleWidth: style.width,
          styleMinWidth: style.minWidth,
          stylePadding: style.padding,
          styleMargin: style.margin,
          parent: el.parentElement ? `${el.parentElement.tagName}.${el.parentElement.className}` : ''
        });
      }
    });
    
    const pre = document.createElement('pre');
    pre.id = 'audit-dump';
    pre.textContent = JSON.stringify(results);
    document.body.appendChild(pre);
  }, 800);
});
</script>
"""

with open(HTML_PATH, "r", encoding="utf-8") as f:
    base_html = f.read()

# Add a style constraint for test to simulate exact 390px layout container
test_html_content = base_html.replace("</head>", """
<style id="sim-390">
  html, body {
    width: 390px !important;
    max-width: 390px !important;
    margin: 0 !important;
  }
</style>
</head>
""").replace("</body>", f"{audit_js}\n</body>")

temp_html = os.path.join(WORKSPACE, "temp_audit_390.html")
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(test_html_content)

out_dump = os.path.join(WORKSPACE, "reports", "overflow_390_dump.json")
os.makedirs(os.path.join(WORKSPACE, "reports"), exist_ok=True)

# Run chrome and extract dump
cmd = [
    CHROME_PATH,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--hide-scrollbars",
    "--allow-file-access-from-files",
    "--window-size=390,844",
    "--virtual-time-budget=2000",
    "--dump-dom",
    "file:///" + temp_html.replace("\\", "/")
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")

if os.path.exists(temp_html):
    os.remove(temp_html)

import re
m = re.search(r'<pre id="audit-dump">(.*?)</pre>', res.stdout, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    print(f"Doc ScrollWidth: {data['docScrollWidth']}, Body ScrollWidth: {data['bodyScrollWidth']}")
    print(f"Total Overflowing Elements: {len(data['overflowingElements'])}\n")
    
    # Group by section or parent
    seen = set()
    for el in data['overflowingElements']:
        key = f"{el['tag']}.{el['className']}"
        if key not in seen:
            seen.add(key)
            print(f"- <{el['tag']} class='{el['className']}'> (id='{el['id']}')")
            print(f"    right={el['right']}px, width={el['width']}px, scrollWidth={el['scrollWidth']}px")
            print(f"    parent: {el['parent']}")
    
    with open(out_dump, "w", encoding="utf-8") as out_f:
        json.dump(data, out_f, indent=2)
else:
    print("Could not find audit dump in DOM output.")
