import os
from PIL import Image, ImageOps
import numpy as np
import cv2
import pillow_heif

pillow_heif.register_heif_opener()

p5 = 'assets/raw-jewellery/extracted/08_Dark_or_Unclear_Review/IMG_0299.HEIC'
with Image.open(p5) as im:
    im_t = ImageOps.exif_transpose(im).convert('RGB')
    np_img = np.array(im_t)

h, w = np_img.shape[:2]
print(f"IMG_0299 transposed size: {w}x{h}")

# Save resized for analysis
preview = cv2.resize(np_img, (800, int(800 * h / w)))
cv2.imwrite('scripts/remediation_test/tray_preview.jpg', cv2.cvtColor(preview, cv2.COLOR_RGB2BGR))

# Let's inspect the layout of the tray
# The tray typically has 3 or 4 columns and 4 rows of compartments
print(f"Width={w}, Height={h}")
