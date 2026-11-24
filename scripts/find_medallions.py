import cv2
import numpy as np

img = cv2.imread('assets/raw-jewellery/extracted/04_Long_Necklace_IMG_0143/IMG_0143.PNG')
h, w = img.shape[:2]

# Crop top-left and top-right
left_box = img[10:200, 150:350]
right_box = img[20:210, 680:880]

# Find circle center by center of mass of the bright/gold+ruby cluster
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Medallions are much brighter than velvet
_, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)

cnts, _ = cv2.findContours(thresh[:250, :], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in cnts:
    area = cv2.contourArea(c)
    if area > 8000:
        (x, y), r = cv2.minEnclosingCircle(c)
        print(f"Top medallion: center=({x:.1f}, {y:.1f}), radius={r:.1f}, area={area}")
