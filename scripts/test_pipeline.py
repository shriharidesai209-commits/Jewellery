import os
import cv2
import numpy as np
from PIL import Image

# Test segmentation and background replacement on IMG_0423 (Earrings Set 1)
raw_path = os.path.join('assets', 'raw-jewellery', 'extracted', '01_Earrings_Set_1_0423', 'IMG_0423.JPG.jpeg')
img = cv2.imread(raw_path)
h, w = img.shape[:2]

# Downscale slightly for test if huge, but let's test full or half res
scale = 0.5
small = cv2.resize(img, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)
sh, sw = small.shape[:2]

# Red velvet background segmentation
# Convert to HSV and LAB
hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
lab = cv2.cvtColor(small, cv2.COLOR_BGR2LAB)

# Red in HSV: H < 12 or H > 168, S > 50, V > 40
m1 = cv2.inRange(hsv, np.array([0, 45, 30]), np.array([12, 255, 255]))
m2 = cv2.inRange(hsv, np.array([168, 45, 30]), np.array([180, 255, 255]))
red_bg = m1 | m2

# Also in LAB, red velvet has high A channel (A > 145)
lab_red = lab[:, :, 1] > 140
red_bg = red_bg | lab_red

# Exclude bottom skin/fingers if present
ycrcb = cv2.cvtColor(small, cv2.COLOR_BGR2YCrCb)
skin = (cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127])) > 0) & \
       (cv2.inRange(hsv, np.array([0, 30, 80]), np.array([25, 170, 255])) > 0)

# Object is NOT red and NOT skin (for pure jewellery extraction)
# In IMG_0423, fingers are at the bottom hook / base
jewel_fg = (~red_bg) & (~skin)

# Morphological cleanup
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
jewel_fg = cv2.morphologyEx(jewel_fg.astype(np.uint8)*255, cv2.MORPH_OPEN, kernel)

# Find main earring contour
cnts, _ = cv2.findContours(jewel_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large_cnts = [c for c in cnts if cv2.contourArea(c) > (sw*sh*0.01)]

mask = np.zeros((sh, sw), dtype=np.uint8)
cv2.drawContours(mask, large_cnts, -1, 255, -1)
# Slight feathering on edge
mask_blur = cv2.GaussianBlur(mask, (5, 5), 1.5)
alpha = (mask_blur.astype(np.float32) / 255.0)[:, :, np.newaxis]

# Create warm ivory luxury studio background (e.g. #F8F6F0 = RGB 248, 246, 240 -> BGR 240, 246, 248)
bg = np.ones((sh, sw, 3), dtype=np.float32)
# Subtle soft radial vignette
y_coords, x_coords = np.ogrid[:sh, :sw]
center_dist = np.sqrt(((x_coords - sw/2)/(sw/2))**2 + ((y_coords - sh/2)/(sh/2))**2)
vignette = 1.0 - 0.04 * np.clip(center_dist, 0, 1.5)
bg[:, :, 0] = 238 * vignette
bg[:, :, 1] = 244 * vignette
bg[:, :, 2] = 247 * vignette

# Generate soft drop shadow from mask
shadow_mask = cv2.GaussianBlur(mask, (31, 31), 10)
# Shift shadow slightly down and right
M = np.float32([[1, 0, 8], [0, 1, 14]])
shifted_shadow = cv2.warpAffine(shadow_mask, M, (sw, sh))
shadow_alpha = (shifted_shadow.astype(np.float32) / 255.0) * 0.28
shadow_alpha = shadow_alpha[:, :, np.newaxis]

# Apply shadow to background
bg = bg * (1.0 - shadow_alpha)

# Composite jewellery
comp = small.astype(np.float32) * alpha + bg * (1.0 - alpha)
comp = np.clip(comp, 0, 255).astype(np.uint8)

os.makedirs('scripts/test_out', exist_ok=True)
cv2.imwrite('scripts/test_out/test_comp_0423.jpg', comp)
print("Test composite saved to scripts/test_out/test_comp_0423.jpg")
