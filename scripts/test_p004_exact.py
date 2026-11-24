import cv2
import numpy as np

img4 = cv2.imread('assets/raw-jewellery/extracted/04_Long_Necklace_IMG_0143/IMG_0143.PNG')
h4, w4 = img4.shape[:2]

# Gold chains
hsv4 = cv2.cvtColor(img4, cv2.COLOR_BGR2HSV)
gold4 = (hsv4[:,:,0] >= 11) & (hsv4[:,:,0] <= 38) & (hsv4[:,:,1] >= 40)

# Medallion masks
med_mask = np.zeros((h4, w4), dtype=np.uint8)
# Left circle: center (240, 115), radius 90
cv2.circle(med_mask, (240, 115), 90, 255, -1)
# Right circle: center (770, 115), radius 90
cv2.circle(med_mask, (770, 115), 90, 255, -1)

tot4 = (gold4.astype(np.uint8)*255) | med_mask
tot4 = cv2.morphologyEx(tot4, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))

cnts4, _ = cv2.findContours(tot4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large4 = [c for c in cnts4 if cv2.contourArea(c) > 2000]

prev4 = img4.copy()
cv2.drawContours(prev4, large4, -1, (0, 255, 0), 2)
cv2.imwrite('scripts/remediation_test/p004_exact_preview.jpg', prev4)
print("Product 004 exact preview saved.")
