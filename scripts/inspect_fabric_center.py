import os
import cv2
import numpy as np

p = 'scripts/thumbs/07_Fabric_Background_Reference__IMG_0037.HEIC.jpg'
img = cv2.imread(p)
h, w = img.shape[:2]

# Let's see what is in the center vs the edges
center = img[int(h*0.3):int(h*0.7), int(w*0.3):int(w*0.7)]
hsv = cv2.cvtColor(center, cv2.COLOR_BGR2HSV)

# Red velvet has H in [0, 15] or [165, 180], S in [80, 255]
# Let's count non-red pixels in center
non_red_mask = ~((hsv[:,:,0] < 15) | (hsv[:,:,0] > 165))
non_red_ratio = np.sum(non_red_mask) / (center.shape[0] * center.shape[1])
print(f"Non-red ratio in center of IMG_0037: {non_red_ratio*100:.2f}%")

# Let's see the colors of non-red pixels:
if np.sum(non_red_mask) > 0:
    non_red_bgr = center[non_red_mask]
    mean_nr_bgr = np.mean(non_red_bgr, axis=0)
    print(f"Mean BGR of non-red pixels: {mean_nr_bgr}")
    # Check if they are gold or white or what
    gold_mask = (hsv[:,:,0] >= 15) & (hsv[:,:,0] <= 35) & (hsv[:,:,1] >= 40)
    print(f"Gold pixels in center: {np.sum(gold_mask)/(center.shape[0]*center.shape[1])*100:.2f}%")

# What about the texture / folds?
gray = cv2.cvtColor(center, cv2.COLOR_BGR2GRAY)
lap = cv2.Laplacian(gray, cv2.CV_64F).var()
print(f"Center Laplacian: {lap:.1f}")
