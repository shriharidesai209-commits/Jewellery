import os
import cv2
import numpy as np
from PIL import Image

thumb_dir = os.path.join('scripts', 'thumbs')

print("Analyzing visual contents of thumbnails...")

results = []
for fname in sorted(os.listdir(thumb_dir)):
    if not fname.endswith('.jpg'):
        continue
    fpath = os.path.join(thumb_dir, fname)
    img = cv2.imread(fpath)
    if img is None:
        continue
    h, w, c = img.shape
    
    # Analyze color distribution in BGR
    b_mean, g_mean, r_mean = [float(v) for v in cv2.mean(img)[:3]]
    
    # Red dominance test (useful for red fabric vs neutral/gold/grey)
    is_red_fabric = (r_mean > 120 and g_mean < 80 and b_mean < 80 and r_mean > 1.5 * max(g_mean, b_mean))
    
    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Detect metallic/gold or bright reflections
    # Gold/yellow: H in [15, 35], S in [50, 255], V in [100, 255]
    gold_mask = cv2.inRange(hsv, np.array([15, 40, 70]), np.array([35, 255, 255]))
    gold_ratio = float(np.sum(gold_mask > 0)) / (w * h)
    
    # Bright highlights (gems/metallic reflections): V > 220, S < 80
    sparkle_mask = cv2.inRange(hsv, np.array([0, 0, 220]), np.array([180, 80, 255]))
    sparkle_ratio = float(np.sum(sparkle_mask > 0)) / (w * h)
    
    # Saliency / object detection using edge density & central region contrast
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = float(np.sum(edges > 0)) / (w * h)
    
    # Background vs foreground segmentation attempt (Otsu threshold on gray)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    results.append({
        'thumb_name': fname,
        'r_mean': round(r_mean, 1),
        'g_mean': round(g_mean, 1),
        'b_mean': round(b_mean, 1),
        'gold_ratio': round(gold_ratio, 4),
        'sparkle_ratio': round(sparkle_ratio, 4),
        'edge_density': round(edge_density, 4),
        'is_red_fabric': is_red_fabric
    })

print(f"Computed visual features for {len(results)} images.")
for r in results:
    orig_name = r['thumb_name'].replace('__', '/').replace('.jpg', '')
    print(f"{orig_name[:45]:45} | R:{r['r_mean']:5.1f} G:{r['g_mean']:5.1f} B:{r['b_mean']:5.1f} | Gold:{r['gold_ratio']:6.3f} | Sparkle:{r['sparkle_ratio']:6.3f} | Edges:{r['edge_density']:6.3f}")
