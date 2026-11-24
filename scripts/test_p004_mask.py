import os
import cv2
import numpy as np

raw_base = os.path.join('assets', 'raw-jewellery', 'extracted')
p4 = os.path.join(raw_base, '04_Long_Necklace_IMG_0143', 'IMG_0143.PNG')
img4 = cv2.imread(p4)
h4, w4 = img4.shape[:2]

# Gold chain detection
hsv4 = cv2.cvtColor(img4, cv2.COLOR_BGR2HSV)
gold4 = (hsv4[:,:,0] >= 12) & (hsv4[:,:,0] <= 38) & (hsv4[:,:,1] >= 40)

# Top medallions:
# The medallions are at y in [0, 400], x in [200, 450] (left) and x in [600, 850] (right)
# Let's detect the complete circular medallions
# Even though the rubies are pink/red, their luminance and contrast with the background is high (V > 100 or S in [120, 255])
# In LAB, the medallion area has very distinct gradient/edges compared to the smooth red background
gray4 = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)
edges4 = cv2.Canny(gray4, 30, 100)

# Detect circular / closed shapes of the medallions
medallion_left = np.zeros((h4, w4), dtype=np.uint8)
cv2.circle(medallion_left, (330, 220), 125, 255, -1)

medallion_right = np.zeros((h4, w4), dtype=np.uint8)
cv2.circle(medallion_right, (725, 220), 125, 255, -1)

# Combined mask: gold chains + complete medallion circles
# Let's refine the chain mask
k4 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
chain_clean = cv2.morphologyEx(gold4.astype(np.uint8)*255, cv2.MORPH_CLOSE, k4)

# Find medallion contour precisely within the circle ROI
roi_left = (medallion_left > 0)
roi_right = (medallion_right > 0)

# In roi_left, any non-dark-velvet pixel:
# Velvet background around the medallion has V < 120 and H in [170, 10]
# Medallion pink stones have bright specular facets and gold prongs
med_mask_l = np.zeros((h4, w4), dtype=np.uint8)
# Find circle
circles_l = cv2.HoughCircles(gray4[80:360, 200:460], cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=90, maxRadius=130)
if circles_l is not None:
    c = circles_l[0][0]
    cx_l, cy_l, r_l = int(c[0] + 200), int(c[1] + 80), int(c[2] + 4)
    cv2.circle(med_mask_l, (cx_l, cy_l), r_l, 255, -1)
    print(f"Detected left medallion circle at ({cx_l}, {cy_l}), r={r_l}")
else:
    cv2.circle(med_mask_l, (330, 220), 115, 255, -1)

circles_r = cv2.HoughCircles(gray4[80:360, 600:860], cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=90, maxRadius=130)
med_mask_r = np.zeros((h4, w4), dtype=np.uint8)
if circles_r is not None:
    c = circles_r[0][0]
    cx_r, cy_r, r_r = int(c[0] + 600), int(c[1] + 80), int(c[2] + 4)
    cv2.circle(med_mask_r, (cx_r, cy_r), r_r, 255, -1)
    print(f"Detected right medallion circle at ({cx_r}, {cy_r}), r={r_r}")
else:
    cv2.circle(med_mask_r, (725, 220), 115, 255, -1)

tot_mask4 = chain_clean | med_mask_l | med_mask_r
tot_mask4 = cv2.morphologyEx(tot_mask4, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))

preview4 = img4.copy()
cnts4, _ = cv2.findContours(tot_mask4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(preview4, cnts4, -1, (0, 255, 0), 2)
cv2.imwrite('scripts/remediation_test/p004_mask_preview.jpg', preview4)
cv2.imwrite('scripts/remediation_test/p004_mask.png', tot_mask4)

print("Product 004 mask generated.")
