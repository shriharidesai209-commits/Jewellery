import os
import json
import pillow_heif
from PIL import Image, ImageOps, ImageDraw, ImageFont
import cv2
import numpy as np

pillow_heif.register_heif_opener()

extract_dir = os.path.join('assets', 'raw-jewellery', 'extracted')
thumb_dir = os.path.join('scripts', 'thumbs')
os.makedirs(thumb_dir, exist_ok=True)

with open('scripts/raw_inventory.json', 'r', encoding='utf-8') as f:
    inventory = json.load(f)

# Generate normalized thumbnails for visual analysis and contact sheets
print("Generating thumbnails...")
for item in inventory:
    path = os.path.join(extract_dir, item['rel_path'])
    out_thumb = os.path.join(thumb_dir, item['rel_path'].replace('/', '__').replace('\\', '__') + '.jpg')
    item['thumb_path'] = out_thumb
    
    with Image.open(path) as img:
        # EXIF transpose handles orientation
        img_transposed = ImageOps.exif_transpose(img)
        rgb = img_transposed.convert('RGB')
        
        # Save high quality 600px max thumbnail
        rgb.thumbnail((800, 800), Image.Resampling.LANCZOS)
        rgb.save(out_thumb, 'JPEG', quality=85)
        
        # Compute color histogram
        np_rgb = np.array(rgb)
        hsv = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2HSV)
        # Dominant colors / hue distribution
        h_hist = cv2.calcHist([hsv], [0], None, [18], [0, 180]).flatten()
        h_hist = h_hist / (h_hist.sum() + 1e-6)
        item['h_hist'] = [round(float(v), 4) for v in h_hist]

# Check pairwise perceptual distances (Hamming distance of dhash)
print("Computing pairwise duplicate / similarity matrix...")
duplicates_or_near = []
n = len(inventory)
for i in range(n):
    dhash_i = int(inventory[i]['dhash'], 16)
    for j in range(i + 1, n):
        dhash_j = int(inventory[j]['dhash'], 16)
        # Hamming distance
        xor_val = dhash_i ^ dhash_j
        hamming_dist = bin(xor_val).count('1')
        
        # Also histogram correlation
        hist_i = np.array(inventory[i]['h_hist'], dtype=np.float32)
        hist_j = np.array(inventory[j]['h_hist'], dtype=np.float32)
        hist_corr = float(cv2.compareHist(hist_i, hist_j, cv2.HISTCMP_CORREL))
        
        if hamming_dist <= 10 or (hamming_dist <= 15 and hist_corr > 0.85):
            duplicates_or_near.append({
                'img1': inventory[i]['rel_path'],
                'img2': inventory[j]['rel_path'],
                'hamming_dist': hamming_dist,
                'hist_corr': round(hist_corr, 3)
            })

print(f"Found {len(duplicates_or_near)} potential near-duplicate / highly similar pairs:")
for pair in duplicates_or_near:
    print(f"  {pair['img1']} <--> {pair['img2']} (dist={pair['hamming_dist']}, corr={pair['hist_corr']})")

with open('scripts/similarity_analysis.json', 'w', encoding='utf-8') as f:
    json.dump({
        'duplicates_or_near': duplicates_or_near,
        'inventory_with_thumbs': inventory
    }, f, indent=2)

print("Done thumbnail generation and similarity analysis.")
