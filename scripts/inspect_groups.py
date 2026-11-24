import os
import cv2
import numpy as np
from PIL import Image

thumb_dir = os.path.join('scripts', 'thumbs')

# Let's inspect each folder group in detail by checking object bounding boxes,
# aspect ratios, color patterns, and feature similarity
def inspect_group(files, group_title):
    print(f"\n==========================================")
    print(f"GROUP: {group_title}")
    print(f"==========================================")
    for fn in files:
        # find matching thumb
        matching = [f for f in os.listdir(thumb_dir) if fn in f]
        if not matching:
            print(f"  {fn}: Not found")
            continue
        p = os.path.join(thumb_dir, matching[0])
        img = cv2.imread(p)
        h, w = img.shape[:2]
        
        # Detect objects
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Check center 60%
        ch1, ch2 = int(h*0.2), int(h*0.8)
        cw1, cw2 = int(w*0.2), int(w*0.8)
        center = img[ch1:ch2, cw1:cw2]
        c_hsv = hsv[ch1:ch2, cw1:cw2]
        
        gold = np.sum(cv2.inRange(c_hsv, np.array([15, 40, 70]), np.array([35, 255, 255])) > 0) / (center.shape[0]*center.shape[1])
        white = np.sum(cv2.inRange(c_hsv, np.array([0, 0, 180]), np.array([180, 50, 255])) > 0) / (center.shape[0]*center.shape[1])
        
        # Check if hand/skin is present in upper or lower half
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        skin = (cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127])) > 0) & \
               (cv2.inRange(hsv, np.array([0, 30, 80]), np.array([25, 170, 255])) > 0)
        
        top_skin = np.sum(skin[:int(h*0.4), :]) / (w * h * 0.4)
        bot_skin = np.sum(skin[int(h*0.6):, :]) / (w * h * 0.4)
        
        print(f"  {fn:20} | Res:{w}x{h} | Gold:{gold*100:4.1f}% | White/Gems:{white*100:4.1f}% | TopSkin:{top_skin*100:4.1f}% | BotSkin:{bot_skin*100:4.1f}%")

inspect_group(["IMG_0423.JPG.jpeg", "IMG_0428.JPG.jpeg", "IMG_0429.JPG.jpeg", "IMG_0431.JPG.jpeg"], "01_Earrings_Set_1")
inspect_group(["IMG_0437.JPG.jpeg", "IMG_0438.JPG.jpeg", "IMG_0439.JPG.jpeg", "IMG_0440.JPG.jpeg", "IMG_0441.JPG.jpeg", "IMG_0442.JPG.jpeg"], "02_Earrings_Set_2")
inspect_group(["IMG_0062.JPG.jpeg"], "03_Necklace")
inspect_group(["IMG_0143.PNG"], "04_Long_Necklace")
inspect_group(["IMG_0300.HEIC", "IMG_0301.HEIC", "IMG_0302.HEIC", "IMG_0303.HEIC", "IMG_0299.HEIC"], "05_Ornate_Closeups_and_0299")
inspect_group(["IMG_0344.HEIC", "IMG_0345.HEIC", "IMG_0350.HEIC", "IMG_0351.HEIC", "IMG_0352.HEIC", "IMG_0353.HEIC", "IMG_0354.HEIC", "IMG_0355.HEIC"], "06_Chain_Grey_and_07_0351-0355")
inspect_group(["IMG_0034.HEIC", "IMG_0035.HEIC", "IMG_0037.HEIC", "IMG_0038.HEIC", "IMG_0039.HEIC", "IMG_0040.HEIC", "IMG_0041.HEIC", "IMG_0042.HEIC", "IMG_0043.HEIC", "IMG_0044.HEIC", "IMG_0235.HEIC", "IMG_0360.HEIC"], "07_Fabric_Group")
inspect_group(["IMG_0231.HEIC", "IMG_0299.HEIC", "IMG_0329.HEIC", "IMG_0444.HEIC", "IMG_0588.HEIC", "IMG_0828.HEIC", "IMG_0839.JPG.jpeg"], "08_Review_and_09_Fastening")
