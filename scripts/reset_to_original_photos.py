import json
import os

WORKSPACE = r"d:\Jewellery"
JSON_PATH = os.path.join(WORKSPACE, "data", "products.json")
JS_PATH = os.path.join(WORKSPACE, "js", "data", "products.js")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

img_map = {
    "PROD-001": {
        "default": "assets/raw-jewellery/extracted/01_Earrings_Set_1_0423/IMG_0428.JPG.jpeg",
        "detail": "assets/raw-jewellery/extracted/01_Earrings_Set_1_0423/IMG_0429.JPG.jpeg",
        "gallery": "assets/raw-jewellery/extracted/01_Earrings_Set_1_0423/IMG_0423.JPG.jpeg",
        "w": 3840, "h": 2160
    },
    "PROD-003": {
        "default": "assets/raw-jewellery/extracted/03_Necklace_IMG_0062/IMG_0062.JPG.jpeg",
        "w": 1280, "h": 960
    },
    "PROD-004": {
        "default": "assets/raw-jewellery/extracted/04_Long_Necklace_IMG_0143/IMG_0143.PNG",
        "is_png": True,
        "w": 1441, "h": 1078
    },
    "PROD-007A": {
        "default": "assets/raw-jewellery/extracted/07_Fabric_Background_Reference/IMG_0037.jpg",
        "w": 3024, "h": 4032
    },
    "PROD-007B": {
        "default": "assets/raw-jewellery/extracted/07_Fabric_Background_Reference/IMG_0041.jpg",
        "w": 3024, "h": 4032
    }
}

for p in data["products"]:
    pid = p["id"]
    cfg = img_map[pid]
    def_path = cfg["default"]
    w, h = cfg["w"], cfg["h"]
    
    for role in ["listing", "gallery", "featured", "detail", "master"]:
        r_path = cfg.get(role, def_path)
        img_entry = {
            "jpg": r_path,
            "width": w,
            "height": h,
            "aspectRatio": "Original Photo",
            "alt": f"{p['name']} Original Photograph"
        }
        if cfg.get("is_png"):
            img_entry["png"] = r_path
        p["images"][role] = img_entry

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# Generate js/data/products.js
js_content = f"""/**
 * Reusable Product Catalogue Data Module (Original Photographs Reset)
 * Source of truth: data/products.json
 * Strictly contains the 5 provisionally verified jewellery products using their original photographs.
 */

export const CATEGORIES = {{
  ALL: 'All Jewellery',
  EARRINGS: 'Earrings',
  NECKLACES: 'Necklaces & Chokers'
}};

export const VERIFIED_PRODUCTS = {json.dumps(data["products"], indent=2)};

export default VERIFIED_PRODUCTS;
"""

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_content)

print("Successfully updated data/products.json and js/data/products.js with original photographs!")
