import os
import zipfile
import json
import csv
import pillow_heif
from PIL import Image, ExifTags
import cv2
import numpy as np

pillow_heif.register_heif_opener()

zip_path = os.path.join('assets', 'raw-jewellery', 'received_photos.zip')
extract_dir = os.path.join('assets', 'raw-jewellery', 'extracted')
os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_dir)
print(f"Extracted zip to {extract_dir}")

all_files = []
for root, dirs, files in os.walk(extract_dir):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp', '.bmp', '.tif', '.tiff')):
            all_files.append(os.path.join(root, f))

print(f"Found {len(all_files)} images.")

def compute_dhash(image, hash_size=8):
    image = image.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = np.array(image.getdata(), dtype=np.float32).reshape((hash_size, hash_size + 1))
    diff = pixels[:, 1:] > pixels[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

inventory = []
for path in sorted(all_files):
    rel_path = os.path.relpath(path, extract_dir)
    stat = os.stat(path)
    try:
        with Image.open(path) as img:
            w, h = img.size
            fmt = img.format
            mode = img.mode
            
            orientation = 1
            exif = img.getexif()
            if exif:
                orientation = exif.get(0x0112, 1)

            rgb_img = img.convert('RGB')
            if orientation == 3:
                rgb_img = rgb_img.rotate(180, expand=True)
            elif orientation == 6:
                rgb_img = rgb_img.rotate(270, expand=True)
            elif orientation == 8:
                rgb_img = rgb_img.rotate(90, expand=True)
                
            np_img = np.array(rgb_img)
            gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
            
            lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
            mean_b = float(np.mean(gray))
            std_b = float(np.std(gray))
            
            r_m = float(np.mean(np_img[:, :, 0]))
            g_m = float(np.mean(np_img[:, :, 1]))
            b_m = float(np.mean(np_img[:, :, 2]))
            
            dhash_val = f"{compute_dhash(rgb_img):016x}"
            
            inventory.append({
                'rel_path': rel_path.replace('\\', '/'),
                'filename': os.path.basename(path),
                'folder': os.path.dirname(rel_path).replace('\\', '/'),
                'format': fmt,
                'width': w,
                'height': h,
                'orientation': orientation,
                'size_bytes': stat.st_size,
                'laplacian_variance': round(lap_var, 2),
                'mean_brightness': round(mean_b, 2),
                'std_contrast': round(std_b, 2),
                'rgb_means': [round(r_m, 1), round(g_m, 1), round(b_m, 1)],
                'dhash': dhash_val
            })
    except Exception as e:
        inventory.append({
            'rel_path': rel_path.replace('\\', '/'),
            'filename': os.path.basename(path),
            'error': str(e)
        })

print(f"Successfully processed {len(inventory)} images.")

# Save raw inventory json for inspection
os.makedirs('scripts', exist_ok=True)
with open('scripts/raw_inventory.json', 'w', encoding='utf-8') as f:
    json.dump(inventory, f, indent=2)

for item in inventory:
    print(f"{item['rel_path']} | {item.get('format')} | {item.get('width')}x{item.get('height')} | Size: {item.get('size_bytes',0)/1024:.1f}KB | Brightness: {item.get('mean_brightness')} | Contrast: {item.get('std_contrast')} | Sharpness: {item.get('laplacian_variance')}")
