import os
import cv2
import numpy as np
from PIL import Image

thumb_dir = os.path.join('scripts', 'thumbs')

# Let's inspect images in 07_Fabric_Background_Reference, 08_Dark_or_Unclear_Review, 09_Fastening_or_Extra_View, etc.
def analyze_image_detail(fname):
    fpath = os.path.join(thumb_dir, fname)
    img = cv2.imread(fpath)
    if img is None:
        return "Failed to load"
    h, w, _ = img.shape
    
    # Analyze center region (where jewellery usually lies) vs outer border
    cw, ch = int(w * 0.5), int(h * 0.5)
    cx, cy = int(w * 0.25), int(h * 0.25)
    center_roi = img[cy:cy+ch, cx:cx+cw]
    
    # Outer border
    border_mask = np.ones((h, w), dtype=bool)
    border_mask[cy:cy+ch, cx:cx+cw] = False
    
    center_gray = cv2.cvtColor(center_roi, cv2.COLOR_BGR2GRAY)
    center_lap = cv2.Laplacian(center_gray, cv2.CV_64F).var()
    center_mean = cv2.mean(center_roi)[:3]
    
    # Color differences between center and border
    border_mean = cv2.mean(img, mask=(~border_mask).astype(np.uint8))[:3]
    color_diff = np.linalg.norm(np.array(center_mean) - np.array(border_mean))
    
    # Gold / yellow pixels in center
    hsv_center = cv2.cvtColor(center_roi, cv2.COLOR_BGR2HSV)
    gold_mask = cv2.inRange(hsv_center, np.array([15, 40, 70]), np.array([35, 255, 255]))
    gold_pct = np.sum(gold_mask > 0) / (cw * ch) * 100
    
    # White / bright sparkle in center
    sparkle_mask = cv2.inRange(hsv_center, np.array([0, 0, 200]), np.array([180, 60, 255]))
    sparkle_pct = np.sum(sparkle_mask > 0) / (cw * ch) * 100
    
    # Check edges
    edges = cv2.Canny(center_gray, 50, 150)
    edge_pct = np.sum(edges > 0) / (cw * ch) * 100
    
    return {
        'center_lap': round(center_lap, 1),
        'center_mean_bgr': [round(v, 1) for v in center_mean],
        'color_diff': round(color_diff, 1),
        'gold_pct': round(gold_pct, 1),
        'sparkle_pct': round(sparkle_pct, 1),
        'edge_pct': round(edge_pct, 1)
    }

print("=== Analyzing images in folders ===")
for fname in sorted(os.listdir(thumb_dir)):
    if not fname.endswith('.jpg'):
        continue
    stats = analyze_image_detail(fname)
    name = fname.replace('__', '/').replace('.jpg', '')
    print(f"{name:50} | CenterLap:{stats['center_lap']:7.1f} | Gold:{stats['gold_pct']:4.1f}% | Sparkle:{stats['sparkle_pct']:4.1f}% | Edges:{stats['edge_pct']:4.1f}%")
