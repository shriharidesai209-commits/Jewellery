import os
import cv2
import numpy as np

thumb_dir = os.path.join('scripts', 'thumbs')

# Let's inspect features for each folder in detail
def describe_img(p):
    img = cv2.imread(p)
    h, w = img.shape[:2]
    # Center crop
    crop = img[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]
    # Color means
    b, g, r = [cv2.mean(crop)[i] for i in range(3)]
    # Edge count
    edges = cv2.Canny(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY), 50, 150)
    edge_density = np.sum(edges > 0) / (crop.shape[0] * crop.shape[1])
    return f"Size:{w}x{h}, BGR:({b:.0f},{g:.0f},{r:.0f}), Edges:{edge_density:.3f}"

# Let's check ORB feature matching between suspect pairs
orb = cv2.ORB_create(nfeatures=500)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

def match_score(p1, p2):
    img1 = cv2.imread(p1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(p2, cv2.IMREAD_GRAYSCALE)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    if des1 is None or des2 is None or len(des1) < 10 or len(des2) < 10:
        return 0, 0
    matches = bf.match(des1, des2)
    good = [m for m in matches if m.distance < 45]
    return len(matches), len(good)

# Check pairs of interest
checks = [
    # Compare 01_Earrings_Set_1 photos
    ("01_Earrings_Set_1_0423__IMG_0423.JPG.jpeg.jpg", "01_Earrings_Set_1_0423__IMG_0428.JPG.jpeg.jpg"),
    ("01_Earrings_Set_1_0423__IMG_0428.JPG.jpeg.jpg", "01_Earrings_Set_1_0423__IMG_0429.JPG.jpeg.jpg"),
    ("01_Earrings_Set_1_0423__IMG_0428.JPG.jpeg.jpg", "01_Earrings_Set_1_0423__IMG_0431.JPG.jpeg.jpg"),
    
    # Compare 02_Earrings_Set_2 photos
    ("02_Earrings_Set_2_0437__IMG_0437.JPG.jpeg.jpg", "02_Earrings_Set_2_0437__IMG_0438.JPG.jpeg.jpg"),
    ("02_Earrings_Set_2_0437__IMG_0437.JPG.jpeg.jpg", "02_Earrings_Set_2_0437__IMG_0439.JPG.jpeg.jpg"),
    ("02_Earrings_Set_2_0437__IMG_0437.JPG.jpeg.jpg", "02_Earrings_Set_2_0437__IMG_0440.JPG.jpeg.jpg"),
    ("02_Earrings_Set_2_0437__IMG_0437.JPG.jpeg.jpg", "02_Earrings_Set_2_0437__IMG_0441.JPG.jpeg.jpg"),
    ("02_Earrings_Set_2_0437__IMG_0437.JPG.jpeg.jpg", "02_Earrings_Set_2_0437__IMG_0442.JPG.jpeg.jpg"),
    ("02_Earrings_Set_2_0437__IMG_0437.JPG.jpeg.jpg", "08_Dark_or_Unclear_Review__IMG_0444.HEIC.jpg"),
    
    # Compare 03_Necklace vs 07_Fabric (0034-0044)
    ("03_Necklace_IMG_0062__IMG_0062.JPG.jpeg.jpg", "07_Fabric_Background_Reference__IMG_0034.HEIC.jpg"),
    ("03_Necklace_IMG_0062__IMG_0062.JPG.jpeg.jpg", "07_Fabric_Background_Reference__IMG_0042.HEIC.jpg"),
    ("07_Fabric_Background_Reference__IMG_0034.HEIC.jpg", "07_Fabric_Background_Reference__IMG_0035.HEIC.jpg"),
    ("07_Fabric_Background_Reference__IMG_0035.HEIC.jpg", "07_Fabric_Background_Reference__IMG_0037.HEIC.jpg"),
    
    # Compare 05_Ornate_Jewellery_Closeups vs 08_Dark_or_Unclear (0299)
    ("05_Ornate_Jewellery_Closeups_0300__IMG_0300.HEIC.jpg", "05_Ornate_Jewellery_Closeups_0300__IMG_0301.HEIC.jpg"),
    ("05_Ornate_Jewellery_Closeups_0300__IMG_0300.HEIC.jpg", "08_Dark_or_Unclear_Review__IMG_0299.HEIC.jpg"),
    
    # Compare 06_Chain vs 07_Fabric (0351-0355)
    ("06_Chain_or_Jewellery_on_Grey_0344__IMG_0344.HEIC.jpg", "06_Chain_or_Jewellery_on_Grey_0344__IMG_0345.HEIC.jpg"),
    ("06_Chain_or_Jewellery_on_Grey_0344__IMG_0344.HEIC.jpg", "06_Chain_or_Jewellery_on_Grey_0344__IMG_0350.HEIC.jpg"),
    ("06_Chain_or_Jewellery_on_Grey_0344__IMG_0344.HEIC.jpg", "07_Fabric_Background_Reference__IMG_0351.HEIC.jpg"),
    ("07_Fabric_Background_Reference__IMG_0351.HEIC.jpg", "07_Fabric_Background_Reference__IMG_0352.HEIC.jpg"),
    ("07_Fabric_Background_Reference__IMG_0351.HEIC.jpg", "07_Fabric_Background_Reference__IMG_0355.HEIC.jpg"),
    
    # Compare 08_Dark IMG_0231 vs 07_Fabric IMG_0235
    ("08_Dark_or_Unclear_Review__IMG_0231.HEIC.jpg", "07_Fabric_Background_Reference__IMG_0235.HEIC.jpg"),
    
    # Compare 08_Dark IMG_0828 vs 09_Fastening IMG_0839
    ("08_Dark_or_Unclear_Review__IMG_0828.HEIC.jpg", "09_Fastening_or_Extra_View__IMG_0839.JPG.jpeg.jpg")
]

print("=== FEATURE MATCH RESULTS ===")
for f1, f2 in checks:
    p1 = os.path.join(thumb_dir, f1)
    p2 = os.path.join(thumb_dir, f2)
    if os.path.exists(p1) and os.path.exists(p2):
        tot, good = match_score(p1, p2)
        n1 = f1.replace('__', '/').replace('.jpg', '')
        n2 = f2.replace('__', '/').replace('.jpg', '')
        print(f"{n1:45} <--> {n2:45} | Matches: {tot:3d}, Good: {good:3d}")
    else:
        print(f"Missing: {f1} or {f2}")
