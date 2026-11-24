import os
import cv2
import numpy as np
from PIL import Image

thumb_dir = os.path.join('scripts', 'thumbs')

# Let's inspect each image's geometry and composition
files = sorted([f for f in os.listdir(thumb_dir) if f.endswith('.jpg')])

for f in files:
    p = os.path.join(thumb_dir, f)
    img = cv2.imread(p)
    h, w = img.shape[:2]
    
    # Check if image has human skin (fingers/hands holding jewellery)
    # Skin color in YCrCb: Y in [0, 255], Cr in [133, 173], Cb in [77, 127]
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    skin_mask = cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127]))
    # Red fabric also has high Cr, so we must separate skin from red fabric:
    # In HSV, skin has H in [0, 25], S in [30, 170], V > 80
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    skin_hsv = cv2.inRange(hsv, np.array([0, 30, 80]), np.array([25, 170, 255]))
    skin = (skin_mask > 0) & (skin_hsv > 0)
    skin_pct = np.sum(skin) / (w * h) * 100
    
    # Check aspect ratio of thumbnail
    ar = w / h
    
    # Name breakdown
    folder = f.split('__')[0]
    fname = f.split('__')[1].replace('.jpg', '')
    
    # White / sticker / tag / ruler detection: bright white rect
    white_mask = cv2.inRange(hsv, np.array([0, 0, 210]), np.array([180, 40, 255]))
    white_pct = np.sum(white_mask > 0) / (w * h) * 100
    
    print(f"{folder[:25]:25} | {fname:20} | AR:{ar:.2f} | Skin:{skin_pct:4.1f}% | White:{white_pct:4.1f}%")
