import os
import cv2
import numpy as np
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

raw_base = os.path.join('assets', 'raw-jewellery', 'extracted')
os.makedirs('scripts/remediation_test', exist_ok=True)

print("--- TESTING HIGH-PRECISION SEGMENTATION ---")

# 1. Product 003: IMG_0062 (Ruby Choker)
# The necklace has:
# - Yellow gold filigree band with ruby cabochons
# - Seed pearls dangling along the bottom
# - Dori string at the top
# - Velvet background is deep red
# Strategy: In HSV/LAB, the velvet is saturated red (H in [170,180] or [0,10], S in [80,255]).
# But rubies also have red hue!
# However:
# 1) The gold bezels and gold band have distinct yellow-gold hue (H in [15,35]) and high brightness.
# 2) The pearls have high brightness (V > 180, S < 60).
# 3) The rubies are completely INSIDE the gold bezels!
# 4) The background is outside the outer perimeter of the necklace!
# If we identify the continuous necklace structure (gold + pearls) and compute its closed convex hull or morphological close of the gold/pearl lattice, the rubies are enclosed!
p3 = os.path.join(raw_base, '03_Necklace_IMG_0062', 'IMG_0062.JPG.jpeg')
img3 = cv2.imread(p3)
h3, w3 = img3.shape[:2]

# Gold mask
hsv3 = cv2.cvtColor(img3, cv2.COLOR_BGR2HSV)
gold_mask = (hsv3[:,:,0] >= 14) & (hsv3[:,:,0] <= 38) & (hsv3[:,:,1] >= 40)
# Pearl / highlight mask
pearl_mask = (hsv3[:,:,2] >= 160) & (hsv3[:,:,1] <= 80)
# Combined gold + pearl
structure_mask = (gold_mask | pearl_mask).astype(np.uint8) * 255

# Fill enclosed holes: any ruby enclosed by the gold bezels will be filled!
# Morphological close along the necklace contour
k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
closed = cv2.morphologyEx(structure_mask, cv2.MORPH_CLOSE, k_close)

# Find necklace contours
cnts3, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Filter by area
main_cnts = [c for c in cnts3 if cv2.contourArea(c) > (w3 * h3 * 0.05)]

filled_mask = np.zeros((h3, w3), dtype=np.uint8)
cv2.drawContours(filled_mask, main_cnts, -1, 255, -1)

# Now in filled_mask, check if rubies are included:
# Rubies are darker red than the velvet and have sharp gradient borders with gold
# Let's save the mask and mask preview
preview3 = img3.copy()
# Draw contour in green
cv2.drawContours(preview3, main_cnts, -1, (0, 255, 0), 2)
cv2.imwrite('scripts/remediation_test/p003_mask_preview.jpg', preview3)
cv2.imwrite('scripts/remediation_test/p003_mask.png', filled_mask)

print("Product 003 mask generated. Main contours found:", len(main_cnts))

# Check ruby pixels inside mask
# In raw img3, within filled_mask:
rubies_inside = np.sum((hsv3[:,:,0] < 15) & (filled_mask > 0))
print(f"Red/ruby pixels preserved inside filled mask: {rubies_inside}")
