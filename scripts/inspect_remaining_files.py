import os
import cv2
import numpy as np

thumb_dir = os.path.join('scripts', 'thumbs')

files_to_check = [
    ('IMG_0235', '07_Fabric_Background_Reference__IMG_0235.HEIC.jpg'),
    ('IMG_0360', '07_Fabric_Background_Reference__IMG_0360.HEIC.jpg'),
    ('IMG_0231', '08_Dark_or_Unclear_Review__IMG_0231.HEIC.jpg'),
    ('IMG_0329', '08_Dark_or_Unclear_Review__IMG_0329.HEIC.jpg'),
    ('IMG_0444', '08_Dark_or_Unclear_Review__IMG_0444.HEIC.jpg'),
    ('IMG_0588', '08_Dark_or_Unclear_Review__IMG_0588.HEIC.jpg'),
    ('IMG_0828', '08_Dark_or_Unclear_Review__IMG_0828.HEIC.jpg'),
    ('IMG_0839', '09_Fastening_or_Extra_View__IMG_0839.JPG.jpeg.jpg'),
    ('IMG_0143', '04_Long_Necklace_IMG_0143__IMG_0143.PNG.jpg')
]

for label, fname in files_to_check:
    p = os.path.join(thumb_dir, fname)
    img = cv2.imread(p)
    h, w = img.shape[:2]
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Check non-red
    m1 = cv2.inRange(hsv, np.array([0, 50, 40]), np.array([10, 255, 255]))
    m2 = cv2.inRange(hsv, np.array([170, 50, 40]), np.array([180, 255, 255]))
    non_red = ~(m1 | m2)
    
    cnts, _ = cv2.findContours(non_red.astype(np.uint8)*255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    large = [c for c in cnts if cv2.contourArea(c) > 300]
    
    print(f"\n=== {label} ({fname}) ===")
    print(f"  Dims: {w}x{h}, MeanGray: {np.mean(gray):.1f}, Lap: {cv2.Laplacian(gray, cv2.CV_64F).var():.1f}")
    print(f"  Non-red percentage: {np.sum(non_red)/(w*h)*100:.1f}%")
    for i, c in enumerate(sorted(large, key=cv2.contourArea, reverse=True)[:3]):
        bx, by, bw, bh = cv2.boundingRect(c)
        print(f"  Contour {i}: Box:({bx},{by},{bw}x{bh}), Area:{cv2.contourArea(c)}")
