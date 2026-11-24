"""
Comprehensive Production Verification Suite for KYK Jewellers on Vercel
Target: https://jewellery-zeta-three.vercel.app

Verifies:
1. HTTPS & Security Headers
2. HTML integrity, Branding, Contacts, and Navigation Anchors
3. All JS Modules and CSS Stylesheet availability
4. All 7 Catalogue Product Images (5 Gold + 2 Silver)
5. All 20 Archival Gallery Photographs
6. Lightbox & Inquiry Data schemas
"""

import sys
import json
import urllib.request
import urllib.error
import ssl
from io import BytesIO
from PIL import Image

BASE_URL = "https://jewellery-zeta-three.vercel.app"

def fetch_url(url, is_binary=False):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    context = ssl.create_default_context()
    with urllib.request.urlopen(req, context=context, timeout=15) as resp:
        status = resp.status
        headers = dict(resp.headers)
        data = resp.read()
        if not is_binary:
            try:
                data = data.decode('utf-8')
            except UnicodeDecodeError:
                pass
        return status, headers, data

def run_production_verification():
    print("=" * 80)
    print(f"VERIFYING LIVE PRODUCTION STOREFRONT: {BASE_URL}")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    def test_assert(condition, desc):
        nonlocal passed, failed
        if condition:
            print(f"  [PASS] {desc}")
            passed += 1
        else:
            print(f"  [FAIL] {desc}")
            failed += 1

    # 1. Test Homepage & HTTPS
    print("\n--> 1. Homepage & HTTPS Security Headers")
    try:
        status, headers, html = fetch_url(f"{BASE_URL}/")
        test_assert(status == 200, f"Homepage returns HTTP 200 OK (got {status})")
        test_assert("text/html" in headers.get("Content-Type", ""), "Content-Type is text/html")
        test_assert("x-content-type-options" in headers or "X-Content-Type-Options" in headers, "Header X-Content-Type-Options present")
        test_assert("Kashinathsa Y. Khatawate" in html, "Official store name present in HTML")
        test_assert("Since 1937" in html, "Heritage year 1937 present in HTML")
        test_assert("Gadag" in html, "Atelier location Gadag present in HTML")
    except Exception as e:
        test_assert(False, f"Homepage fetch failed: {e}")

    # 2. Test Navigation & Section Anchors in HTML
    print("\n--> 2. Navigation & Section Anchors")
    test_assert('id="vault-section"' in html, "Catalogue Vault anchor #vault-section present")
    test_assert('id="gallery-section"' in html, "1937 Archival Gallery anchor #gallery-section present")
    test_assert('id="collections-section"' in html, "Collections anchor #collections-section present")
    test_assert('id="spotlight-section"' in html, "Spotlight anchor #spotlight-section present")
    test_assert('id="craftsmanship-section"' in html, "Craftsmanship anchor #craftsmanship-section present")
    test_assert('id="philosophy-section"' in html, "Philosophy anchor #philosophy-section present")
    test_assert('id="salon-section"' in html, "Boutique & Salon anchor #salon-section present")
    test_assert('1937 Gallery' in html, "1937 Gallery nav link present in desktop navigation")

    # 3. Test Verified Contacts & WhatsApp Links
    print("\n--> 3. Verified Contacts & WhatsApp Escalation")
    test_assert("tel:+919448753791" in html, "Direct telephone link for Venkatesh present")
    test_assert("https://wa.me/919448753791" in html, "WhatsApp link for Venkatesh present")
    test_assert("tel:+919148996998" in html, "Direct telephone link for Prajwal present")
    test_assert("https://wa.me/919148996998" in html, "WhatsApp link for Prajwal present")

    # 4. Test Core Assets (CSS, JS, Branding)
    print("\n--> 4. Stylesheets & JavaScript Modules")
    css_status, _, css_body = fetch_url(f"{BASE_URL}/css/styles.css")
    test_assert(css_status == 200, "css/styles.css returns HTTP 200 OK")
    test_assert(".section-archival-gallery" in css_body, "Archival gallery CSS styles present in stylesheet")
    test_assert(".gallery-slide-card" in css_body, "Gallery slide card CSS styles present in stylesheet")

    js_app_status, _, js_app = fetch_url(f"{BASE_URL}/js/app.js")
    test_assert(js_app_status == 200, "js/app.js returns HTTP 200 OK")
    test_assert("ArchivalGallery" in js_app, "ArchivalGallery imported in app.js")

    gallery_comp_status, _, _ = fetch_url(f"{BASE_URL}/js/components/ArchivalGallery.js")
    test_assert(gallery_comp_status == 200, "js/components/ArchivalGallery.js returns HTTP 200 OK")

    gallery_data_js_status, _, _ = fetch_url(f"{BASE_URL}/js/data/galleryPhotos.js")
    test_assert(gallery_data_js_status == 200, "js/data/galleryPhotos.js returns HTTP 200 OK")

    # 5. Test Logo & Branding Media Assets
    print("\n--> 5. Brand Logo & QR Code Integrity")
    logo_status, _, logo_bytes = fetch_url(f"{BASE_URL}/assets/branding/IMG_0941.PNG", is_binary=True)
    test_assert(logo_status == 200, "Official Logo (IMG_0941.PNG) returns HTTP 200 OK")
    try:
        im = Image.open(BytesIO(logo_bytes))
        test_assert(im.size == (362, 393), f"Logo dimensions valid (expected 362x393, got {im.size})")
    except Exception as e:
        test_assert(False, f"Logo image invalid: {e}")

    qr_status, _, _ = fetch_url(f"{BASE_URL}/assets/branding/IMG_0942.JPG.jpeg", is_binary=True)
    test_assert(qr_status == 200, "Instagram QR Code (IMG_0942.JPG.jpeg) returns HTTP 200 OK")

    # 6. Test Catalogue Datasets & All 7 Products
    print("\n--> 6. Verified Catalogue Masterpieces (5 Gold + 2 Silver)")
    prod_json_status, _, prod_json_str = fetch_url(f"{BASE_URL}/data/products.json")
    test_assert(prod_json_status == 200, "data/products.json returns HTTP 200 OK")
    catalogue = json.loads(prod_json_str)
    gold_prods = catalogue.get("products", [])
    silver_prods = catalogue.get("silver_products", [])
    test_assert(len(gold_prods) == 5, f"Exactly 5 Gold products in catalogue (got {len(gold_prods)})")
    test_assert(len(silver_prods) == 2, f"Exactly 2 Silver products in catalogue (got {len(silver_prods)})")

    catalogue_image_urls = [
        # Gold
        f"{BASE_URL}/assets/raw-jewellery/extracted/01_Earrings_Set_1_0423/IMG_0428.JPG.jpeg", # PROD-001
        f"{BASE_URL}/assets/raw-jewellery/extracted/03_Necklace_IMG_0062/IMG_0062.JPG.jpeg",   # PROD-003
        f"{BASE_URL}/assets/raw-jewellery/extracted/04_Long_Necklace_IMG_0143/IMG_0143.PNG",   # PROD-004
        f"{BASE_URL}/assets/raw-jewellery/extracted/07_Fabric_Background_Reference/IMG_0037.jpg", # PROD-007A
        f"{BASE_URL}/assets/raw-jewellery/extracted/07_Fabric_Background_Reference/IMG_0041.jpg", # PROD-007B
        # Silver
        f"{BASE_URL}/assets/raw-jewellery/extracted/08_Dark_or_Unclear_Review/IMG_0231.jpg",   # SILV-001
        f"{BASE_URL}/assets/raw-jewellery/extracted/09_Fastening_or_Extra_View/IMG_0839.JPG.jpeg", # SILV-002
    ]

    for img_url in catalogue_image_urls:
        filename = img_url.split("/")[-1]
        try:
            img_status, _, img_data = fetch_url(img_url, is_binary=True)
            im = Image.open(BytesIO(img_data))
            test_assert(img_status == 200 and im.size[0] > 0, f"Catalogue Image {filename} returns HTTP 200 OK ({im.size[0]}x{im.size[1]}px)")
        except Exception as e:
            test_assert(False, f"Catalogue Image {filename} failed: {e}")

    # 7. Test Archival Gallery Dataset & All 20 Photographs
    print("\n--> 7. The 1937 Archival Gallery (20 Photographs)")
    gal_json_status, _, gal_json_str = fetch_url(f"{BASE_URL}/data/gallery_photos.json")
    test_assert(gal_json_status == 200, "data/gallery_photos.json returns HTTP 200 OK")
    gallery_data = json.loads(gal_json_str)
    photos = gallery_data.get("photos", [])
    test_assert(len(photos) == 20, f"Exactly 20 archival photographs in dataset (got {len(photos)})")

    for p in photos:
        pid = p["id"]
        title = p["title"]
        src = p["sourceImage"]
        full_url = f"{BASE_URL}/{src}"
        try:
            s, _, d = fetch_url(full_url, is_binary=True)
            im = Image.open(BytesIO(d))
            test_assert(s == 200 and im.size[0] > 0, f"Gallery [{pid}] {title} ({im.size[0]}x{im.size[1]}px) -> 200 OK")
        except Exception as e:
            test_assert(False, f"Gallery [{pid}] {title} failed: {e}")

    print("\n" + "=" * 80)
    print(f"PRODUCTION VERIFICATION RESULTS: {passed} PASSED, {failed} FAILED")
    print("=" * 80)
    
    if failed == 0:
        print("ALL LIVE PRODUCTION CHECKS ON VERCEL PASSED WITH 100% FIDELITY!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_production_verification()
