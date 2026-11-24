import os
import cv2
import numpy as np

# Let's inspect what is in IMG_0034.HEIC vs IMG_0062 vs IMG_0143
thumb_dir = os.path.join('scripts', 'thumbs')

def describe_file_content(thumb_fname):
    p = os.path.join(thumb_dir, thumb_fname)
    img = cv2.imread(p)
    h, w = img.shape[:2]
    # Check central 50%
    c = img[int(h*0.25):int(h*0.75), int(w*0.25):int(w*0.75)]
    # BGR stats
    b, g, r = [float(cv2.mean(c)[i]) for i in range(3)]
    # HSV
    hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    # Brightness range
    min_v, max_v = np.min(hsv[:,:,2]), np.max(hsv[:,:,2])
    # Distinct non-red pixels
    m1 = cv2.inRange(hsv, np.array([0, 50, 40]), np.array([10, 255, 255]))
    m2 = cv2.inRange(hsv, np.array([170, 50, 40]), np.array([180, 255, 255]))
    non_red = np.sum((~(m1 | m2)) > 0) / (c.shape[0]*c.shape[1]) * 100
    return f"BGR:({b:.1f},{g:.1f},{r:.1f}), V_range:[{min_v},{max_v}], NonRed:{non_red:.1f}%"

print("IMG_0034:", describe_file_content("07_Fabric_Background_Reference__IMG_0034.HEIC.jpg"))
print("IMG_0035:", describe_file_content("07_Fabric_Background_Reference__IMG_0035.HEIC.jpg"))
print("IMG_0037:", describe_file_content("07_Fabric_Background_Reference__IMG_0037.HEIC.jpg"))
print("IMG_0062:", describe_file_content("03_Necklace_IMG_0062__IMG_0062.JPG.jpeg.jpg"))
print("IMG_0143:", describe_file_content("04_Long_Necklace_IMG_0143__IMG_0143.PNG.jpg"))
print("IMG_0235:", describe_file_content("07_Fabric_Background_Reference__IMG_0235.HEIC.jpg"))
print("IMG_0360:", describe_file_content("07_Fabric_Background_Reference__IMG_0360.HEIC.jpg"))
print("IMG_0231:", describe_file_content("08_Dark_or_Unclear_Review__IMG_0231.HEIC.jpg"))
print("IMG_0588:", describe_file_content("08_Dark_or_Unclear_Review__IMG_0588.HEIC.jpg"))
print("IMG_0828:", describe_file_content("08_Dark_or_Unclear_Review__IMG_0828.HEIC.jpg"))
print("IMG_0839:", describe_file_content("09_Fastening_or_Extra_View__IMG_0839.JPG.jpeg.jpg"))
