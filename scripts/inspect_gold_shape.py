import os
import cv2
import numpy as np

p = 'scripts/thumbs/07_Fabric_Background_Reference__IMG_0037.HEIC.jpg'
img = cv2.imread(p)
h, w = img.shape[:2]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
gold_mask = (hsv[:,:,0] >= 15) & (hsv[:,:,0] <= 38) & (hsv[:,:,1] >= 40)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
clean = cv2.morphologyEx(gold_mask.astype(np.uint8)*255, cv2.MORPH_OPEN, kernel)
clean = cv2.morphologyEx(clean, cv2.MORPH_CLOSE, kernel)

cnts, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large = [c for c in cnts if cv2.contourArea(c) > 500]

print(f"Found {len(large)} large gold contours in IMG_0037:")
for i, c in enumerate(large):
    x, y, bw, bh = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    perim = cv2.arcLength(c, True)
    circ = 4 * np.pi * area / (perim * perim + 1e-6)
    print(f"  Contour {i}: Box:({x},{y},{bw}x{bh}), Area:{area}, Circ:{circ:.3f}")

# Also let's check what is in IMG_0062
p62 = 'scripts/thumbs/03_Necklace_IMG_0062__IMG_0062.JPG.jpeg.jpg'
img62 = cv2.imread(p62)
h62, w62 = img62.shape[:2]
hsv62 = cv2.cvtColor(img62, cv2.COLOR_BGR2HSV)
gold62 = (hsv62[:,:,0] >= 15) & (hsv62[:,:,0] <= 38) & (hsv62[:,:,1] >= 40)
clean62 = cv2.morphologyEx(gold62.astype(np.uint8)*255, cv2.MORPH_OPEN, kernel)
cnts62, _ = cv2.findContours(clean62, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large62 = [c for c in cnts62 if cv2.contourArea(c) > 500]
print(f"\nFound {len(large62)} large gold contours in IMG_0062:")
for i, c in enumerate(large62):
    x, y, bw, bh = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    perim = cv2.arcLength(c, True)
    circ = 4 * np.pi * area / (perim * perim + 1e-6)
    print(f"  Contour {i}: Box:({x},{y},{bw}x{bh}), Area:{area}, Circ:{circ:.3f}")
