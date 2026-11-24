import os
import cv2
import numpy as np

thumb_dir = os.path.join('scripts', 'thumbs')
check_dir = os.path.join('scripts', 'check_crops')
os.makedirs(check_dir, exist_ok=True)

files = [
    ('IMG_0235', '07_Fabric_Background_Reference__IMG_0235.HEIC.jpg'),
    ('IMG_0360', '07_Fabric_Background_Reference__IMG_0360.HEIC.jpg'),
    ('IMG_0231', '08_Dark_or_Unclear_Review__IMG_0231.HEIC.jpg'),
    ('IMG_0329', '08_Dark_or_Unclear_Review__IMG_0329.HEIC.jpg'),
    ('IMG_0444', '08_Dark_or_Unclear_Review__IMG_0444.HEIC.jpg'),
    ('IMG_0588', '08_Dark_or_Unclear_Review__IMG_0588.HEIC.jpg'),
    ('IMG_0828', '08_Dark_or_Unclear_Review__IMG_0828.HEIC.jpg'),
    ('IMG_0839', '09_Fastening_or_Extra_View__IMG_0839.JPG.jpeg.jpg'),
    ('IMG_0143', '04_Long_Necklace_IMG_0143__IMG_0143.PNG.jpg')
]

for label, fname in files:
    img = cv2.imread(os.path.join(thumb_dir, fname))
    h, w = img.shape[:2]
    # save full thumbnail to check_dir
    cv2.imwrite(os.path.join(check_dir, f"{label}_full.jpg"), img)
    # central crop
    c = img[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]
    cv2.imwrite(os.path.join(check_dir, f"{label}_center.jpg"), c)

print("Saved inspection crops to scripts/check_crops/")
