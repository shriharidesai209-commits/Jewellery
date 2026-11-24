import os
import cv2
import numpy as np
from PIL import Image

thumb_dir = os.path.join('scripts', 'thumbs')
crop_dir = os.path.join('scripts', 'crops')
os.makedirs(crop_dir, exist_ok=True)

# Let's crop the salient object from each thumbnail and save it
descriptions = {}

for fname in sorted(os.listdir(thumb_dir)):
    if not fname.endswith('.jpg'):
        continue
    img_p = os.path.join(thumb_dir, fname)
    img = cv2.imread(img_p)
    h, w = img.shape[:2]
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, np.array([0, 50, 40]), np.array([10, 255, 255]))
    mask2 = cv2.inRange(hsv, np.array([170, 50, 40]), np.array([180, 255, 255]))
    red_mask = mask1 | mask2
    
    # If dominant red background
    if np.sum(red_mask > 0) / (w * h) > 0.4:
        # Foreground is NOT red
        fg_mask = cv2.bitwise_not(red_mask)
        # Clean up noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Find largest or combined bounding box
            large_cnts = [c for c in contours if cv2.contourArea(c) > (w * h * 0.005)]
            if large_cnts:
                all_pts = np.vstack(large_cnts)
                bx, by, bw, bh = cv2.boundingRect(all_pts)
                # Expand slightly
                pad = 10
                x1, y1 = max(0, bx - pad), max(0, by - pad)
                x2, y2 = min(w, bx + bw + pad), min(h, by + bh + pad)
                crop = img[y1:y2, x1:x2]
            else:
                crop = img
        else:
            crop = img
    else:
        # Not a red background - might be closeup or grey background
        crop = img
        
    crop_path = os.path.join(crop_dir, fname)
    cv2.imwrite(crop_path, crop)
    
    # Get mean color of cropped foreground object
    crop_hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    # Exclude red if any
    mask1_c = cv2.inRange(crop_hsv, np.array([0, 50, 40]), np.array([10, 255, 255]))
    mask2_c = cv2.inRange(crop_hsv, np.array([170, 50, 40]), np.array([180, 255, 255]))
    non_red = cv2.bitwise_not(mask1_c | mask2_c)
    
    mean_val = cv2.mean(crop, mask=non_red)[:3]
    gold_cnt = np.sum(cv2.inRange(crop_hsv, np.array([15, 40, 70]), np.array([35, 255, 255])) > 0)
    white_cnt = np.sum(cv2.inRange(crop_hsv, np.array([0, 0, 180]), np.array([180, 60, 255])) > 0)
    
    total_pix = crop.shape[0] * crop.shape[1]
    descriptions[fname] = {
        'crop_shape': f"{crop.shape[1]}x{crop.shape[0]}",
        'fg_bgr': [round(v, 1) for v in mean_val],
        'gold_ratio': round(gold_cnt / total_pix, 3),
        'white_ratio': round(white_cnt / total_pix, 3)
    }

print("Cropped salient areas and computed foreground properties.")
