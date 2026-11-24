#!/usr/bin/env python3
"""
scripts/repair_defects.py
Targeted visual defect repairs for Maison Aurum jewellery assets:
1. Fix Defect 1: Re-segment PROD-001 drop earrings to remove red velvet square and scale to 80% card fill.
2. Fix Defect 2: Re-generate macro detail shots for PROD-003 (ruby bezels) and Choker A (rhodium crest + tassels).
3. Update dual JPG and WebP formats in processed-jewellery-v2/enhanced/
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()

WORKSPACE = r"d:\Jewellery"
RAW_BASE = os.path.join(WORKSPACE, "assets", "raw-jewellery", "extracted")
V2_ENHANCED = os.path.join(WORKSPACE, "processed-jewellery-v2", "enhanced")
V2_MASKS = os.path.join(WORKSPACE, "processed-jewellery-v2", "masks")
BG_COLOR = (242, 247, 249) # BGR for warm ivory #F9F7F2

def add_contact_shadow(canvas_bgr, mask, shadow_offset=(0, 20), blur_kernel=(51, 51), opacity=0.18):
    h, w = canvas_bgr.shape[:2]
    M = np.float32([[1, 0, shadow_offset[0]], [0, 1, shadow_offset[1]]])
    shifted_mask = cv2.warpAffine(mask, M, (w, h), borderValue=0)
    shadow = cv2.GaussianBlur(shifted_mask, blur_kernel, 0)
    norm_shadow = (shadow.astype(np.float32) / 255.0) * opacity
    for c in range(3):
        canvas_bgr[:, :, c] = (canvas_bgr[:, :, c] * (1.0 - norm_shadow)).astype(np.uint8)
    return canvas_bgr

def compose_on_canvas(cropped_bgr, cropped_mask, target_w, target_h, padding_ratio=0.10):
    ch, cw = cropped_bgr.shape[:2]
    max_w = int(target_w * (1.0 - 2 * padding_ratio))
    max_h = int(target_h * (1.0 - 2 * padding_ratio))
    scale = min(max_w / cw, max_h / ch)
    new_w = max(1, int(cw * scale))
    new_h = max(1, int(ch * scale))
    
    resized_bgr = cv2.resize(cropped_bgr, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    resized_mask = cv2.resize(cropped_mask, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    blurred_mask = cv2.GaussianBlur(resized_mask, (3, 3), 0)
    alpha = (blurred_mask.astype(np.float32) / 255.0)[:, :, np.newaxis]
    
    canvas = np.full((target_h, target_w, 3), BG_COLOR, dtype=np.uint8)
    x_offset = (target_w - new_w) // 2
    y_offset = (target_h - new_h) // 2
    
    full_mask = np.zeros((target_h, target_w), dtype=np.uint8)
    full_mask[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_mask
    canvas = add_contact_shadow(canvas, full_mask)
    
    roi_canv = canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w]
    comp = (resized_bgr.astype(np.float32) * alpha + roi_canv.astype(np.float32) * (1.0 - alpha)).astype(np.uint8)
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = comp
    return canvas

def save_dual(bgr, base_path):
    cv2.imwrite(base_path + ".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 95])
    cv2.imwrite(base_path + ".webp", bgr, [cv2.IMWRITE_WEBP_QUALITY, 95])
    print(f"  Saved {base_path}.jpg and .webp ({bgr.shape[1]}x{bgr.shape[0]})")

def repair_product_001():
    print("--> Repairing Product 001 (Traditional Gold Drop Earrings)...")
    src = os.path.join(RAW_BASE, "01_Earrings_Set_1_0423", "IMG_0428.JPG.jpeg")
    im = cv2.imread(src)
    h, w = im.shape[:2]
    
    # Accurate earrings bounding ROI: Y 1480:2710, X 490:1800
    roi = im[1480:2710, 490:1800].copy()
    rh, rw = roi.shape[:2]
    
    # GrabCut segmentation
    mask_gc = np.zeros((rh, rw), np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    rect = (15, 15, rw - 30, rh - 30)
    cv2.grabCut(roi, mask_gc, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask_bin = np.where((mask_gc == 2) | (mask_gc == 0), 0, 1).astype('uint8') * 255
    
    # Save mask to masks directory for traceability
    full_mask = np.zeros((h, w), dtype=np.uint8)
    full_mask[1480:2710, 490:1800] = mask_bin
    cv2.imwrite(os.path.join(V2_MASKS, "product-001_mask.png"), full_mask)
    
    ys, xs = np.where(mask_bin > 0)
    cropped_bgr = roi[ys.min():ys.max(), xs.min():xs.max()]
    cropped_mask = mask_bin[ys.min():ys.max(), xs.min():xs.max()]
    
    out_dir = os.path.join(V2_ENHANCED, "product-001")
    
    # 1. Master: isolated object with alpha
    rgba = cv2.cvtColor(cropped_bgr, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = cv2.GaussianBlur(cropped_mask, (3, 3), 0)
    cv2.imwrite(os.path.join(out_dir, "master.png"), rgba)
    cv2.imwrite(os.path.join(out_dir, "master.webp"), rgba)
    print("  Saved master.png and master.webp")
    
    # 2. Listing card: 1:1, 1600x1600 (padding 0.10 for full card presence)
    listing = compose_on_canvas(cropped_bgr, cropped_mask, 1600, 1600, padding_ratio=0.10)
    save_dual(listing, os.path.join(out_dir, "listing"))
    
    # 3. Gallery image: 4:5, 1600x2000
    gallery = compose_on_canvas(cropped_bgr, cropped_mask, 1600, 2000, padding_ratio=0.12)
    save_dual(gallery, os.path.join(out_dir, "gallery"))
    
    # 4. Featured hero: 16:9, 1920x1080
    featured = compose_on_canvas(cropped_bgr, cropped_mask, 1920, 1080, padding_ratio=0.10)
    save_dual(featured, os.path.join(out_dir, "featured"))
    
    # 5. Detail shot: 1:1, 1200x1200 close-up of jhumka dome and filigree tassels
    det_roi = cropped_bgr[int(cropped_bgr.shape[0]*0.25):, :]
    det_mask = cropped_mask[int(cropped_mask.shape[0]*0.25):, :]
    detail = compose_on_canvas(det_roi, det_mask, 1200, 1200, padding_ratio=0.08)
    save_dual(detail, os.path.join(out_dir, "detail"))

def repair_product_003_detail():
    print("--> Repairing Product 003 Detail (Royal Gold Ruby Choker Ruby Bezels)...")
    src = os.path.join(RAW_BASE, "03_Necklace_IMG_0062", "IMG_0062.JPG.jpeg")
    im = cv2.imread(src)
    
    # Precise center crop containing ruby bezels and pearls
    det_crop = im[550:950, 280:680]
    
    # Mask inside this crop
    hsv = cv2.cvtColor(det_crop, cv2.COLOR_BGR2HSV)
    gold = (hsv[:,:,0] >= 14) & (hsv[:,:,0] <= 38) & (hsv[:,:,1] >= 40)
    pearl = (hsv[:,:,2] >= 160) & (hsv[:,:,1] <= 80)
    dori = (hsv[:,:,0] >= 35) & (hsv[:,:,0] <= 85) & (hsv[:,:,1] >= 30)
    ruby = ((hsv[:,:,0] <= 10) | (hsv[:,:,0] >= 170)) & (hsv[:,:,1] >= 80)
    structure = (gold | pearl | dori | ruby).astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    mask = cv2.morphologyEx(structure, cv2.MORPH_CLOSE, k)
    
    # Fill internal contours
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    main_cnts = [c for c in cnts if cv2.contourArea(c) > 5000]
    filled_mask = np.zeros_like(mask)
    cv2.drawContours(filled_mask, main_cnts, -1, 255, -1)
    
    out_dir = os.path.join(V2_ENHANCED, "product-003")
    detail = compose_on_canvas(det_crop, filled_mask, 1200, 1200, padding_ratio=0.08)
    save_dual(detail, os.path.join(out_dir, "detail"))

def repair_choker_a_detail():
    print("--> Repairing Choker A Detail (Rhodium Medallion & Tassels)...")
    src = os.path.join(RAW_BASE, "07_Fabric_Background_Reference", "IMG_0037.HEIC")
    with Image.open(src) as img_pil:
        im = cv2.cvtColor(np.array(ImageOps.exif_transpose(img_pil).convert("RGB")), cv2.COLOR_RGB2BGR)
    
    # Precise crop containing center rhodium medallion and dangling tassels
    det_crop = im[1950:3550, 712:2312]
    
    hsv = cv2.cvtColor(det_crop, cv2.COLOR_BGR2HSV)
    gold = (hsv[:,:,0] >= 12) & (hsv[:,:,0] <= 38) & (hsv[:,:,1] >= 40)
    rhodium = (hsv[:,:,2] >= 130) & (hsv[:,:,1] <= 70)
    jewel = (gold | rhodium).astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mask = cv2.morphologyEx(jewel, cv2.MORPH_CLOSE, k)
    
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    main_cnts = [c for c in cnts if cv2.contourArea(c) > 5000]
    filled_mask = np.zeros_like(mask)
    cv2.drawContours(filled_mask, main_cnts, -1, 255, -1)
    
    out_dir = os.path.join(V2_ENHANCED, "choker-a")
    detail = compose_on_canvas(det_crop, filled_mask, 1200, 1200, padding_ratio=0.08)
    save_dual(detail, os.path.join(out_dir, "detail"))

if __name__ == "__main__":
    repair_product_001()
    repair_product_003_detail()
    repair_choker_a_detail()
    print("--> All targeted asset repairs completed successfully!")
