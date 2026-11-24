import os
import cv2
import numpy as np
from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()

raw_base = os.path.join('assets', 'raw-jewellery', 'extracted')
os.makedirs('scripts/remediation_inspect', exist_ok=True)

# 1. Product 001: Inspect IMG_0428
p1_428 = os.path.join(raw_base, '01_Earrings_Set_1_0423', 'IMG_0428.JPG.jpeg')
im1 = cv2.imread(p1_428)
# Save preview
cv2.imwrite('scripts/remediation_inspect/p1_0428_preview.jpg', cv2.resize(im1, (800, int(800 * im1.shape[0]/im1.shape[1]))))

# 2. Product 002: Inspect IMG_0437 and IMG_0438
p2_437 = os.path.join(raw_base, '02_Earrings_Set_2_0437', 'IMG_0437.JPG.jpeg')
im2_437 = cv2.imread(p2_437)
cv2.imwrite('scripts/remediation_inspect/p2_0437_preview.jpg', cv2.resize(im2_437, (800, int(800 * im2_437.shape[0]/im2_437.shape[1]))))

p2_438 = os.path.join(raw_base, '02_Earrings_Set_2_0437', 'IMG_0438.JPG.jpeg')
im2_438 = cv2.imread(p2_438)
cv2.imwrite('scripts/remediation_inspect/p2_0438_preview.jpg', cv2.resize(im2_438, (800, int(800 * im2_438.shape[0]/im2_438.shape[1]))))

# 3. Product 007: Inspect Choker A (IMG_0037) and Choker B (IMG_0041, IMG_0043)
p7_37 = os.path.join(raw_base, '07_Fabric_Background_Reference', 'IMG_0037.HEIC')
with Image.open(p7_37) as im:
    im_t = ImageOps.exif_transpose(im).convert('RGB')
    cv2.imwrite('scripts/remediation_inspect/choker_A_0037.jpg', cv2.cvtColor(cv2.resize(np.array(im_t), (800, 1066)), cv2.COLOR_RGB2BGR))

p7_41 = os.path.join(raw_base, '07_Fabric_Background_Reference', 'IMG_0041.HEIC')
with Image.open(p7_41) as im:
    im_t = ImageOps.exif_transpose(im).convert('RGB')
    cv2.imwrite('scripts/remediation_inspect/choker_B_0041.jpg', cv2.cvtColor(cv2.resize(np.array(im_t), (800, 1066)), cv2.COLOR_RGB2BGR))

p7_43 = os.path.join(raw_base, '07_Fabric_Background_Reference', 'IMG_0043.HEIC')
with Image.open(p7_43) as im:
    im_t = ImageOps.exif_transpose(im).convert('RGB')
    cv2.imwrite('scripts/remediation_inspect/choker_B_0043.jpg', cv2.cvtColor(cv2.resize(np.array(im_t), (800, 1066)), cv2.COLOR_RGB2BGR))

print("Previews saved to scripts/remediation_inspect/")
