import os
import cv2
import numpy as np

thumb_dir = os.path.join('scripts', 'thumbs')

def get_contour_info(p):
    img = cv2.imread(p)
    h, w = img.shape[:2]
    # mask non-red
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m1 = cv2.inRange(hsv, np.array([0, 50, 40]), np.array([10, 255, 255]))
    m2 = cv2.inRange(hsv, np.array([170, 50, 40]), np.array([180, 255, 255]))
    red = m1 | m2
    
    if np.sum(red > 0) / (w * h) > 0.4:
        fg = cv2.bitwise_not(red)
    else:
        # Gray background
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, fg = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel)
    cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    large = [c for c in cnts if cv2.contourArea(c) > (w * h * 0.01)]
    return len(large), [cv2.boundingRect(c) for c in sorted(large, key=cv2.contourArea, reverse=True)[:3]]

# Let's check IMG_0034 to IMG_0044
print("--- 07_Fabric IMG_0034..0044 vs IMG_0062 ---")
for f in sorted(os.listdir(thumb_dir)):
    if any(k in f for k in ['0034', '0035', '0037', '0038', '0039', '0040', '0041', '0042', '0043', '0044', '0062']):
        p = os.path.join(thumb_dir, f)
        n, boxes = get_contour_info(p)
        fn = f.split('__')[1].replace('.jpg', '')
        print(f"{fn:20}: {n} contours, largest box={boxes[0] if boxes else 'None'}")

# Check 01_Earrings_Set_1 vs 02_Earrings_Set_2
print("\n--- 01_Earrings vs 02_Earrings ---")
for f in sorted(os.listdir(thumb_dir)):
    if '01_Earrings' in f or '02_Earrings' in f:
        p = os.path.join(thumb_dir, f)
        n, boxes = get_contour_info(p)
        fn = f.split('__')[1].replace('.jpg', '')
        fld = f.split('__')[0]
        print(f"{fld[:15]} | {fn:20}: {n} contours, boxes={boxes}")

# Check 05_Ornate vs 0299
print("\n--- 05_Ornate vs 08_IMG_0299 ---")
for f in sorted(os.listdir(thumb_dir)):
    if '05_Ornate' in f or '0299' in f:
        fn = f.split('__')[1].replace('.jpg', '')
        print(f"Ornate shot: {fn}")

# Check 06_Chain vs 0351..0355
print("\n--- 06_Chain vs 0351..0355 ---")
for f in sorted(os.listdir(thumb_dir)):
    if '06_Chain' in f or any(k in f for k in ['0351', '0352', '0353', '0354', '0355']):
        fn = f.split('__')[1].replace('.jpg', '')
        fld = f.split('__')[0]
        print(f"{fld[:20]} | {fn:20}")

# Check other files in 08_Dark and 09_Fastening and remaining
print("\n--- Other files in 08_Dark, 09_Fastening, remaining ---")
for f in sorted(os.listdir(thumb_dir)):
    if any(k in f for k in ['0231', '0235', '0329', '0444', '0588', '0828', '0839', '0360', '0143']):
        fn = f.split('__')[1].replace('.jpg', '')
        fld = f.split('__')[0]
        print(f"{fld[:20]} | {fn:20}")
