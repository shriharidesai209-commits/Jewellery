import os
import cv2
import numpy as np

thumb_dir = os.path.join('scripts', 'thumbs')

# Let's inspect each image's visual structure
# Specifically:
# 1. 02_Earrings_Set_2
# 2. 03_Necklace & 07_Fabric
# 3. 04_Long_Necklace
# 4. 05_Ornate & 08_IMG_0299
# 5. 06_Chain & 07_0351..0355
# 6. Remaining 08_Dark & 09_Fastening

def print_image_stats(fname):
    p = os.path.join(thumb_dir, fname)
    img = cv2.imread(p)
    h, w = img.shape[:2]
    # Center 50%
    c = img[int(h*0.25):int(h*0.75), int(w*0.25):int(w*0.75)]
    # Average color
    b, g, r = [float(cv2.mean(c)[i]) for i in range(3)]
    # Min/max brightness
    gray = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
    min_v, max_v = int(np.min(gray)), int(np.max(gray))
    # Detect prominent edges / lines
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40, minLineLength=30, maxLineGap=10)
    n_lines = len(lines) if lines is not None else 0
    return f"Res:{w}x{h}, BGR:({b:.1f},{g:.1f},{r:.1f}), GrayRange:[{min_v},{max_v}], Lines:{n_lines}"

for f in sorted(os.listdir(thumb_dir)):
    if not f.endswith('.jpg'):
        continue
    stats = print_image_stats(f)
    print(f"{f.replace('.jpg', ''):55} | {stats}")
