import os
import shutil
import json
import csv
import math
import pillow_heif
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
import cv2
import numpy as np

pillow_heif.register_heif_opener()

print("==================================================")
print("STARTING JEWELLERY CURATION & ENHANCEMENT PIPELINE")
print("==================================================")

# Directories
RAW_DIR = os.path.join('assets', 'raw-jewellery', 'extracted')
OUTPUT_BASE = 'processed-jewellery'
INVENTORY_DIR = os.path.join(OUTPUT_BASE, 'inventory')
CONTACT_DIR = os.path.join(OUTPUT_BASE, 'contact-sheets')
GROUP_CONTACT_DIR = os.path.join(CONTACT_DIR, 'product-groups')
SELECTED_ORIG_DIR = os.path.join(OUTPUT_BASE, 'selected-originals')
ENHANCED_DIR = os.path.join(OUTPUT_BASE, 'enhanced')
REVIEW_DIR = os.path.join(OUTPUT_BASE, 'review')
REJECTED_DIR = os.path.join(REVIEW_DIR, 'rejected')
UNCERTAIN_DIR = os.path.join(REVIEW_DIR, 'uncertain-grouping')
FAILURES_DIR = os.path.join(REVIEW_DIR, 'enhancement-failures')
REPORTS_DIR = os.path.join(OUTPUT_BASE, 'reports')

for d in [INVENTORY_DIR, CONTACT_DIR, GROUP_CONTACT_DIR, SELECTED_ORIG_DIR, ENHANCED_DIR,
          REJECTED_DIR, UNCERTAIN_DIR, FAILURES_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)

# Load existing analysis data
with open('scripts/raw_inventory.json', 'r', encoding='utf-8') as f:
    raw_inventory = json.load(f)

# ----------------------------------------------------
# STEP 1: Inventory CSV
# ----------------------------------------------------
print("\n--- STEP 1: Generating image_inventory.csv ---")

csv_path = os.path.join(INVENTORY_DIR, 'image_inventory.csv')
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'filename', 'folder', 'format', 'width', 'height', 'size_kb',
        'mean_brightness', 'std_contrast', 'sharpness_laplacian',
        'perceptual_hash', 'quality_status', 'issues_detected'
    ])
    
    for item in raw_inventory:
        b = item.get('mean_brightness', 0)
        c = item.get('std_contrast', 0)
        s = item.get('laplacian_variance', 0)
        fn = item['filename']
        sz_kb = round(item.get('size_bytes', 0) / 1024, 1)
        
        issues = []
        if b < 55:
            issues.append('Underexposed/Dark')
        elif b > 140:
            issues.append('Overexposed')
        if s < 60:
            issues.append('Blurry/Soft')
        if c < 35:
            issues.append('Low-Contrast')
            
        # Specific file flags
        if fn == 'IMG_0329.HEIC':
            issues.append('Severe Blur & Hand Obstruction')
        elif fn == 'IMG_0444.HEIC':
            issues.append('Hand Obstruction & Awkward Angle')
        elif fn in ['IMG_0038.HEIC', 'IMG_0040.HEIC', 'IMG_0041.HEIC']:
            issues.append('Near-Duplicate Burst Shot')
        elif fn == 'IMG_0044.HEIC':
            issues.append('Blurry Burst Shot')
            
        status = 'Rejected' if ('Severe Blur' in ' '.join(issues) or s < 30) else ('Review Needed' if issues else 'Suitable')
        
        writer.writerow([
            fn, item['folder'], item.get('format', ''), item.get('width', 0),
            item.get('height', 0), sz_kb, b, c, s,
            item.get('dhash', ''), status, '; '.join(issues) if issues else 'None'
        ])

print(f"Saved: {csv_path}")

# ----------------------------------------------------
# STEP 2: Product Grouping Definition
# ----------------------------------------------------
print("\n--- STEP 2: Defining Product Groups ---")

product_groups = {
    "product-001": {
        "id": "product-001",
        "name": "Traditional Gold Drop Earrings (Design 1)",
        "category": "Earrings",
        "description": "Ornate 22K yellow gold chandelier drop earrings featuring intricate filigree work, spherical drop bell, and textured suspension loop.",
        "source_folder": "01_Earrings_Set_1_0423",
        "source_files": [
            "01_Earrings_Set_1_0423/IMG_0423.JPG.jpeg",
            "01_Earrings_Set_1_0423/IMG_0428.JPG.jpeg",
            "01_Earrings_Set_1_0423/IMG_0429.JPG.jpeg",
            "01_Earrings_Set_1_0423/IMG_0431.JPG.jpeg"
        ],
        "roles": {
            "front_view": ["01_Earrings_Set_1_0423/IMG_0423.JPG.jpeg"],
            "alternate_front": ["01_Earrings_Set_1_0423/IMG_0428.JPG.jpeg"],
            "side_angle_view": ["01_Earrings_Set_1_0423/IMG_0429.JPG.jpeg"],
            "detail_view": ["01_Earrings_Set_1_0423/IMG_0431.JPG.jpeg"],
            "back_view": [],
            "scale_reference": [],
            "redundant": []
        },
        "confidence": "High",
        "notes": "Verified coherent product group. IMG_0423 provides the cleanest front profile without upper hand obstruction."
    },
    "product-002": {
        "id": "product-002",
        "name": "Diamond & Gold Chandelier Drop Earrings (Design 2)",
        "category": "Earrings",
        "description": "Multi-tier statement drop earrings featuring white gemstone / diamond clusters set in yellow gold, complete with lower articulation and secure post fastening.",
        "source_folder": "02_Earrings_Set_2_0437",
        "source_files": [
            "02_Earrings_Set_2_0437/IMG_0437.JPG.jpeg",
            "02_Earrings_Set_2_0437/IMG_0438.JPG.jpeg",
            "02_Earrings_Set_2_0437/IMG_0439.JPG.jpeg",
            "02_Earrings_Set_2_0437/IMG_0440.JPG.jpeg",
            "02_Earrings_Set_2_0437/IMG_0441.JPG.jpeg",
            "02_Earrings_Set_2_0437/IMG_0442.JPG.jpeg"
        ],
        "roles": {
            "front_view": ["02_Earrings_Set_2_0437/IMG_0437.JPG.jpeg"],
            "side_angle_view": ["02_Earrings_Set_2_0437/IMG_0439.JPG.jpeg"],
            "detail_view": ["02_Earrings_Set_2_0437/IMG_0438.JPG.jpeg"],
            "profile_view": ["02_Earrings_Set_2_0437/IMG_0440.JPG.jpeg"],
            "back_fastening_view": ["02_Earrings_Set_2_0437/IMG_0441.JPG.jpeg"],
            "redundant": ["02_Earrings_Set_2_0437/IMG_0442.JPG.jpeg"]
        },
        "confidence": "High",
        "notes": "Rich multi-angle set. IMG_0441 captures the rear clasp/fastening. IMG_0442 is rejected due to poor perspective and low visual utility."
    },
    "product-003": {
        "id": "product-003",
        "name": "Royal Gold Choker Necklace",
        "category": "Necklace",
        "description": "Exquisite bridal gold choker necklace featuring floral and paisley openwork filigree motifs with hanging gold bead droplets.",
        "source_folder": "03_Necklace_IMG_0062",
        "source_files": [
            "03_Necklace_IMG_0062/IMG_0062.JPG.jpeg"
        ],
        "roles": {
            "front_view": ["03_Necklace_IMG_0062/IMG_0062.JPG.jpeg"],
            "side_angle_view": [],
            "detail_view": [],
            "back_view": [],
            "scale_reference": [],
            "redundant": []
        },
        "confidence": "High",
        "notes": "Single primary shot. Requires exposure elevation and background replacement from dark red velvet to luxury studio ivory."
    },
    "product-004": {
        "id": "product-004",
        "name": "Temple Heritage Long Gold Haar Necklace",
        "category": "Necklace",
        "description": "Grand heritage gold haar featuring interlocking textured chain links and an ornate handcrafted temple pendant.",
        "source_folder": "04_Long_Necklace_IMG_0143",
        "source_files": [
            "04_Long_Necklace_IMG_0143/IMG_0143.PNG"
        ],
        "roles": {
            "front_view": ["04_Long_Necklace_IMG_0143/IMG_0143.PNG"],
            "side_angle_view": [],
            "detail_view": [],
            "back_view": [],
            "scale_reference": [],
            "redundant": []
        },
        "confidence": "High",
        "notes": "Vertical presentation shot ideal for product detail page and vertical mobile cards."
    },
    "product-005": {
        "id": "product-005",
        "name": "Antique Ornate Gold Statement Piece",
        "category": "Statement Jewellery / Pendant",
        "description": "Antique finished gold statement piece featuring master-crafted micro-filigree lace, dual floral medallions, and handset gemstone accents.",
        "source_folder": "05_Ornate_Jewellery_Closeups_0300 & 08_Dark_or_Unclear_Review",
        "source_files": [
            "08_Dark_or_Unclear_Review/IMG_0299.HEIC",
            "05_Ornate_Jewellery_Closeups_0300/IMG_0300.HEIC",
            "05_Ornate_Jewellery_Closeups_0300/IMG_0301.HEIC",
            "05_Ornate_Jewellery_Closeups_0300/IMG_0302.HEIC",
            "05_Ornate_Jewellery_Closeups_0300/IMG_0303.HEIC"
        ],
        "roles": {
            "front_view": ["08_Dark_or_Unclear_Review/IMG_0299.HEIC"],
            "detail_view": [
                "05_Ornate_Jewellery_Closeups_0300/IMG_0300.HEIC",
                "05_Ornate_Jewellery_Closeups_0300/IMG_0301.HEIC",
                "05_Ornate_Jewellery_Closeups_0300/IMG_0302.HEIC",
                "05_Ornate_Jewellery_Closeups_0300/IMG_0303.HEIC"
            ],
            "side_angle_view": [],
            "back_view": [],
            "scale_reference": [],
            "redundant": []
        },
        "confidence": "High (Verified by 59 ORB feature matches)",
        "notes": "IMG_0299 was misplaced in folder 08 but visually and structurally matches the sequence 0300-0303. Serves as the primary full shot, while 0300-0303 serve as macro detail shots."
    },
    "product-006": {
        "id": "product-006",
        "name": "Contemporary Fine Gold Chain / Necklace",
        "category": "Chains & Collars",
        "description": "Delicate high-polish yellow gold chain necklace styled on natural architectural stone slab with velvet textile backdrop.",
        "source_folder": "06_Chain_or_Jewellery_on_Grey_0344 & 07_Fabric_Background_Reference",
        "source_files": [
            "06_Chain_or_Jewellery_on_Grey_0344/IMG_0344.HEIC",
            "06_Chain_or_Jewellery_on_Grey_0344/IMG_0345.HEIC",
            "06_Chain_or_Jewellery_on_Grey_0344/IMG_0350.HEIC",
            "07_Fabric_Background_Reference/IMG_0351.HEIC",
            "07_Fabric_Background_Reference/IMG_0352.HEIC",
            "07_Fabric_Background_Reference/IMG_0353.HEIC",
            "07_Fabric_Background_Reference/IMG_0354.HEIC",
            "07_Fabric_Background_Reference/IMG_0355.HEIC"
        ],
        "roles": {
            "front_view": ["06_Chain_or_Jewellery_on_Grey_0344/IMG_0344.HEIC"],
            "supporting_overhead": ["06_Chain_or_Jewellery_on_Grey_0344/IMG_0350.HEIC"],
            "side_angle_view": ["06_Chain_or_Jewellery_on_Grey_0344/IMG_0345.HEIC", "07_Fabric_Background_Reference/IMG_0352.HEIC"],
            "scale_reference": ["07_Fabric_Background_Reference/IMG_0353.HEIC"],
            "detail_view": ["07_Fabric_Background_Reference/IMG_0355.HEIC"],
            "redundant": [
                "07_Fabric_Background_Reference/IMG_0351.HEIC",
                "07_Fabric_Background_Reference/IMG_0354.HEIC"
            ]
        },
        "confidence": "High (Verified across sequence 0344-0355)",
        "notes": "Visual continuity across folder 06 and files 0351-0355 from folder 07. Natural stone background provides premium secondary aesthetic."
    },
    "product-007": {
        "id": "product-007",
        "name": "Circular Floral Gold Bridal Choker",
        "category": "Necklace",
        "description": "Grand circular gold collar necklace featuring articulated scallop motifs, raised floral bosses, and drop clusters.",
        "source_folder": "07_Fabric_Background_Reference (IMG_0034-0044)",
        "source_files": [
            "07_Fabric_Background_Reference/IMG_0034.HEIC",
            "07_Fabric_Background_Reference/IMG_0035.HEIC",
            "07_Fabric_Background_Reference/IMG_0037.HEIC",
            "07_Fabric_Background_Reference/IMG_0038.HEIC",
            "07_Fabric_Background_Reference/IMG_0039.HEIC",
            "07_Fabric_Background_Reference/IMG_0040.HEIC",
            "07_Fabric_Background_Reference/IMG_0041.HEIC",
            "07_Fabric_Background_Reference/IMG_0042.HEIC",
            "07_Fabric_Background_Reference/IMG_0043.HEIC",
            "07_Fabric_Background_Reference/IMG_0044.HEIC"
        ],
        "roles": {
            "front_view": ["07_Fabric_Background_Reference/IMG_0037.HEIC"],
            "supporting_front": ["07_Fabric_Background_Reference/IMG_0035.HEIC"],
            "side_angle_view": ["07_Fabric_Background_Reference/IMG_0042.HEIC"],
            "detail_view": ["07_Fabric_Background_Reference/IMG_0043.HEIC"],
            "alternate_take": ["07_Fabric_Background_Reference/IMG_0039.HEIC"],
            "redundant": [
                "07_Fabric_Background_Reference/IMG_0034.HEIC",
                "07_Fabric_Background_Reference/IMG_0038.HEIC",
                "07_Fabric_Background_Reference/IMG_0040.HEIC",
                "07_Fabric_Background_Reference/IMG_0041.HEIC",
                "07_Fabric_Background_Reference/IMG_0044.HEIC"
            ]
        },
        "confidence": "High (Burst sequence of one product)",
        "notes": "Although labeled as fabric reference in the raw zip, clear visual evidence confirms a full circular bridal choker. IMG_0037 is the sharpest and best exposed."
    }
}

groups_path = os.path.join(INVENTORY_DIR, 'product_groups.json')
with open(groups_path, 'w', encoding='utf-8') as f:
    json.dump(product_groups, f, indent=2)

print(f"Saved: {groups_path}")

# ----------------------------------------------------
# STEP 3: Selection Manifest
# ----------------------------------------------------
print("\n--- STEP 3: Generating selection_manifest.json ---")

selection_manifest = {
    "curated_products": {},
    "review_items": {
        "uncertain_grouping": [
            {
                "file": "07_Fabric_Background_Reference/IMG_0235.HEIC",
                "reason": "Isolated low-contrast gold element on red fabric; insufficient context to associate with a known set."
            },
            {
                "file": "07_Fabric_Background_Reference/IMG_0360.HEIC",
                "reason": "Fragmented cluster of small gold components; unclear whether loose elements or disassembled set."
            },
            {
                "file": "08_Dark_or_Unclear_Review/IMG_0231.HEIC",
                "reason": "White stone/silver piece, underexposed, single isolated take without companion views."
            },
            {
                "file": "08_Dark_or_Unclear_Review/IMG_0444.HEIC",
                "reason": "Severe hand obstruction holding multiple jewellery pieces across fingers; unsuited for catalog hero."
            },
            {
                "file": "08_Dark_or_Unclear_Review/IMG_0588.HEIC",
                "reason": "Severe underexposure on long necklace; needs studio re-shoot rather than excessive digital boosting."
            },
            {
                "file": "08_Dark_or_Unclear_Review/IMG_0828.HEIC",
                "reason": "Low-contrast, underexposed gold element on red velvet; lacks paired views."
            },
            {
                "file": "09_Fastening_or_Extra_View/IMG_0839.JPG.jpeg",
                "reason": "Isolated clasp/rear detail; product association to a specific front view is unconfirmed."
            }
        ],
        "rejected": [
            {
                "file": "08_Dark_or_Unclear_Review/IMG_0329.HEIC",
                "reason": "Severe motion blur (Laplacian variance 8.97), 78% finger obstruction. Completely unsuitable."
            },
            {
                "file": "02_Earrings_Set_2_0437/IMG_0442.JPG.jpeg",
                "reason": "Poor perspective angle; extreme edge view offering minimal visual detail of earring."
            },
            {
                "file": "07_Fabric_Background_Reference/IMG_0044.HEIC",
                "reason": "Blurry burst duplicate (Laplacian 22.98) of product-007."
            },
            {
                "file": "07_Fabric_Background_Reference/IMG_0038.HEIC",
                "reason": "Severely overexposed duplicate take of product-007."
            },
            {
                "file": "07_Fabric_Background_Reference/IMG_0040.HEIC",
                "reason": "Near-duplicate redundant burst frame of product-007."
            },
            {
                "file": "07_Fabric_Background_Reference/IMG_0041.HEIC",
                "reason": "Near-duplicate redundant burst frame of product-007."
            },
            {
                "file": "07_Fabric_Background_Reference/IMG_0351.HEIC",
                "reason": "Redundant flat-lay take of product-006 on stone."
            },
            {
                "file": "07_Fabric_Background_Reference/IMG_0354.HEIC",
                "reason": "Redundant flat-lay take of product-006 on stone."
            }
        ]
    }
}

for pid, pdata in product_groups.items():
    primary = pdata['roles']['front_view'][0]
    supporting = []
    for role_name, flist in pdata['roles'].items():
        if role_name not in ['front_view', 'redundant']:
            supporting.extend(flist)
    
    selection_manifest['curated_products'][pid] = {
        "product_name": pdata['name'],
        "category": pdata['category'],
        "primary_hero": primary,
        "supporting_views": supporting,
        "detail_views": pdata['roles'].get('detail_view', []),
        "rejected_views": pdata['roles'].get('redundant', []),
        "selection_rationale": pdata['notes']
    }

manifest_path = os.path.join(INVENTORY_DIR, 'selection_manifest.json')
with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(selection_manifest, f, indent=2)

print(f"Saved: {manifest_path}")

# ----------------------------------------------------
# STEP 4: Populate selected-originals & review folders
# ----------------------------------------------------
print("\n--- STEP 4: Populating selected-originals and review directories ---")

for pid, pinfo in selection_manifest['curated_products'].items():
    dest_dir = os.path.join(SELECTED_ORIG_DIR, pid)
    os.makedirs(dest_dir, exist_ok=True)
    all_selected = [pinfo['primary_hero']] + pinfo['supporting_views']
    for rel_f in set(all_selected):
        src = os.path.join(RAW_DIR, rel_f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dest_dir, os.path.basename(src)))

# Populate rejected
for rej in selection_manifest['review_items']['rejected']:
    src = os.path.join(RAW_DIR, rej['file'])
    if os.path.exists(src):
        dst = os.path.join(REJECTED_DIR, os.path.basename(src))
        shutil.copy2(src, dst)
        # write reason
        with open(dst + '.reason.txt', 'w', encoding='utf-8') as rf:
            rf.write(rej['reason'])

# Populate uncertain
for unc in selection_manifest['review_items']['uncertain_grouping']:
    src = os.path.join(RAW_DIR, unc['file'])
    if os.path.exists(src):
        dst = os.path.join(UNCERTAIN_DIR, os.path.basename(src))
        shutil.copy2(src, dst)
        with open(dst + '.reason.txt', 'w', encoding='utf-8') as rf:
            rf.write(unc['reason'])

print("Copied selected originals and categorized review files.")

# ----------------------------------------------------
# STEP 5: Product Group Contact Sheets
# ----------------------------------------------------
print("\n--- STEP 5: Generating Product Group Contact Sheets ---")

for pid, pdata in product_groups.items():
    files = pdata['source_files']
    n_files = len(files)
    if n_files == 0:
        continue
    cols = min(4, n_files)
    rows = math.ceil(n_files / cols)
    
    cell_w, cell_h = 360, 440
    gw, gh = cols * cell_w, rows * cell_h + 70
    
    gsheet = Image.new('RGB', (gw, gh), color=(24, 24, 28))
    gdraw = ImageDraw.Draw(gsheet)
    
    try:
        title_font = ImageFont.truetype('arialbd.ttf', 20)
        card_font = ImageFont.truetype('arialbd.ttf', 14)
        sub_font = ImageFont.truetype('arial.ttf', 12)
    except:
        title_font = ImageFont.load_default()
        card_font = title_font
        sub_font = title_font
        
    gdraw.text((20, 20), f"{pid.upper()}: {pdata['name']} ({n_files} photos)", fill=(245, 245, 245), font=title_font)
    
    for i, rel_f in enumerate(files):
        c = i % cols
        r = i // cols
        x0 = c * cell_w
        y0 = 65 + r * cell_h
        
        # Determine role tag
        role_tag = "Supporting"
        if rel_f in pdata['roles'].get('front_view', []):
            role_tag = "PRIMARY HERO"
        elif rel_f in pdata['roles'].get('detail_view', []):
            role_tag = "Detail Close-Up"
        elif rel_f in pdata['roles'].get('redundant', []):
            role_tag = "REDUNDANT"
        elif rel_f in pdata['roles'].get('back_fastening_view', []):
            role_tag = "Fastening/Back"
            
        card_bg = (40, 40, 48) if role_tag != "REDUNDANT" else (48, 30, 30)
        gdraw.rectangle([x0 + 8, y0 + 8, x0 + cell_w - 8, y0 + cell_h - 8], fill=card_bg, outline=(65, 65, 75))
        
        p = os.path.join(RAW_DIR, rel_f)
        try:
            with Image.open(p) as img:
                img_t = ImageOps.exif_transpose(img).convert('RGB')
                img_t.thumbnail((cell_w - 30, cell_h - 100), Image.Resampling.LANCZOS)
                tw, th = img_t.size
                tx = x0 + (cell_w - tw) // 2
                ty = y0 + 15 + (cell_h - 100 - th) // 2
                gsheet.paste(img_t, (tx, ty))
        except Exception as e:
            pass
            
        tag_color = (110, 231, 183) if "HERO" in role_tag else ((248, 113, 113) if "REDUNDANT" in role_tag else (186, 230, 253))
        gdraw.text((x0 + 16, y0 + cell_h - 68), os.path.basename(rel_f), fill=(240, 240, 240), font=card_font)
        gdraw.text((x0 + 16, y0 + cell_h - 44), f"Role: {role_tag}", fill=tag_color, font=card_font)
        gdraw.text((x0 + 16, y0 + cell_h - 24), f"Dir: {os.path.dirname(rel_f)}", fill=(160, 160, 160), font=sub_font)
        
    out_sheet_p = os.path.join(GROUP_CONTACT_DIR, f"{pid}.jpg")
    gsheet.save(out_sheet_p, 'JPEG', quality=88)

print("Product group contact sheets saved.")

print("\nSTEP 1 - 5 completed successfully.")
