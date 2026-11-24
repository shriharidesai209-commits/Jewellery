import os
import cv2
import numpy as np

thumb_dir = os.path.join('scripts', 'thumbs')

# Let's inspect the color palettes of the jewelry objects in each image
def get_dominant_colors(crop, k=4):
    pixels = crop.reshape(-1, 3).astype(np.float32)
    # Filter out pure black or extreme background
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    try:
        compactness, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, flags)
        counts = np.bincount(labels.flatten())
        sorted_indices = np.argsort(counts)[::-1]
        res = []
        for idx in sorted_indices:
            b, g, r = centers[idx]
            pct = counts[idx] / len(pixels) * 100
            res.append((round(r, 1), round(g, 1), round(b, 1), round(pct, 1)))
        return res
    except:
        return []

# Inspect each category
for f in sorted(os.listdir(thumb_dir)):
    if not f.endswith('.jpg'):
        continue
    img = cv2.imread(os.path.join(thumb_dir, f))
    # Salient center
    h, w = img.shape[:2]
    c_img = img[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]
    colors = get_dominant_colors(c_img, k=3)
    folder = f.split('__')[0]
    fname = f.split('__')[1].replace('.jpg', '')
    col_str = " | ".join([f"RGB({c[0]},{c[1]},{c[2]}): {c[3]}%" for c in colors])
    print(f"{fname:22} [{folder[:20]:20}] -> {col_str}")
