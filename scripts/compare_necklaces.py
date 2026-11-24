import os
import cv2
import numpy as np
from PIL import Image

thumb_dir = os.path.join('scripts', 'thumbs')

# Compare 03_Necklace IMG_0062 with 07_Fabric IMG_0034-0044
p0062 = os.path.join(thumb_dir, '03_Necklace_IMG_0062__IMG_0062.JPG.jpeg.jpg')
img0062 = cv2.imread(p0062)

print("Comparing IMG_0062 with IMG_0034-0044:")
fabric_files = [f for f in sorted(os.listdir(thumb_dir)) if '07_Fabric' in f and any(x in f for x in ['0034', '0035', '0037', '0038', '0039', '0040', '0041', '0042', '0043', '0044'])]

for ff in fabric_files:
    p = os.path.join(thumb_dir, ff)
    img = cv2.imread(p)
    fn = ff.split('__')[1].replace('.jpg', '')
    
    # Feature comparison between img0062 and img
    # Crop central region
    h, w = img.shape[:2]
    c1 = img0062[int(img0062.shape[0]*0.25):int(img0062.shape[0]*0.75), int(img0062.shape[1]*0.15):int(img0062.shape[1]*0.85)]
    c2 = img[int(h*0.25):int(h*0.75), int(w*0.15):int(w*0.85)]
    
    # Resize c2 to c1 for comparison
    c2_res = cv2.resize(c2, (c1.shape[1], c1.shape[0]))
    diff = cv2.absdiff(c1, c2_res)
    mean_diff = np.mean(diff)
    
    # Compare histograms
    h1 = cv2.calcHist([c1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    h2 = cv2.calcHist([c2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(h1, h1)
    cv2.normalize(h2, h2)
    corr = cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)
    
    print(f"  IMG_0062 vs {fn}: MeanDiff={mean_diff:.1f}, HistCorr={corr:.3f}")

# Compare IMG_0034 to IMG_0044 amongst themselves
print("\nComparing IMG_0034 to IMG_0044 amongst themselves:")
p0037 = os.path.join(thumb_dir, '07_Fabric_Background_Reference__IMG_0037.HEIC.jpg')
img0037 = cv2.imread(p0037)
for ff in fabric_files:
    p = os.path.join(thumb_dir, ff)
    img = cv2.imread(p)
    fn = ff.split('__')[1].replace('.jpg', '')
    h, w = img.shape[:2]
    c1 = img0037[int(img0037.shape[0]*0.25):int(img0037.shape[0]*0.75), int(img0037.shape[1]*0.15):int(img0037.shape[1]*0.85)]
    c2 = img[int(h*0.25):int(h*0.75), int(w*0.15):int(w*0.85)]
    c2_res = cv2.resize(c2, (c1.shape[1], c1.shape[0]))
    diff = cv2.absdiff(c1, c2_res)
    mean_diff = np.mean(diff)
    print(f"  IMG_0037 vs {fn}: MeanDiff={mean_diff:.1f}")
