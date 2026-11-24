#!/usr/bin/env python3
"""
Comprehensive Inventory & Deep Visual Audit of All 43 Original Jewellery Images.
"""

import os
import json
import pillow_heif
from PIL import Image

pillow_heif.register_heif_opener()

WORKSPACE = r"d:\Jewellery"
EXTRACT_DIR = os.path.join(WORKSPACE, "assets", "raw-jewellery", "extracted")

# Load existing raw_inventory.json for metrics
raw_inv_path = os.path.join(WORKSPACE, "scripts", "raw_inventory.json")
raw_inv_dict = {}
if os.path.exists(raw_inv_path):
    with open(raw_inv_path, "r", encoding="utf-8") as f:
        for item in json.load(f):
            raw_inv_dict[item["filename"]] = item

all_items = []
for root, dirs, files in os.walk(EXTRACT_DIR):
    for f in sorted(files):
        if not f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp')):
            continue
        full_path = os.path.join(root, f)
        folder = os.path.relpath(root, EXTRACT_DIR).replace("\\", "/")
        sz = os.path.getsize(full_path)
        try:
            with Image.open(full_path) as img:
                w, h = img.size
                fmt = img.format
                exif = img.getexif()
                orient = exif.get(0x0112, 1) if exif else 1
                cw, ch = (h, w) if orient in (6, 8) else (w, h)
        except Exception as e:
            w, h, fmt, orient, cw, ch = 0, 0, "ERR", 1, 0, 0

        metric = raw_inv_dict.get(f, {})
        all_items.append({
            "folder": folder,
            "filename": f,
            "format": fmt,
            "raw_dim": f"{w}x{h}",
            "corrected_dim": f"{cw}x{ch}",
            "orientation": orient,
            "size_bytes": sz,
            "size_kb": round(sz / 1024, 1),
            "size_mb": round(sz / (1024 * 1024), 2),
            "brightness": metric.get("mean_brightness", None),
            "contrast": metric.get("std_contrast", None),
            "laplacian_variance": metric.get("laplacian_variance", None),
            "dhash": metric.get("dhash", None)
        })

print(f"Total original images cataloged: {len(all_items)}")

# Print breakdown by folder
by_folder = {}
for item in all_items:
    by_folder.setdefault(item["folder"], []).append(item)

for folder, items in sorted(by_folder.items()):
    print(f"\nFolder: {folder} ({len(items)} files)")
    for it in items:
        print(f"  {it['filename']:22} | {it['format']:5} | Raw: {it['raw_dim']:9} | Display: {it['corrected_dim']:9} | {it['size_kb']:7} KB | BlurVar: {it['laplacian_variance']}")

# Export detailed inventory to JSON for structured analysis
out_json = os.path.join(WORKSPACE, "reports", "complete_raw_inventory.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(all_items, f, indent=2)

print(f"\nSaved complete raw inventory to {out_json}")
