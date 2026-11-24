import os
import cv2
import numpy as np

thumb_dir = os.path.join('scripts', 'thumbs')

# Let's inspect the pairwise feature matches between 06_Chain (0344, 0345, 0350) and 07_Fabric (0351..0355)
orb = cv2.ORB_create(nfeatures=1000)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

chain_files = [
    '06_Chain_or_Jewellery_on_Grey_0344__IMG_0344.HEIC.jpg',
    '06_Chain_or_Jewellery_on_Grey_0344__IMG_0345.HEIC.jpg',
    '06_Chain_or_Jewellery_on_Grey_0344__IMG_0350.HEIC.jpg',
    '07_Fabric_Background_Reference__IMG_0351.HEIC.jpg',
    '07_Fabric_Background_Reference__IMG_0352.HEIC.jpg',
    '07_Fabric_Background_Reference__IMG_0353.HEIC.jpg',
    '07_Fabric_Background_Reference__IMG_0354.HEIC.jpg',
    '07_Fabric_Background_Reference__IMG_0355.HEIC.jpg'
]

print("=== Comparing 0344-0355 sequence ===")
for i in range(len(chain_files)):
    f1 = chain_files[i]
    img1 = cv2.imread(os.path.join(thumb_dir, f1), cv2.IMREAD_GRAYSCALE)
    kp1, des1 = orb.detectAndCompute(img1, None)
    for j in range(i+1, len(chain_files)):
        f2 = chain_files[j]
        img2 = cv2.imread(os.path.join(thumb_dir, f2), cv2.IMREAD_GRAYSCALE)
        kp2, des2 = orb.detectAndCompute(img2, None)
        if des1 is not None and des2 is not None:
            matches = bf.match(des1, des2)
            good = [m for m in matches if m.distance < 40]
            if len(good) > 10:
                print(f"  {f1.split('__')[1][:15]} <--> {f2.split('__')[1][:15]}: {len(good)} matches")

# Compare 0231 and 0235
p231 = os.path.join(thumb_dir, '08_Dark_or_Unclear_Review__IMG_0231.HEIC.jpg')
p235 = os.path.join(thumb_dir, '07_Fabric_Background_Reference__IMG_0235.HEIC.jpg')
img231 = cv2.imread(p231, cv2.IMREAD_GRAYSCALE)
img235 = cv2.imread(p235, cv2.IMREAD_GRAYSCALE)
kp1, des1 = orb.detectAndCompute(img231, None)
kp2, des2 = orb.detectAndCompute(img235, None)
if des1 is not None and des2 is not None:
    matches = bf.match(des1, des2)
    good = [m for m in matches if m.distance < 40]
    print(f"\n0231 vs 0235 matches: {len(good)}")

# Compare 0828 and 0839
p828 = os.path.join(thumb_dir, '08_Dark_or_Unclear_Review__IMG_0828.HEIC.jpg')
p839 = os.path.join(thumb_dir, '09_Fastening_or_Extra_View__IMG_0839.JPG.jpeg.jpg')
img828 = cv2.imread(p828, cv2.IMREAD_GRAYSCALE)
img839 = cv2.imread(p839, cv2.IMREAD_GRAYSCALE)
kp1, des1 = orb.detectAndCompute(img828, None)
kp2, des2 = orb.detectAndCompute(img839, None)
if des1 is not None and des2 is not None:
    matches = bf.match(des1, des2)
    good = [m for m in matches if m.distance < 40]
    print(f"0828 vs 0839 matches: {len(good)}")
