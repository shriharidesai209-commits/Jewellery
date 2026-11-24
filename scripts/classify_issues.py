import os
import cv2
import numpy as np

thumb_dir = os.path.join('scripts', 'thumbs')

# Let's inspect each image's features to understand what it shows
files = sorted([f for f in os.listdir(thumb_dir) if f.endswith('.jpg')])

for f in files:
    p = os.path.join(thumb_dir, f)
    img = cv2.imread(p)
    h, w = img.shape[:2]
    
    # Analyze brightness and distribution
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mean_val = np.mean(gray)
    std_val = np.std(gray)
    
    # Sharpness (laplacian variance)
    lap = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Check if image is dark, blurry, or low contrast
    issues = []
    if mean_val < 55:
        issues.append("DARK")
    if lap < 60:
        issues.append("BLURRY")
    if std_val < 35:
        issues.append("LOW_CONTRAST")
    
    # Check color
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red1 = cv2.inRange(hsv, np.array([0, 50, 40]), np.array([10, 255, 255]))
    red2 = cv2.inRange(hsv, np.array([170, 50, 40]), np.array([180, 255, 255]))
    red_pct = np.sum((red1 | red2) > 0) / (w * h) * 100
    
    gold_pct = np.sum(cv2.inRange(hsv, np.array([15, 40, 70]), np.array([35, 255, 255])) > 0) / (w * h) * 100
    
    # Skin
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    skin_mask = (cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127])) > 0) & \
                (cv2.inRange(hsv, np.array([0, 30, 80]), np.array([25, 170, 255])) > 0)
    skin_pct = np.sum(skin_mask) / (w * h) * 100
    if skin_pct > 15:
        issues.append(f"HAND_VISIBLE({skin_pct:.0f}%)")
        
    fn = f.replace('.jpg', '')
    issue_str = ", ".join(issues) if issues else "CLEAN"
    print(f"{fn:55} | Red:{red_pct:4.1f}% | Gold:{gold_pct:4.1f}% | Lap:{lap:6.1f} | Issues: {issue_str}")
