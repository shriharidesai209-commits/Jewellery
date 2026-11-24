import os
import cv2
import numpy as np

thumb_dir = os.path.join('scripts', 'thumbs')

files = [
    '08_Dark_or_Unclear_Review__IMG_0444.HEIC.jpg',
    '08_Dark_or_Unclear_Review__IMG_0231.HEIC.jpg',
    '08_Dark_or_Unclear_Review__IMG_0329.HEIC.jpg',
    '08_Dark_or_Unclear_Review__IMG_0588.HEIC.jpg',
    '08_Dark_or_Unclear_Review__IMG_0828.HEIC.jpg',
    '09_Fastening_or_Extra_View__IMG_0839.JPG.jpeg.jpg',
    '08_Dark_or_Unclear_Review__IMG_0299.HEIC.jpg',
    '07_Fabric_Background_Reference__IMG_0235.HEIC.jpg',
    '07_Fabric_Background_Reference__IMG_0360.HEIC.jpg',
    '04_Long_Necklace_IMG_0143__IMG_0143.PNG.jpg',
    '03_Necklace_IMG_0062__IMG_0062.JPG.jpeg.jpg'
]

for f in files:
    p = os.path.join(thumb_dir, f)
    img = cv2.imread(p)
    h, w = img.shape[:2]
    # Check what colors are in the central 60%
    c = img[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]
    bgr = [round(float(v), 1) for v in cv2.mean(c)[:3]]
    hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    gold = np.sum(cv2.inRange(hsv, np.array([15, 40, 70]), np.array([35, 255, 255])) > 0) / (c.shape[0]*c.shape[1]) * 100
    white = np.sum(cv2.inRange(hsv, np.array([0, 0, 180]), np.array([180, 50, 255])) > 0) / (c.shape[0]*c.shape[1]) * 100
    gray = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F).var()
    print(f"{f:50} | CenterBGR:{bgr} | Gold:{gold:4.1f}% | White:{white:4.1f}% | Sharpness:{lap:6.1f}")
