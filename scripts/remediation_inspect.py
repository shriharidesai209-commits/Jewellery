import os
import cv2
import numpy as np
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

raw_base = os.path.join('assets', 'raw-jewellery', 'extracted')

print("=== INSPECTING RAW FILES FOR REMEDIATION ===")

# 1. Product 001: IMG_0428 vs IMG_0429
for fn in ['01_Earrings_Set_1_0423/IMG_0423.JPG.jpeg', '01_Earrings_Set_1_0423/IMG_0428.JPG.jpeg', '01_Earrings_Set_1_0423/IMG_0429.JPG.jpeg', '01_Earrings_Set_1_0423/IMG_0431.JPG.jpeg']:
    p = os.path.join(raw_base, fn)
    img = cv2.imread(p)
    print(f"P1: {os.path.basename(fn)}: {img.shape}")

# 2. Product 002: IMG_0437 to IMG_0442
for fn in sorted(os.listdir(os.path.join(raw_base, '02_Earrings_Set_2_0437'))):
    if fn.endswith('.jpeg'):
        p = os.path.join(raw_base, '02_Earrings_Set_2_0437', fn)
        img = cv2.imread(p)
        print(f"P2: {fn}: {img.shape}")

# 3. Product 003: IMG_0062
p3 = os.path.join(raw_base, '03_Necklace_IMG_0062', 'IMG_0062.JPG.jpeg')
img3 = cv2.imread(p3)
print(f"P3: IMG_0062: {img3.shape}")

# 4. Product 004: IMG_0143
p4 = os.path.join(raw_base, '04_Long_Necklace_IMG_0143', 'IMG_0143.PNG')
img4 = cv2.imread(p4)
print(f"P4: IMG_0143: {img4.shape}")

# 5. Product 005: IMG_0299
p5 = os.path.join(raw_base, '08_Dark_or_Unclear_Review', 'IMG_0299.HEIC')
with Image.open(p5) as im:
    print(f"P5: IMG_0299: size={im.size}, mode={im.mode}")

# 6. Product 006: IMG_0344, 0345, 0350, 0351..0355
print("P6 Files:")
for fn in ['06_Chain_or_Jewellery_on_Grey_0344/IMG_0344.HEIC', '06_Chain_or_Jewellery_on_Grey_0344/IMG_0345.HEIC', '06_Chain_or_Jewellery_on_Grey_0344/IMG_0350.HEIC']:
    p = os.path.join(raw_base, fn)
    with Image.open(p) as im:
        print(f"  {os.path.basename(fn)}: {im.size}")
for i in range(351, 356):
    p = os.path.join(raw_base, '07_Fabric_Background_Reference', f'IMG_0{i}.HEIC')
    with Image.open(p) as im:
        print(f"  IMG_0{i}.HEIC: {im.size}")

# 7. Product 007: Check if IMG_0036 exists
print("P7 Files:")
for i in range(34, 45):
    p = os.path.join(raw_base, '07_Fabric_Background_Reference', f'IMG_00{i}.HEIC')
    exists = os.path.exists(p)
    print(f"  IMG_00{i}.HEIC: exists={exists}")
