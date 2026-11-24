#!/usr/bin/env python3
"""
scripts/detect_mobile_overflow.py
Detects all elements causing horizontal overflow at viewport width 390px.
Loads index.html via file:// in headless Chrome, injects JS to inspect all DOM elements,
and prints any element whose getBoundingClientRect().right > 390 or scrollWidth > 390.
"""

import os
import subprocess
import json

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE = r"d:\Jewellery"
HTML_PATH = os.path.join(WORKSPACE, "index.html")

# Create a temporary runner html that executes overflow audit and dumps to console
audit_script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const vw = window.innerWidth;
    const docWidth = document.documentElement.scrollWidth;
    const bodyWidth = document.body.scrollWidth;
    
    console.log(`AUDIT_START: vw=${vw}, docScrollWidth=${docWidth}, bodyScrollWidth=${bodyWidth}`);
    
    const overflowing = [];
    const all = document.querySelectorAll('*');
    all.forEach(el => {
      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);
      
      const isHidden = style.display === 'none' || style.visibility === 'hidden' || rect.width === 0;
      if (isHidden) return;
      
      if (rect.right > vw + 1 || rect.left < -1 || el.scrollWidth > vw + 1) {
        overflowing.push({
          tag: el.tagName,
          id: el.id,
          className: el.className,
          rect: { left: Math.round(rect.left), right: Math.round(rect.right), width: Math.round(rect.width) },
          scrollWidth: el.scrollWidth,
          styleWidth: style.width,
          styleMinWidth: style.minWidth,
          styleMaxWidth: style.maxWidth,
          stylePadding: style.padding,
          styleMargin: style.margin,
          parent: el.parentElement ? `${el.parentElement.tagName}.${el.parentElement.className}` : null
        });
      }
    });
    
    console.log('AUDIT_RESULT:' + JSON.stringify(overflowing));
  }, 1000);
});
</script>
"""

with open(HTML_PATH, "r", encoding="utf-8") as f:
    base_html = f.read()

temp_html = os.path.join(WORKSPACE, "temp_overflow_audit.html")
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(base_html.replace("</body>", f"{audit_script}\n</body>"))

file_url = "file:///" + temp_html.replace("\\", "/")

cmd = [
    CHROME_PATH,
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    "--hide-scrollbars",
    "--allow-file-access-from-files",
    "--window-size=390,844",
    "--virtual-time-budget=3000",
    "--enable-logging=stderr",
    "--v=1",
    file_url
]

res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(temp_html):
    os.remove(temp_html)

output = res.stderr + "\n" + res.stdout

for line in output.splitlines():
    if "AUDIT_START" in line:
        print(line)
    if "AUDIT_RESULT:" in line:
        data = line.split("AUDIT_RESULT:")[1]
        try:
            items = json.loads(data)
            print(f"\nFound {len(items)} overflowing elements:")
            for idx, it in enumerate(items):
                print(f"[{idx+1}] <{it['tag']}> id='{it['id']}' class='{it['className']}'")
                print(f"     rect: left={it['rect']['left']}, right={it['rect']['right']}, width={it['rect']['width']} (vw=390)")
                print(f"     scrollWidth={it['scrollWidth']}, style: width={it['styleWidth']}, minWidth={it['styleMinWidth']}")
                print(f"     padding={it['stylePadding']}, margin={it['styleMargin']}")
                print(f"     parent={it['parent']}")
        except Exception as e:
            print("Failed to parse json:", e, line[:200])
