import os
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import pillow_heif

pillow_heif.register_heif_opener()

print("==================================================")
print("RUNNING JEWELLERY IMAGE ENHANCEMENT ENGINE")
print("==================================================")

RAW_DIR = os.path.join('assets', 'raw-jewellery', 'extracted')
ENHANCED_DIR = os.path.join('processed-jewellery', 'enhanced')

# Color definitions
# Primary background: Warm ivory / cream / off-white
# RGB: (249, 247, 242) -> BGR: (242, 247, 249)
BG_IVORY_RGB = (249, 247, 242)
BG_IVORY_BGR = (242, 247, 249)

def load_image_rgb(rel_path):
    p = os.path.join(RAW_DIR, rel_path)
    with Image.open(p) as img:
        img_t = ImageOps.exif_transpose(img)
        rgb = img_t.convert('RGB')
        return np.array(rgb)

def create_studio_background(width, height, base_color_bgr=BG_IVORY_BGR, vignette_strength=0.03):
    bg = np.ones((height, width, 3), dtype=np.float32)
    y, x = np.ogrid[:height, :width]
    cx, cy = width / 2.0, height / 2.0
    r = np.sqrt(((x - cx) / cx)**2 + ((y - cy) / cy)**2)
    vignette = 1.0 - vignette_strength * np.clip(r, 0, 1.5)
    
    for c in range(3):
        bg[:, :, c] = base_color_bgr[c] * vignette
    return bg

def segment_red_velvet(img_bgr, remove_skin=True):
    h, w = img_bgr.shape[:2]
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    
    # Red in HSV
    m1 = cv2.inRange(hsv, np.array([0, 45, 25]), np.array([12, 255, 255]))
    m2 = cv2.inRange(hsv, np.array([168, 45, 25]), np.array([180, 255, 255]))
    red_hsv = m1 | m2
    
    # Red in LAB: high A channel
    red_lab = lab[:, :, 1] > 140
    red_bg = red_hsv | red_lab
    
    fg = ~red_bg
    
    if remove_skin:
        ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
        skin1 = cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127])) > 0
        skin2 = cv2.inRange(hsv, np.array([0, 25, 60]), np.array([28, 180, 255])) > 0
        skin = skin1 & skin2
        
        # Don't remove skin if it overlaps with gold highlights (gold has S > 80, V > 120 in specific H)
        gold = (hsv[:,:,0] >= 15) & (hsv[:,:,0] <= 36) & (hsv[:,:,1] >= 65)
        skin = skin & (~gold)
        fg = fg & (~skin)
        
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fg_clean = cv2.morphologyEx(fg.astype(np.uint8)*255, cv2.MORPH_OPEN, kernel)
    fg_clean = cv2.morphologyEx(fg_clean, cv2.MORPH_CLOSE, kernel)
    
    # Keep significant components
    cnts, _ = cv2.findContours(fg_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = w * h * 0.003
    large_cnts = [c for c in cnts if cv2.contourArea(c) > min_area]
    
    mask = np.zeros((h, w), dtype=np.uint8)
    if large_cnts:
        cv2.drawContours(mask, large_cnts, -1, 255, -1)
    else:
        mask = fg_clean
        
    # Smooth edge with Gaussian
    mask_blur = cv2.GaussianBlur(mask, (5, 5), 1.2)
    return mask_blur

def segment_dark_velvet(img_bgr):
    h, w = img_bgr.shape[:2]
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    # Threshold dark background (black velvet is very dark: gray < 38)
    _, fg = cv2.threshold(gray, 38, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg_clean = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel)
    fg_clean = cv2.morphologyEx(fg_clean, cv2.MORPH_CLOSE, kernel)
    
    cnts, _ = cv2.findContours(fg_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = w * h * 0.01
    large_cnts = [c for c in cnts if cv2.contourArea(c) > min_area]
    
    mask = np.zeros((h, w), dtype=np.uint8)
    if large_cnts:
        cv2.drawContours(mask, large_cnts, -1, 255, -1)
    else:
        mask = fg_clean
        
    mask_blur = cv2.GaussianBlur(mask, (5, 5), 1.2)
    return mask_blur

def calibrate_exposure(img_bgr, target_mean=110.0, max_gain=2.2):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    current_mean = np.mean(gray)
    if current_mean < target_mean:
        gain = min(target_mean / max(current_mean, 10.0), max_gain)
        # Apply gentle gamma curve rather than linear blowout
        gamma = 1.0 / (gain ** 0.6)
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(img_bgr, table)
    return img_bgr

def enhance_jewellery_item(rel_path, bg_type='ivory', exposure_boost=False, is_dark_bg=False):
    rgb = load_image_rgb(rel_path)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    h, w = bgr.shape[:2]
    
    # Optional exposure correction for underexposed pieces (e.g. IMG_0062)
    if exposure_boost:
        bgr = calibrate_exposure(bgr, target_mean=95.0, max_gain=1.8)
        
    # Segment foreground mask
    if is_dark_bg:
        mask = segment_dark_velvet(bgr)
    else:
        mask = segment_red_velvet(bgr)
        
    # Find bounding box of jewellery object
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if cnts:
        all_pts = np.vstack(cnts)
        bx, by, bw, bh = cv2.boundingRect(all_pts)
    else:
        bx, by, bw, bh = 0, 0, w, h
        
    # Crop to jewellery with 6% margin
    pad_x = int(bw * 0.06)
    pad_y = int(bh * 0.06)
    x1, y1 = max(0, bx - pad_x), max(0, by - pad_y)
    x2, y2 = min(w, bx + bw + pad_x), min(h, by + bh + pad_y)
    
    crop_bgr = bgr[y1:y2, x1:x2]
    crop_mask = mask[y1:y2, x1:x2]
    cw, ch = crop_bgr.shape[1], crop_bgr.shape[0]
    
    return crop_bgr, crop_mask

def compose_on_canvas(crop_bgr, crop_mask, target_w, target_h, padding_ratio=0.16, shadow_offset=(10, 16)):
    cw, ch = crop_bgr.shape[1], crop_bgr.shape[0]
    
    # Calculate fit scale inside canvas with padding
    max_avail_w = target_w * (1.0 - 2 * padding_ratio)
    max_avail_h = target_h * (1.0 - 2 * padding_ratio)
    
    scale = min(max_avail_w / cw, max_avail_h / ch)
    new_w = int(cw * scale)
    new_h = int(ch * scale)
    
    res_bgr = cv2.resize(crop_bgr, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    res_mask = cv2.resize(crop_mask, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    
    # Center position
    pos_x = (target_w - new_w) // 2
    pos_y = (target_h - new_h) // 2
    
    # Canvas background
    bg = create_studio_background(target_w, target_h, BG_IVORY_BGR)
    
    # Drop shadow calculation
    # 1. Contact shadow (tight, darker)
    contact_blur = cv2.GaussianBlur(res_mask, (15, 15), 4)
    # 2. Ambient drop shadow (soft, broader)
    ambient_blur = cv2.GaussianBlur(res_mask, (45, 45), 14)
    
    # Shift ambient shadow
    M_amb = np.float32([[1, 0, shadow_offset[0]], [0, 1, shadow_offset[1]]])
    shifted_ambient = cv2.warpAffine(ambient_blur, M_amb, (new_w, new_h))
    
    # Combine shadows onto canvas
    canvas_shadow = np.zeros((target_h, target_w), dtype=np.float32)
    
    # Paste contact and ambient shadow
    c_shadow_norm = (contact_blur.astype(np.float32) / 255.0) * 0.22
    a_shadow_norm = (shifted_ambient.astype(np.float32) / 255.0) * 0.18
    tot_shadow = np.clip(c_shadow_norm + a_shadow_norm, 0, 0.38)
    
    canvas_shadow[pos_y:pos_y+new_h, pos_x:pos_x+new_w] = tot_shadow
    
    # Apply shadow to canvas background
    canvas_shadow_3d = canvas_shadow[:, :, np.newaxis]
    bg = bg * (1.0 - canvas_shadow_3d)
    
    # Composite jewellery onto canvas
    alpha = (res_mask.astype(np.float32) / 255.0)[:, :, np.newaxis]
    
    canvas_roi = bg[pos_y:pos_y+new_h, pos_x:pos_x+new_w]
    comp_roi = res_bgr.astype(np.float32) * alpha + canvas_roi * (1.0 - alpha)
    bg[pos_y:pos_y+new_h, pos_x:pos_x+new_w] = comp_roi
    
    final_img = np.clip(bg, 0, 255).astype(np.uint8)
    return final_img

# Enhancement specs for all curated products
enhancement_jobs = [
    # product-001
    {
        "pid": "product-001",
        "primary": "01_Earrings_Set_1_0423/IMG_0423.JPG.jpeg",
        "supporting": [
            ("01_Earrings_Set_1_0423/IMG_0428.JPG.jpeg", "front_alternate"),
            ("01_Earrings_Set_1_0423/IMG_0429.JPG.jpeg", "angle_3quarter"),
            ("01_Earrings_Set_1_0423/IMG_0431.JPG.jpeg", "detail_macro")
        ],
        "is_dark": False,
        "exposure_boost": False
    },
    # product-002
    {
        "pid": "product-002",
        "primary": "02_Earrings_Set_2_0437/IMG_0437.JPG.jpeg",
        "supporting": [
            ("02_Earrings_Set_2_0437/IMG_0439.JPG.jpeg", "angle_3quarter"),
            ("02_Earrings_Set_2_0437/IMG_0438.JPG.jpeg", "detail_lower_cluster"),
            ("02_Earrings_Set_2_0437/IMG_0440.JPG.jpeg", "side_profile"),
            ("02_Earrings_Set_2_0437/IMG_0441.JPG.jpeg", "back_fastening")
        ],
        "is_dark": False,
        "exposure_boost": False
    },
    # product-003
    {
        "pid": "product-003",
        "primary": "03_Necklace_IMG_0062/IMG_0062.JPG.jpeg",
        "supporting": [],
        "is_dark": False,
        "exposure_boost": True # Needs exposure boost
    },
    # product-004
    {
        "pid": "product-004",
        "primary": "04_Long_Necklace_IMG_0143/IMG_0143.PNG",
        "supporting": [],
        "is_dark": False,
        "exposure_boost": False
    },
    # product-005
    {
        "pid": "product-005",
        "primary": "08_Dark_or_Unclear_Review/IMG_0299.HEIC",
        "supporting": [
            ("05_Ornate_Jewellery_Closeups_0300/IMG_0300.HEIC", "detail_filigree_top"),
            ("05_Ornate_Jewellery_Closeups_0300/IMG_0301.HEIC", "detail_gem_setting"),
            ("05_Ornate_Jewellery_Closeups_0300/IMG_0302.HEIC", "detail_floral_medallion"),
            ("05_Ornate_Jewellery_Closeups_0300/IMG_0303.HEIC", "detail_side_filigree")
        ],
        "is_dark": True, # Black velvet
        "exposure_boost": False
    },
    # product-006
    {
        "pid": "product-006",
        "primary": "06_Chain_or_Jewellery_on_Grey_0344/IMG_0344.HEIC",
        "supporting": [
            ("06_Chain_or_Jewellery_on_Grey_0344/IMG_0350.HEIC", "overhead_flatlay"),
            ("06_Chain_or_Jewellery_on_Grey_0344/IMG_0345.HEIC", "perspective_angle"),
            ("07_Fabric_Background_Reference/IMG_0352.HEIC", "stone_surface_angle"),
            ("07_Fabric_Background_Reference/IMG_0353.HEIC", "scale_reference"),
            ("07_Fabric_Background_Reference/IMG_0355.HEIC", "fabric_transition_detail")
        ],
        "is_dark": False,
        "exposure_boost": False,
        "preserve_stone": True # Special handling for natural stone styling
    },
    # product-007
    {
        "pid": "product-007",
        "primary": "07_Fabric_Background_Reference/IMG_0037.HEIC",
        "supporting": [
            ("07_Fabric_Background_Reference/IMG_0035.HEIC", "supporting_front"),
            ("07_Fabric_Background_Reference/IMG_0042.HEIC", "perspective_angle"),
            ("07_Fabric_Background_Reference/IMG_0043.HEIC", "detail_links"),
            ("07_Fabric_Background_Reference/IMG_0039.HEIC", "alternate_lighting")
        ],
        "is_dark": False,
        "exposure_boost": False
    }
]

def save_image_formats(img_bgr, base_path_no_ext):
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    
    # Save WebP
    webp_path = base_path_no_ext + ".webp"
    pil_img.save(webp_path, "WEBP", quality=92, method=6)
    
    # Save JPEG
    jpg_path = base_path_no_ext + ".jpg"
    pil_img.save(jpg_path, "JPEG", quality=92, optimize=True)
    
    return webp_path, jpg_path

# Execute enhancements
manifest_enhanced = {}

for job in enhancement_jobs:
    pid = job['pid']
    print(f"\nProcessing {pid}...")
    p_dir = os.path.join(ENHANCED_DIR, pid)
    for sub in ['master', 'listing', 'gallery', 'featured', 'detail']:
        os.makedirs(os.path.join(p_dir, sub), exist_ok=True)
        
    primary_rel = job['primary']
    crop_bgr, crop_mask = enhance_jewellery_item(
        primary_rel,
        exposure_boost=job.get('exposure_boost', False),
        is_dark_bg=job.get('is_dark', False)
    )
    
    # 1. Master High-Resolution
    master_bgr = compose_on_canvas(crop_bgr, crop_mask, 2400, 2400, padding_ratio=0.14)
    save_image_formats(master_bgr, os.path.join(p_dir, 'master', f"{pid}_master"))
    
    # 2. Product Listing Card (1:1 square, 1600x1600)
    listing_bgr = compose_on_canvas(crop_bgr, crop_mask, 1600, 1600, padding_ratio=0.16)
    save_image_formats(listing_bgr, os.path.join(p_dir, 'listing', f"{pid}_listing"))
    
    # 3. Product Detail Gallery Hero (4:5 vertical, 1600x2000)
    gallery_hero = compose_on_canvas(crop_bgr, crop_mask, 1600, 2000, padding_ratio=0.18)
    save_image_formats(gallery_hero, os.path.join(p_dir, 'gallery', f"{pid}_gallery_01_front"))
    
    # 4. Homepage / Featured Banner (16:9 landscape, 1920x1080)
    featured_bgr = compose_on_canvas(crop_bgr, crop_mask, 1920, 1080, padding_ratio=0.16)
    save_image_formats(featured_bgr, os.path.join(p_dir, 'featured', f"{pid}_featured_hero"))
    
    # 5. Detail / Macro Zoom View (1:1, 1200x1200)
    detail_bgr = compose_on_canvas(crop_bgr, crop_mask, 1200, 1200, padding_ratio=0.08)
    save_image_formats(detail_bgr, os.path.join(p_dir, 'detail', f"{pid}_detail_macro_01"))
    
    # Supporting views for gallery and detail
    supp_records = []
    for idx, (supp_rel, tag) in enumerate(job['supporting']):
        s_crop_bgr, s_crop_mask = enhance_jewellery_item(
            supp_rel,
            exposure_boost=job.get('exposure_boost', False),
            is_dark_bg=job.get('is_dark', False)
        )
        
        # Gallery view (4:5, 1600x2000)
        s_gallery = compose_on_canvas(s_crop_bgr, s_crop_mask, 1600, 2000, padding_ratio=0.18)
        g_name = f"{pid}_gallery_{idx+2:02d}_{tag}"
        save_image_formats(s_gallery, os.path.join(p_dir, 'gallery', g_name))
        
        # Detail view if marked as detail
        if 'detail' in tag:
            s_detail = compose_on_canvas(s_crop_bgr, s_crop_mask, 1200, 1200, padding_ratio=0.08)
            d_name = f"{pid}_detail_{tag}"
            save_image_formats(s_detail, os.path.join(p_dir, 'detail', d_name))
            
        supp_records.append({"source": supp_rel, "role": tag, "gallery_asset": g_name})
        
    print(f"  Completed {pid}: Generated master, listing, {len(job['supporting'])+1} gallery views, featured banner, and detail crops.")

print("\nALL PRODUCT ENHANCEMENTS AND DERIVATIVES COMPLETED.")
