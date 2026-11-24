import os
import cv2
import numpy as np

p37 = 'scripts/thumbs/07_Fabric_Background_Reference__IMG_0037.HEIC.jpg'
p62 = 'scripts/thumbs/03_Necklace_IMG_0062__IMG_0062.JPG.jpeg.jpg'

img37 = cv2.imread(p37)
img62 = cv2.imread(p62)

# Save high-res crops of both to compare visually
cv2.imwrite('scripts/crop_necklace_0037.jpg', img37)
cv2.imwrite('scripts/crop_necklace_0062.jpg', img62)

# Check central pendant / motif
# In 0037, center is around (w//2, h//2 + 50)
h37, w37 = img37.shape[:2]
h62, w62 = img62.shape[:2]

pendant37 = img37[int(h37*0.5):int(h37*0.75), int(w37*0.35):int(w37*0.65)]
pendant62 = img62[int(h62*0.45):int(h62*0.75), int(w62*0.35):int(w62*0.65)]

cv2.imwrite('scripts/pendant_0037.jpg', pendant37)
cv2.imwrite('scripts/pendant_0062.jpg', pendant62)

# Check ORB feature match between pendant37 and pendant62
orb = cv2.ORB_create(nfeatures=500)
kp1, des1 = orb.detectAndCompute(pendant37, None)
kp2, des2 = orb.detectAndCompute(pendant62, None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
if des1 is not None and des2 is not None:
    matches = bf.match(des1, des2)
    good = [m for m in matches if m.distance < 45]
    print(f"Pendant 0037 vs Pendant 0062: {len(matches)} total, {len(good)} good matches")
else:
    print("Could not compute descriptors for pendants")
