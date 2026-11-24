#!/usr/bin/env python3
"""
scripts/reframe_hero_haar.py
Re-frames PROD-004 (Temple Long Gold Haar) on the 1920x1080 featured canvas.
Provides 345px of clean bottom margin clearance so the cascading gold swags
and lower beads remain 100% visible and unoccluded by the hero card overlay.
"""

import os
import cv2
import numpy as np

WORKSPACE = r"d:\Jewellery"
RAW_IMG = os.path.join(WORKSPACE, "assets", "raw-jewellery", "extracted", "04_Long_Necklace_IMG_0143", "IMG_0143.PNG")
MASK_IMG = os.path.join(WORKSPACE, "processed-jewellery-v2", "masks", "product-004_mask.png")
OUT_DIR = os.path.join(WORKSPACE, "processed-jewellery-v2", "enhanced", "product-004")

im = cv2.imread(RAW_IMG)
mask = cv2.imread(MASK_IMG, 0)

ys, xs = np.where(mask > 0)
cropped_bgr = im[ys.min():ys.max(), xs.min():xs.max()]
cropped_mask = mask[ys.min():ys.max(), xs.min():xs.max()]

def add_contact_shadow(canvas_bgr, mask, shadow_offset=(0, 20), blur_kernel=(51, 51), opacity=0.18):
    h, w = canvas_bgr.shape[:2]
    M = np.float32([[1, 0, shadow_offset[0]], [0, 1, shadow_offset[1]]])
    shifted_mask = cv2.warpAffine(mask, M, (w, h), borderValue=0)
    shadow = cv2.GaussianBlur(shifted_mask, blur_kernel, 0)
    norm_shadow = (shadow.astype(np.float32) / 255.0) * opacity
    for c in range(3):
        canvas_bgr[:, :, c] = (canvas_bgr[:, :, c] * (1.0 - norm_shadow)).astype(np.uint8)
    return canvas_bgr

target_w, target_h = 1920, 1080
new_h = 710
new_w = int(cropped_bgr.shape[1] * (new_h / cropped_bgr.shape[0]))
resized_bgr = cv2.resize(cropped_bgr, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
resized_mask = cv2.resize(cropped_mask, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

alpha = (cv2.GaussianBlur(resized_mask, (3, 3), 0).astype(np.float32) / 255.0)[:, :, np.newaxis]
canvas = np.full((target_h, target_w, 3), (242, 247, 249), dtype=np.uint8)

x_offset = (target_w - new_w) // 2
y_offset = 25 # Elevate haar to provide 345px bottom clearance

full_mask = np.zeros((target_h, target_w), dtype=np.uint8)
full_mask[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_mask
canvas = add_contact_shadow(canvas, full_mask)

roi = canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w]
comp = (resized_bgr.astype(np.float32) * alpha + roi.astype(np.float32) * (1.0 - alpha)).astype(np.uint8)
canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = comp

# Save dual formats
jpg_path = os.path.join(OUT_DIR, "featured.jpg")
webp_path = os.path.join(OUT_DIR, "featured.webp")

cv2.imwrite(jpg_path, canvas, [cv2.IMWRITE_JPEG_QUALITY, 95])
cv2.imwrite(webp_path, canvas, [cv2.IMWRITE_WEBP_QUALITY, 95])

print(f"Re-framed PROD-004 featured assets successfully:")
print(f"  {jpg_path} ({os.path.getsize(jpg_path)/1024:.1f} KB)")
print(f"  {webp_path} ({os.path.getsize(webp_path)/1024:.1f} KB)")
print(f"  Haar vertical placement: Y={y_offset}..{y_offset+new_h}, bottom clearance: {target_h - (y_offset+new_h)}px")
