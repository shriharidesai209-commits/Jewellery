#!/usr/bin/env python3
import json
import os
from PIL import Image

with open('data/products.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for p in catalog['products']:
    pid = p['id']
    name = p['name']
    print(f"\n=== {pid}: {name} ===")
    for role, paths in p['images'].items():
        if isinstance(paths, dict):
            for fmt, rel in paths.items():
                if isinstance(rel, str) and (rel.endswith('.webp') or rel.endswith('.jpg') or rel.endswith('.png')):
                    if os.path.exists(rel):
                        with Image.open(rel) as im:
                            print(f"  {role:8} ({fmt:4}): {rel:58} | {im.size} | {im.format}")
                    else:
                        print(f"  {role:8} ({fmt:4}): {rel:58} | MISSING!")
