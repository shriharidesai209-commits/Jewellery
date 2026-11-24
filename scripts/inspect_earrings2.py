import os
import cv2
import numpy as np

# Detailed inspection of 02_Earrings_Set_2 photos
crop_dir = os.path.join('scripts', 'extracted_objects')

files = [f for f in sorted(os.listdir(crop_dir)) if '02_Earrings' in f]
for f in files:
    img = cv2.imread(os.path.join(crop_dir, f))
    h, w = img.shape[:2]
    # Check text or numbers, colors, aspect ratio
    print(f"02_Earrings photo: {f:45} | Size: {w}x{h}")
