import os
import cv2
import numpy as np

thumb_dir = os.path.join('scripts', 'thumbs')

# Let's inspect 02_Earrings in detail
for fn in ["IMG_0437.JPG.jpeg", "IMG_0438.JPG.jpeg", "IMG_0439.JPG.jpeg", "IMG_0440.JPG.jpeg", "IMG_0441.JPG.jpeg", "IMG_0442.JPG.jpeg"]:
    p = os.path.join(thumb_dir, f"02_Earrings_Set_2_0437__{fn}.jpg")
    img = cv2.imread(p)
    h, w = img.shape[:2]
    
    # Locate where the non-red object is in this 450x800 image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m1 = cv2.inRange(hsv, np.array([0, 50, 40]), np.array([10, 255, 255]))
    m2 = cv2.inRange(hsv, np.array([170, 50, 40]), np.array([180, 255, 255]))
    non_red = cv2.bitwise_not(m1 | m2)
    
    # Exclude skin
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    skin = (cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127])) > 0) & \
           (cv2.inRange(hsv, np.array([0, 30, 80]), np.array([25, 170, 255])) > 0)
    
    jewel = non_red & (~skin)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    jewel = cv2.morphologyEx(jewel, cv2.MORPH_OPEN, kernel)
    
    cnts, _ = cv2.findContours(jewel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = [cv2.boundingRect(c) for c in cnts if cv2.contourArea(c) > 200]
    
    print(f"{fn:20}: Object boxes: {boxes}")
