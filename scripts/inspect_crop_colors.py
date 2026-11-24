import os
import cv2
import numpy as np

check_dir = os.path.join('scripts', 'check_crops')

def analyze_crop(name):
    p = os.path.join(check_dir, f"{name}_center.jpg")
    img = cv2.imread(p)
    if img is None:
        return "None"
    h, w = img.shape[:2]
    # Dominant colors
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Check gold
    gold = np.sum((hsv[:,:,0]>=15)&(hsv[:,:,0]<=35)&(hsv[:,:,1]>=50)) / (w*h) * 100
    # Check white/silver/diamonds
    white = np.sum((hsv[:,:,1]<=40)&(hsv[:,:,2]>=180)) / (w*h) * 100
    # Check red
    red = np.sum(((hsv[:,:,0]<15)|(hsv[:,:,0]>165))&(hsv[:,:,1]>=50)) / (w*h) * 100
    # Check skin
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    skin = (cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127])) > 0) & \
           (cv2.inRange(hsv, np.array([0, 30, 80]), np.array([25, 170, 255])) > 0)
    skin_pct = np.sum(skin) / (w*h) * 100
    
    # Sharpness
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F).var()
    mean_val = np.mean(gray)
    
    return f"Gold:{gold:4.1f}%, White/Gems:{white:4.1f}%, Red:{red:4.1f}%, Skin:{skin_pct:4.1f}%, MeanB:{mean_val:4.1f}, Lap:{lap:5.1f}"

for item in ['IMG_0235', 'IMG_0360', 'IMG_0231', 'IMG_0329', 'IMG_0444', 'IMG_0588', 'IMG_0828', 'IMG_0839', 'IMG_0143']:
    print(f"{item:10} -> {analyze_crop(item)}")
