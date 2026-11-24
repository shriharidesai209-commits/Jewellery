import os
import cv2
import numpy as np

thumb_dir = os.path.join('scripts', 'thumbs')
obj_dir = os.path.join('scripts', 'extracted_objects')
os.makedirs(obj_dir, exist_ok=True)

files = sorted([f for f in os.listdir(thumb_dir) if f.endswith('.jpg')])

report = []

for f in files:
    p = os.path.join(thumb_dir, f)
    img = cv2.imread(p)
    h, w = img.shape[:2]
    
    # Background segmentation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Red background mask
    m1 = cv2.inRange(hsv, np.array([0, 45, 35]), np.array([12, 255, 255]))
    m2 = cv2.inRange(hsv, np.array([168, 45, 35]), np.array([180, 255, 255]))
    red_mask = m1 | m2
    
    # Grey background mask
    grey_mask = cv2.inRange(hsv, np.array([0, 0, 50]), np.array([180, 35, 235]))
    
    # Black/dark background mask
    dark_mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 45]))
    
    # Hand/skin mask
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    skin_mask = (cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127])) > 0) & \
                (cv2.inRange(hsv, np.array([0, 30, 80]), np.array([25, 170, 255])) > 0)
    
    # Decide primary background
    r_pct = np.sum(red_mask > 0) / (w * h)
    g_pct = np.sum(grey_mask > 0) / (w * h)
    d_pct = np.sum(dark_mask > 0) / (w * h)
    
    if r_pct > 0.4:
        bg_name = "Red Fabric"
        obj_mask = (~red_mask).astype(np.uint8) * 255
    elif g_pct > 0.3:
        bg_name = "Grey/Neutral Surface"
        obj_mask = (~grey_mask).astype(np.uint8) * 255
    elif d_pct > 0.35:
        bg_name = "Dark/Black"
        obj_mask = (~dark_mask).astype(np.uint8) * 255
    else:
        bg_name = "Mixed"
        obj_mask = np.ones((h, w), dtype=np.uint8) * 255
        
    # Remove skin from jewellery object mask if skin is detected
    jewel_mask = obj_mask.copy()
    jewel_mask[skin_mask] = 0
    
    # Clean up
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    jewel_clean = cv2.morphologyEx(jewel_mask, cv2.MORPH_OPEN, kernel)
    jewel_clean = cv2.morphologyEx(jewel_clean, cv2.MORPH_CLOSE, kernel)
    
    cnts, _ = cv2.findContours(jewel_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    large_cnts = [c for c in cnts if cv2.contourArea(c) > (w * h * 0.005)]
    
    if large_cnts:
        all_pts = np.vstack(large_cnts)
        bx, by, bw, bh = cv2.boundingRect(all_pts)
        pad = 12
        x1, y1 = max(0, bx - pad), max(0, by - pad)
        x2, y2 = min(w, bx + bw + pad), min(h, by + bh + pad)
        crop = img[y1:y2, x1:x2]
        
        # Calculate circularity and aspect ratio of largest contour
        c0 = max(large_cnts, key=cv2.contourArea)
        area = cv2.contourArea(c0)
        perimeter = cv2.arcLength(c0, True)
        circularity = 4 * np.pi * area / (perimeter * perimeter + 1e-6)
        obj_ar = bw / max(bh, 1)
    else:
        crop = img
        circularity = 0
        obj_ar = w / h
        bw, bh = w, h
        
    out_crop_p = os.path.join(obj_dir, f)
    cv2.imwrite(out_crop_p, crop)
    
    # Jewelry colors in crop
    c_hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    gold_pct = np.sum(cv2.inRange(c_hsv, np.array([15, 40, 70]), np.array([35, 255, 255])) > 0) / (crop.shape[0] * crop.shape[1])
    gem_pct = np.sum(cv2.inRange(c_hsv, np.array([0, 0, 180]), np.array([180, 50, 255])) > 0) / (crop.shape[0] * crop.shape[1])
    
    folder = f.split('__')[0]
    fname = f.split('__')[1].replace('.jpg', '')
    
    report.append({
        'folder': folder,
        'filename': fname,
        'bg': bg_name,
        'skin_pct': round(float(np.sum(skin_mask)/(w*h)*100), 1),
        'obj_box': f"{bw}x{bh}",
        'obj_ar': round(obj_ar, 2),
        'circularity': round(circularity, 3),
        'gold_pct': round(gold_pct*100, 1),
        'gem_pct': round(gem_pct*100, 1)
    })

print(f"Extracted {len(report)} objects. Showing summary:")
for r in report:
    print(f"{r['filename']:20} [{r['folder'][:18]:18}] | BG:{r['bg']:15} | Obj:{r['obj_box']:9} AR:{r['obj_ar']:4.2f} Circ:{r['circularity']:5.3f} | Gold:{r['gold_pct']:4.1f}% Gems:{r['gem_pct']:4.1f}% Skin:{r['skin_pct']:4.1f}%")
