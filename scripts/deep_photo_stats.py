import os
import cv2
import numpy as np
from PIL import Image

thumb_dir = os.path.join('scripts', 'thumbs')

# Let's inspect each image and classify:
# 1. Image quality (brightness, contrast, sharpness, blur flag, dark flag, overexposed flag)
# 2. Presence of fingers/hands (skin detected in contact with product)
# 3. Presence of rulers/scales/measurement tape
# 4. View type (front, angle/side, close-up, back/fastening, scale reference, texture/reference only)
# 5. Visual product identification

def analyze_photo(fname):
    p = os.path.join(thumb_dir, fname)
    img = cv2.imread(p)
    h, w = img.shape[:2]
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    mean_b = float(np.mean(gray))
    std_b = float(np.std(gray))
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Red fabric background
    mask1 = cv2.inRange(hsv, np.array([0, 50, 40]), np.array([10, 255, 255]))
    mask2 = cv2.inRange(hsv, np.array([170, 50, 40]), np.array([180, 255, 255]))
    red_pct = np.sum((mask1 | mask2) > 0) / (w * h) * 100
    
    # Grey/neutral background
    grey_mask = cv2.inRange(hsv, np.array([0, 0, 50]), np.array([180, 40, 220]))
    grey_pct = np.sum(grey_mask > 0) / (w * h) * 100
    
    # Dark background (black/charcoal)
    dark_mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 45]))
    dark_bg_pct = np.sum(dark_mask > 0) / (w * h) * 100
    
    # Gold pixels
    gold_mask = cv2.inRange(hsv, np.array([15, 40, 70]), np.array([35, 255, 255]))
    gold_pct = np.sum(gold_mask > 0) / (w * h) * 100
    
    # Silver/white sparkle
    sparkle_mask = cv2.inRange(hsv, np.array([0, 0, 200]), np.array([180, 60, 255]))
    sparkle_pct = np.sum(sparkle_mask > 0) / (w * h) * 100
    
    # Skin detection
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    skin_mask = cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127]))
    skin_hsv = cv2.inRange(hsv, np.array([0, 30, 80]), np.array([25, 170, 255]))
    skin = (skin_mask > 0) & (skin_hsv > 0)
    skin_pct = np.sum(skin) / (w * h) * 100
    
    return {
        'brightness': round(mean_b, 1),
        'contrast': round(std_b, 1),
        'sharpness': round(lap_var, 1),
        'red_bg': round(red_pct, 1),
        'grey_bg': round(grey_pct, 1),
        'dark_bg': round(dark_bg_pct, 1),
        'gold': round(gold_pct, 1),
        'sparkle': round(sparkle_pct, 1),
        'skin': round(skin_pct, 1)
    }

for f in sorted(os.listdir(thumb_dir)):
    if not f.endswith('.jpg'):
        continue
    stats = analyze_photo(f)
    print(f"{f.replace('.jpg', ''):55} | B:{stats['brightness']:5.1f} | S:{stats['sharpness']:6.1f} | Red:{stats['red_bg']:4.1f}% | Grey:{stats['grey_bg']:4.1f}% | Dark:{stats['dark_bg']:4.1f}% | Gold:{stats['gold']:4.1f}% | Skin:{stats['skin']:4.1f}%")
