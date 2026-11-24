import os
import json
import base64

with open('scripts/raw_inventory.json', 'r', encoding='utf-8') as f:
    inv = json.load(f)

# Build an HTML inspector
html = ['<!DOCTYPE html><html><head><meta charset="utf-8"><title>Visual Image Inspector</title>',
        '<style>body{font-family:sans-serif;background:#18181b;color:#e4e4e7;padding:20px;}',
        'h1,h2{color:#f43f5e;border-bottom:1px solid #3f3f46;padding-bottom:6px;}',
        '.grid{display:grid;grid-template-columns:repeat(auto-fill, minmax(280px, 1fr));gap:16px;margin-bottom:30px;}',
        '.card{background:#27272a;border-radius:8px;overflow:hidden;border:1px solid #3f3f46;box-shadow:0 4px 6px rgba(0,0,0,0.3);}',
        '.card img{width:100%;height:220px;object-fit:contain;background:#09090b;}',
        '.info{padding:10px;font-size:12px;line-height:1.5;}',
        '.fn{font-weight:bold;color:#38bdf8;font-size:13px;word-break:break-all;}',
        '.badge{display:inline-block;padding:2px 6px;border-radius:4px;font-size:11px;font-weight:bold;margin-right:4px;}',
        '.badge-dark{background:#713f12;color:#fde047;}',
        '.badge-blur{background:#831843;color:#fbcfe8;}',
        '.badge-ok{background:#064e3b;color:#6ee7b7;}',
        '</style></head><body><h1>Jewellery Photo Curation Inspector</h1>']

by_folder = {}
for item in inv:
    fld = item['folder']
    by_folder.setdefault(fld, []).append(item)

for fld, items in by_folder.items():
    html.append(f'<h2>Folder: {fld} ({len(items)} photos)</h2><div class="grid">')
    for it in items:
        fn = it['filename']
        thumb = 'thumbs/' + it['rel_path'].replace('/', '__').replace('\\', '__') + '.jpg'
        b = it.get('mean_brightness', 0)
        c = it.get('std_contrast', 0)
        s = it.get('laplacian_variance', 0)
        w, h = it.get('width', 0), it.get('height', 0)
        fmt = it.get('format', '')
        
        badges = []
        if b < 60:
            badges.append('<span class="badge badge-dark">DARK</span>')
        elif b > 140:
            badges.append('<span class="badge badge-dark">OVEREXPOSED</span>')
        if s < 50:
            badges.append('<span class="badge badge-blur">BLURRY</span>')
        if not badges:
            badges.append('<span class="badge badge-ok">CLEAN</span>')
            
        badge_html = ' '.join(badges)
        html.append(f'''<div class="card">
            <img src="{thumb}" loading="lazy" />
            <div class="info">
                <div class="fn">{fn}</div>
                <div>Format: {fmt} | {w}x{h}</div>
                <div>Brightness: {b} | Contrast: {c} | Sharp: {s}</div>
                <div>Status: {badge_html}</div>
            </div>
        </div>''')
    html.append('</div>')

html.append('</body></html>')

with open('scripts/inspector.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(html))

print("Created scripts/inspector.html")
