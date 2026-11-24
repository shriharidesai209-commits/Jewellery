import os
import cv2
import numpy as np
from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()

raw_base = os.path.join('assets', 'raw-jewellery', 'extracted')
os.makedirs('scripts/remediation_test', exist_ok=True)

# 1. Product 001: IMG_0428 (Complete Jhumkas)
im1 = cv2.imread(os.path.join(raw_base, '01_Earrings_Set_1_0423', 'IMG_0428.JPG.jpeg'))
h1, w1 = im1.shape[:2]
# Earrings are in middle of the frame
# Gold + rubies
hsv1 = cv2.cvtColor(im1, cv2.COLOR_BGR2HSV)
gold1 = (hsv1[:,:,0] >= 12) & (hsv1[:,:,0] <= 38) & (hsv1[:,:,1] >= 45) & (hsv1[:,:,2] >= 60)
ruby1 = ((hsv1[:,:,0] <= 10) | (hsv1[:,:,0] >= 170)) & (hsv1[:,:,1] >= 100) & (hsv1[:,:,2] >= 50)
# Skin exclusion: skin is at top fingers (y < 1600)
ycrcb1 = cv2.cvtColor(im1, cv2.COLOR_BGR2YCrCb)
skin1 = (cv2.inRange(ycrcb1, np.array([0, 133, 77]), np.array([255, 173, 127])) > 0) & \
        (cv2.inRange(hsv1, np.array([0, 25, 50]), np.array([25, 160, 255])) > 0)

earring_pix = (gold1 | ruby1) & (~skin1)
k1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
earring_clean = cv2.morphologyEx(earring_pix.astype(np.uint8)*255, cv2.MORPH_CLOSE, k1)

# Find contours in the earring region: x in [400, 1800], y in [1200, 2800]
roi_mask = np.zeros((h1, w1), dtype=np.uint8)
roi_mask[1200:2800, 400:1800] = 255
earring_clean = earring_clean & roi_mask

cnts1, _ = cv2.findContours(earring_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large_cnts1 = [c for c in cnts1 if cv2.contourArea(c) > 5000]

mask1 = np.zeros((h1, w1), dtype=np.uint8)
cv2.drawContours(mask1, large_cnts1, -1, 255, -1)
# Slight dilation to cover bead edges
mask1 = cv2.dilate(mask1, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

prev1 = im1.copy()
cv2.drawContours(prev1, large_cnts1, -1, (0, 255, 0), 4)
cv2.imwrite('scripts/remediation_test/p001_mask_preview.jpg', cv2.resize(prev1, (800, int(800*h1/w1))))
cv2.imwrite('scripts/remediation_test/p001_mask.png', mask1)
print(f"Product 001 mask: {len(large_cnts1)} contours found")

# 2. Product 007: Choker A (IMG_0037)
with Image.open(os.path.join(raw_base, '07_Fabric_Background_Reference', 'IMG_0037.HEIC')) as im:
    im7_a = cv2.cvtColor(np.array(ImageOps.exif_transpose(im).convert('RGB')), cv2.COLOR_RGB2BGR)

h7a, w7a = im7_a.shape[:2]
hsv7a = cv2.cvtColor(im7_a, cv2.COLOR_BGR2HSV)
# Gold + rhodium center
# Background velvet is deep red: H in [170, 10], S > 60
# Non-background is gold (H 15-38), rhodium (high brightness, low S: V > 140, S < 60)
gold7a = (hsv7a[:,:,0] >= 12) & (hsv7a[:,:,0] <= 38) & (hsv7a[:,:,1] >= 40)
rhodium7a = (hsv7a[:,:,2] >= 130) & (hsv7a[:,:,1] <= 70)
jewel7a = (gold7a | rhodium7a).astype(np.uint8)*255

k7a = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
jewel7a_closed = cv2.morphologyEx(jewel7a, cv2.MORPH_CLOSE, k7a)

cnts7a, _ = cv2.findContours(jewel7a_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large_cnts7a = [c for c in cnts7a if cv2.contourArea(c) > (w7a * h7a * 0.05)]

mask7a = np.zeros((h7a, w7a), dtype=np.uint8)
cv2.drawContours(mask7a, large_cnts7a, -1, 255, -1)
# Fill interior
mask7a = cv2.morphologyEx(mask7a, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))

prev7a = im7_a.copy()
cv2.drawContours(prev7a, large_cnts7a, -1, (0, 255, 0), 4)
cv2.imwrite('scripts/remediation_test/chokerA_mask_preview.jpg', cv2.resize(prev7a, (800, int(800*h7a/w7a))))
cv2.imwrite('scripts/remediation_test/chokerA_mask.png', mask7a)
print(f"Choker A mask: {len(large_cnts7a)} contours found")

# 3. Product 007: Choker B (IMG_0041)
with Image.open(os.path.join(raw_base, '07_Fabric_Background_Reference', 'IMG_0041.HEIC')) as im:
    im7_b = cv2.cvtColor(np.array(ImageOps.exif_transpose(im).convert('RGB')), cv2.COLOR_RGB2BGR)

h7b, w7b = im7_b.shape[:2]
hsv7b = cv2.cvtColor(im7_b, cv2.COLOR_BGR2HSV)
gold7b = (hsv7b[:,:,0] >= 12) & (hsv7b[:,:,0] <= 38) & (hsv7b[:,:,1] >= 40)
rhodium7b = (hsv7b[:,:,2] >= 130) & (hsv7b[:,:,1] <= 70)
jewel7b = (gold7b | rhodium7b).astype(np.uint8)*255

k7b = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
jewel7b_closed = cv2.morphologyEx(jewel7b, cv2.MORPH_CLOSE, k7b)

cnts7b, _ = cv2.findContours(jewel7b_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large_cnts7b = [c for c in cnts7b if cv2.contourArea(c) > (w7b * h7b * 0.05)]

mask7b = np.zeros((h7b, w7b), dtype=np.uint8)
cv2.drawContours(mask7b, large_cnts7b, -1, 255, -1)
# Fill interior to protect rubies!
mask7b = cv2.morphologyEx(mask7b, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))

prev7b = im7_b.copy()
cv2.drawContours(prev7b, large_cnts7b, -1, (0, 255, 0), 4)
cv2.imwrite('scripts/remediation_test/chokerB_mask_preview.jpg', cv2.resize(prev7b, (800, int(800*h7b/w7b))))
cv2.imwrite('scripts/remediation_test/chokerB_mask.png', mask7b)
print(f"Choker B mask: {len(large_cnts7b)} contours found")
