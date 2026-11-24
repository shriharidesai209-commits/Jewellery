import os
import cv2
import numpy as np
from PIL import Image

thumb_dir = os.path.join('scripts', 'thumbs')

# Let's inspect each folder specifically
folders = sorted(list(set([f.split('__')[0] for f in os.listdir(thumb_dir) if '__' in f])))

for fld in folders:
    print(f"\n=================== FOLDER: {fld} ===================")
    files = [f for f in sorted(os.listdir(thumb_dir)) if f.startswith(fld + '__')]
    for f in files:
        img_p = os.path.join(thumb_dir, f)
        img = cv2.imread(img_p)
        h, w = img.shape[:2]
        
        # Detect bright / non-background areas
        # Red background detection (since red velvet is often used)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Red fabric mask
        mask1 = cv2.inRange(hsv, np.array([0, 50, 40]), np.array([10, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([170, 50, 40]), np.array([180, 255, 255]))
        red_bg_mask = mask1 | mask2
        red_bg_ratio = np.sum(red_bg_mask > 0) / (w * h)
        
        # Grey / neutral background detection
        # Low saturation: S < 40, V between 50 and 220
        grey_bg_mask = cv2.inRange(hsv, np.array([0, 0, 50]), np.array([180, 40, 220]))
        grey_bg_ratio = np.sum(grey_bg_mask > 0) / (w * h)
        
        # Object mask (anything not background)
        # If red background is dominant
        if red_bg_ratio > 0.4:
            obj_mask = (~red_bg_mask).astype(np.uint8) * 255
            bg_type = f"Red Fabric ({red_bg_ratio*100:.1f}%)"
        elif grey_bg_ratio > 0.4:
            obj_mask = (~grey_bg_mask).astype(np.uint8) * 255
            bg_type = f"Grey/Neutral ({grey_bg_ratio*100:.1f}%)"
        else:
            bg_type = f"Mixed/Other (Red:{red_bg_ratio*100:.1f}%, Grey:{grey_bg_ratio*100:.1f}%)"
            obj_mask = np.ones((h, w), dtype=np.uint8) * 255

        # Clean mask with morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        obj_clean = cv2.morphologyEx(obj_mask, cv2.MORPH_OPEN, kernel)
        obj_clean = cv2.morphologyEx(obj_clean, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(obj_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Filter contours by area
        valid_cnts = [c for c in contours if cv2.contourArea(c) > (w * h * 0.01)]
        
        obj_info = []
        for c in sorted(valid_cnts, key=cv2.contourArea, reverse=True)[:3]:
            bx, by, bw, bh = cv2.boundingRect(c)
            area_pct = cv2.contourArea(c) / (w * h) * 100
            aspect = bh / max(bw, 1)
            obj_info.append(f"Box:[{bx},{by},{bw}x{bh}, ar={aspect:.2f}, area={area_pct:.1f}%]")

        fname_clean = f.split('__')[1].replace('.jpg', '')
        print(f"File: {fname_clean:22} | BG: {bg_type:28} | Objs: {len(valid_cnts)} | {', '.join(obj_info[:2])}")
