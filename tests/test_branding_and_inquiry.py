#!/usr/bin/env python3
"""
Comprehensive Validation Suite: Client Branding, Contacts, WhatsApp, Instagram QR & Supabase Integration
Kashinathsa Y. Khatawate Jewellers (KYK Since 1937) · Gadag, Karnataka
"""

import os
import sys
import json
import re

WORKSPACE = r"d:\Jewellery"
INDEX_PATH = os.path.join(WORKSPACE, "index.html")
CSS_PATH = os.path.join(WORKSPACE, "css", "styles.css")
BRAND_JS_PATH = os.path.join(WORKSPACE, "js", "config", "brand.js")
SUPABASE_SQL_PATH = os.path.join(WORKSPACE, "supabase", "migrations", "20261124_create_inquiries_table.sql")
EDGE_FUNC_PATH = os.path.join(WORKSPACE, "supabase", "functions", "submit-inquiry", "index.ts")
INQUIRY_SERVICE_PATH = os.path.join(WORKSPACE, "js", "services", "inquiryService.js")
INQUIRY_MODAL_PATH = os.path.join(WORKSPACE, "js", "components", "InquiryModal.js")

class TestBrandingAndInquiry:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def assert_true(self, condition, test_name, error_msg=""):
        if condition:
            self.passed += 1
            print(f"  [PASS] {test_name}")
        else:
            self.failed += 1
            full_msg = f"  [FAIL] {test_name}: {error_msg}"
            print(full_msg)
            self.errors.append(full_msg)

    def run_all(self):
        print("================================================================================")
        print("KYK JEWELLERS — BRANDING, CONTACTS, WHATSAPP & SUPABASE TEST SUITE")
        print("================================================================================")

        self.test_brand_identity_and_removal_of_placeholders()
        self.test_logo_and_instagram_qr_assets()
        self.test_contact_names_phone_and_whatsapp_urls()
        self.test_metadata_and_favicon()
        self.test_supabase_schema_and_rls()
        self.test_edge_function_security_and_email()
        self.test_inquiry_service_and_modal()
        self.test_viewing_drawer_multi_piece_flow()
        self.test_silver_catalogue_integration()
        self.test_product_asset_and_design_preservation()

        print("================================================================================")
        print(f"RESULTS: {self.passed} Passed, {self.failed} Failed")
        print("================================================================================")

        if self.failed > 0:
            print("\nErrors encountered:")
            for e in self.errors:
                print(e)
            sys.exit(1)
        else:
            print("\nALL BRANDING, CONTACT, AND SUPABASE VERIFICATION CHECKS PASSED.")
            sys.exit(0)

    def test_brand_identity_and_removal_of_placeholders(self):
        print("\n--> 1. Client Brand Name & Zero Customer-facing Placeholder Checks")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        # Must have zero customer-facing "Maison Aurum" in index.html
        maison_matches = re.findall(r"Maison\s+Aurum", html, re.IGNORECASE)
        self.assert_true(len(maison_matches) == 0, "Zero customer-facing 'Maison Aurum' in index.html", f"Found {len(maison_matches)} matches")

        # Must contain actual client name variants
        self.assert_true("Kashinathsa Y. Khatawate" in html or "K.Y. Khatawate" in html, "Client brand name in index.html")
        self.assert_true("1937" in html, "Heritage year '1937' in index.html")
        self.assert_true("Gadag" in html, "Store location 'Gadag' in index.html")

        # Check centralized brand config
        self.assert_true(os.path.exists(BRAND_JS_PATH), "js/config/brand.js exists")
        with open(BRAND_JS_PATH, "r", encoding="utf-8") as f:
            brand_js = f.read()
        self.assert_true("Kashinathsa Y. Khatawate Jewellers" in brand_js, "Official storeName in brand.js")
        self.assert_true("KYK" in brand_js, "Monogram KYK in brand.js")

    def test_logo_and_instagram_qr_assets(self):
        print("\n--> 2. Logo & Instagram QR Asset Integrity")
        logo_path = os.path.join(WORKSPACE, "assets", "branding", "IMG_0941.PNG")
        qr_path = os.path.join(WORKSPACE, "assets", "branding", "IMG_0942.JPG.jpeg")

        self.assert_true(os.path.exists(logo_path), "Client logo file exists on disk (IMG_0941.PNG)")
        self.assert_true(os.path.exists(qr_path), "Instagram QR file exists on disk (IMG_0942.JPG.jpeg)")

        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        self.assert_true("assets/branding/IMG_0941.PNG" in html, "Original logo IMG_0941.PNG referenced in index.html")
        self.assert_true("assets/branding/IMG_0942.JPG.jpeg" in html, "Original QR IMG_0942.JPG.jpeg referenced in index.html")

    def test_contact_names_phone_and_whatsapp_urls(self):
        print("\n--> 3. Verified Contacts, Phone Links & WhatsApp Actions")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        # Contact names
        self.assert_true("Venkatesh" in html, "Contact name 'Venkatesh' in index.html")
        self.assert_true("Prajwal" in html, "Contact name 'Prajwal' in index.html")

        # Verified phone numbers
        self.assert_true("94487 53791" in html or "9448753791" in html, "Phone 9448753791 in index.html")
        self.assert_true("91489 96998" in html or "9148996998" in html, "Phone 9148996998 in index.html")

        # tel: links
        self.assert_true('href="tel:+919448753791"' in html, "Clickable tel:+919448753791 present")
        self.assert_true('href="tel:+919148996998"' in html, "Clickable tel:+919148996998 present")

        # WhatsApp links: must use international digits only, no +, no spaces
        self.assert_true('href="https://wa.me/919448753791"' in html, "Clickable https://wa.me/919448753791 present")
        self.assert_true('href="https://wa.me/919148996998"' in html, "Clickable https://wa.me/919148996998 present")

        # Instagram URL
        self.assert_true("https://www.instagram.com/k.y.khatawate_jewellers_gadag/" in html, "Official Instagram profile link present")

    def test_metadata_and_favicon(self):
        print("\n--> 4. Metadata, Favicon, Open Graph & Twitter Cards")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        # Favicon
        self.assert_true('rel="icon"' in html and 'assets/branding/IMG_0941.PNG' in html, "Favicon link using client logo in index.html")

        # Title
        self.assert_true("<title>Kashinathsa Y. Khatawate Jewellers" in html, "Client brand name in browser <title>")

        # Meta description
        self.assert_true('name="description"' in html and 'Khatawate' in html, "Client brand in meta description")

        # Open Graph
        self.assert_true('property="og:site_name"' in html, "og:site_name present")
        self.assert_true('property="og:image"' in html, "og:image present")

        # Twitter Card
        self.assert_true('name="twitter:card"' in html, "twitter:card present")

    def test_supabase_schema_and_rls(self):
        print("\n--> 5. Supabase SQL Schema & Row Level Security (RLS)")
        self.assert_true(os.path.exists(SUPABASE_SQL_PATH), "SQL migration file exists")

        with open(SUPABASE_SQL_PATH, "r", encoding="utf-8") as f:
            sql = f.read()

        # Required fields
        required_fields = ["id", "created_at", "customer_name", "email", "phone", "product_id", "product_name", "message", "status"]
        for field in required_fields:
            self.assert_true(field in sql, f"SQL table defines '{field}' column")

        # RLS Enabled
        self.assert_true("ENABLE ROW LEVEL SECURITY" in sql, "Row Level Security explicitly enabled in SQL")

        # Public INSERT only policy
        self.assert_true("FOR INSERT" in sql and "anon" in sql, "Public INSERT policy defined")

    def test_edge_function_security_and_email(self):
        print("\n--> 6. Supabase Edge Function & Resend Email Integration")
        self.assert_true(os.path.exists(EDGE_FUNC_PATH), "Edge Function submit-inquiry/index.ts exists")

        with open(EDGE_FUNC_PATH, "r", encoding="utf-8") as f:
            fn = f.read()

        self.assert_true("honeypot" in fn, "Bot honeypot spam protection present")
        self.assert_true("RESEND_API_KEY" in fn, "Resend API key integration present")
        self.assert_true("notification_status" in fn, "notification_status tracking present")
        self.assert_true("unconfigured" in fn, "Graceful unconfigured email fallback present")

    def test_inquiry_service_and_modal(self):
        print("\n--> 7. Inquiry Service & InquiryModal UI Component")
        self.assert_true(os.path.exists(INQUIRY_SERVICE_PATH), "js/services/inquiryService.js exists")
        self.assert_true(os.path.exists(INQUIRY_MODAL_PATH), "js/components/InquiryModal.js exists")

        with open(INQUIRY_MODAL_PATH, "r", encoding="utf-8") as f:
            modal_code = f.read()

        self.assert_true("inquiry-customer-name" in modal_code, "Customer name input in modal")
        self.assert_true("inquiry-email" in modal_code, "Email input in modal")
        self.assert_true("inquiry-phone" in modal_code, "Mandatory phone input in modal")
        self.assert_true("inquiry-message" in modal_code, "Message input in modal")
        self.assert_true("inquiry_type: 'individual_product'" in modal_code, "Inquiry modal specifies individual_product type")
        self.assert_true("btn-transmit-inquiry" in modal_code, "Submit button in modal")
        self.assert_true("inquiry-success-dialog" in modal_code, "Success confirmation state in modal")

        with open(INQUIRY_SERVICE_PATH, "r", encoding="utf-8") as f:
            svc_code = f.read()
        self.assert_true("phoneRegex" in svc_code, "Phone regex validation in inquiryService.js")
        self.assert_true("viewing_appointment" in svc_code, "Viewing appointment support in inquiryService.js")

    def test_viewing_drawer_multi_piece_flow(self):
        print("\n--> 8. Private Viewing Drawer Multi-Piece Consultation Flow")
        drawer_path = os.path.join(WORKSPACE, "js", "components", "ViewingDrawer.js")
        self.assert_true(os.path.exists(drawer_path), "js/components/ViewingDrawer.js exists")

        with open(drawer_path, "r", encoding="utf-8") as f:
            drawer_code = f.read()

        self.assert_true("viewing-name" in drawer_code, "Client name input in ViewingDrawer")
        self.assert_true("viewing-email" in drawer_code, "Client email input in ViewingDrawer")
        self.assert_true("viewing-phone" in drawer_code, "Mandatory phone input in ViewingDrawer")
        self.assert_true("viewing-location" in drawer_code, "Consultation location selector in ViewingDrawer")
        self.assert_true("viewing_appointment" in drawer_code, "ViewingDrawer submits with inquiry_type viewing_appointment")
        self.assert_true("selected_products" in drawer_code, "ViewingDrawer captures selected_products array")
        self.assert_true("viewing-success-pane" in drawer_code, "ViewingDrawer has dedicated luxury confirmation state")

    def test_silver_catalogue_integration(self):
        print("\n--> 9. Genuine Silver Jewellery Catalogue Integration")
        products_json_path = os.path.join(WORKSPACE, "data", "products.json")
        products_js_path = os.path.join(WORKSPACE, "js", "data", "products.js")

        self.assert_true(os.path.exists(products_json_path), "data/products.json exists")
        self.assert_true(os.path.exists(products_js_path), "js/data/products.js exists")

        with open(products_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assert_true("silver_products" in data, "silver_products array present in products.json")
        silver_items = data.get("silver_products", [])
        self.assert_true(len(silver_items) == 2, f"Exactly 2 silver items present (found {len(silver_items)})")

        silver_ids = [p["id"] for p in silver_items]
        self.assert_true("SILV-001" in silver_ids, "SILV-001 present in silver_products")
        self.assert_true("SILV-002" in silver_ids, "SILV-002 present in silver_products")

        # Verify raw images for silver products exist on disk
        silv1_path = os.path.join(WORKSPACE, "assets", "raw-jewellery", "extracted", "08_Dark_or_Unclear_Review", "IMG_0231.jpg")
        silv2_path = os.path.join(WORKSPACE, "assets", "raw-jewellery", "extracted", "09_Fastening_or_Extra_View", "IMG_0839.JPG.jpeg")
        self.assert_true(os.path.exists(silv1_path), "SILV-001 raw master photo IMG_0231.jpg exists on disk")
        self.assert_true(os.path.exists(silv2_path), "SILV-002 raw master photo IMG_0839.JPG.jpeg exists on disk")

        # Verify 5 Gold products are preserved intact
        gold_items = data.get("products", [])
        self.assert_true(len(gold_items) == 5, f"Original 5 Gold products preserved intact (found {len(gold_items)})")

    def test_product_asset_and_design_preservation(self):
        print("\n--> 8. Design & Raw Product Photograph Preservation")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        # Confirm all 5 approved raw photographs are retained
        self.assert_true("assets/raw-jewellery/extracted/01_Earrings_Set_1_0423/IMG_0428.JPG.jpeg" in html, "PROD-001 raw photo preserved")
        self.assert_true("assets/raw-jewellery/extracted/03_Necklace_IMG_0062/IMG_0062.JPG.jpeg" in html, "PROD-003 raw photo preserved")
        self.assert_true("assets/raw-jewellery/extracted/04_Long_Necklace_IMG_0143/IMG_0143.PNG" in html, "PROD-004 raw photo preserved")
        self.assert_true("assets/raw-jewellery/extracted/07_Fabric_Background_Reference/IMG_0037.jpg" in html, "PROD-007A raw photo preserved")
        self.assert_true("assets/raw-jewellery/extracted/07_Fabric_Background_Reference/IMG_0041.jpg" in html, "PROD-007B raw photo preserved")

        # Zero quarantined products
        for q in ["prod-002", "product-002", "prod-005", "product-005", "prod-006", "product-006"]:
            self.assert_true(q not in html.lower(), f"Zero quarantined {q} in index.html")

if __name__ == "__main__":
    test_suite = TestBrandingAndInquiry()
    test_suite.run_all()
