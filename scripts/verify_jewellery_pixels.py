import os
import cv2
import numpy as np
import json

WORKSPACE = r"d:\Jewellery"
SCREENSHOT_DIR = os.path.join(WORKSPACE, "reports", "final-review-screenshots")

def audit_catalogue_desktop():
    cat_path = os.path.join(SCREENSHOT_DIR, "03_final_desktop_catalogue.png")
    if not os.path.exists(cat_path):
        return {"error": "03_final_desktop_catalogue.png not found"}

    img = cv2.imread(cat_path)
    h, w, _ = img.shape

    # In desktop catalogue: 3 columns:
    # Col 1: x: 25 to 452
    # Col 2: x: 490 to 917
    # Col 3: x: 955 to 1382
    # Row 1 cards: y: ~150 to ~650
    # Media image container is approx 427x427 within each card
    
    crops = {
        "PROD-001 (Earrings)": img[150:577, 25:452],
        "PROD-003 (Ruby Choker)": img[150:577, 490:917],
        "PROD-004 (Long Haar)": img[150:577, 955:1382],
    }

    card_reports = {}
    for name, crop in crops.items():
        uniq = len(np.unique(crop.reshape(-1, 3), axis=0))
        std = float(crop.std())
        
        # Check HSV for gold / gemstone color content
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        
        # Gold hue is typically 15 to 45 with saturation > 40
        gold_mask = (hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) & (hsv[:, :, 1] >= 40)
        gold_pixels = int(np.count_nonzero(gold_mask))

        # Ruby hue is typically 0 to 10 or 165 to 180 with saturation > 50
        ruby_mask = ((hsv[:, :, 0] <= 10) | (hsv[:, :, 0] >= 165)) & (hsv[:, :, 1] >= 50)
        ruby_pixels = int(np.count_nonzero(ruby_mask))

        # Placeholder detection (specific stroke color #997D3D -> BGR [61, 125, 153])
        bgr_gold = np.array([61, 125, 153])
        dist = np.abs(crop.astype(int) - bgr_gold).sum(axis=2)
        placeholder_hits = int(np.count_nonzero(dist < 20))

        # Real photo criteria: > 5000 unique colors, std > 25, non-zero gold/ruby pixels
        is_real_photo = (uniq > 5000) and (std > 25.0) and (gold_pixels > 1000 or ruby_pixels > 1000)

        card_reports[name] = {
            "crop_shape": f"{crop.shape[1]}x{crop.shape[0]}",
            "unique_colors": uniq,
            "std_deviation": round(std, 1),
            "gold_pixels": gold_pixels,
            "ruby_pixels": ruby_pixels,
            "placeholder_hits": placeholder_hits,
            "status": "PASS - REAL JEWELLERY VISIBLE" if is_real_photo else "FAIL - BLANK / PLACEHOLDER"
        }

    return card_reports

def audit_modal():
    modal_path = os.path.join(SCREENSHOT_DIR, "04_final_desktop_product_modal.png")
    if not os.path.exists(modal_path):
        return {"error": "04_final_desktop_product_modal.png not found"}

    img = cv2.imread(modal_path)
    # The modal visual column is on left side
    modal_crop = img[100:800, 100:700]
    uniq = len(np.unique(modal_crop.reshape(-1, 3), axis=0))
    std = float(modal_crop.std())
    is_real = uniq > 10000 and std > 30

    return {
        "crop_shape": f"{modal_crop.shape[1]}x{modal_crop.shape[0]}",
        "unique_colors": uniq,
        "std_deviation": round(std, 1),
        "status": "PASS - MODAL MASTERPIECE VISIBLE" if is_real else "FAIL - BLANK"
    }

def audit_search():
    search_path = os.path.join(SCREENSHOT_DIR, "05_final_desktop_search_modal.png")
    if not os.path.exists(search_path):
        return {"error": "05_final_desktop_search_modal.png not found"}

    img = cv2.imread(search_path)
    # Search dialog has result list with thumbnails
    dialog_crop = img[150:700, 300:1140]
    uniq = len(np.unique(dialog_crop.reshape(-1, 3), axis=0))
    std = float(dialog_crop.std())
    is_real = uniq > 8000 and std > 25

    return {
        "crop_shape": f"{dialog_crop.shape[1]}x{dialog_crop.shape[0]}",
        "unique_colors": uniq,
        "std_deviation": round(std, 1),
        "status": "PASS - SEARCH RESULTS WITH THUMBNAILS VISIBLE" if is_real else "FAIL - BLANK"
    }

def audit_mobile_catalogue():
    mob_path = os.path.join(SCREENSHOT_DIR, "08_final_mobile_catalogue_390.png")
    if not os.path.exists(mob_path):
        return {"error": "08_final_mobile_catalogue_390.png not found"}

    img = cv2.imread(mob_path)
    h, w, _ = img.shape
    # On mobile, width must be exact 390
    card1_crop = img[140:550, 20:370]
    uniq = len(np.unique(card1_crop.reshape(-1, 3), axis=0))
    std = float(card1_crop.std())
    
    hsv = cv2.cvtColor(card1_crop, cv2.COLOR_BGR2HSV)
    gold_mask = (hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) & (hsv[:, :, 1] >= 40)
    gold_pixels = int(np.count_nonzero(gold_mask))

    is_real = (w == 390) and (uniq > 5000) and (gold_pixels > 1000)

    return {
        "width": w,
        "crop_shape": f"{card1_crop.shape[1]}x{card1_crop.shape[0]}",
        "unique_colors": uniq,
        "std_deviation": round(std, 1),
        "gold_pixels": gold_pixels,
        "status": "PASS - MOBILE JEWELLERY VISIBLE AT 390PX" if is_real else "FAIL"
    }

if __name__ == "__main__":
    report = {
        "desktop_catalogue": audit_catalogue_desktop(),
        "product_modal": audit_modal(),
        "search_modal": audit_search(),
        "mobile_catalogue_390": audit_mobile_catalogue()
    }
    print(json.dumps(report, indent=2))
    with open(os.path.join(WORKSPACE, "reports", "jewellery_pixel_verification.json"), "w") as f:
        json.dump(report, f, indent=2)
