#!/usr/bin/env python3
"""
Catalogue Foundation & Product Integration Test Suite
Validates the Stage 1 build deliverables against all strict safety and architecture constraints.
"""

import os
import sys
import json
import re

WORKSPACE = r"d:\Jewellery"
JSON_PATH = os.path.join(WORKSPACE, "data", "products.json")
JS_DATA_PATH = os.path.join(WORKSPACE, "js", "data", "products.js")

class TestCatalogueIntegration:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.products = []

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
        print("STAGE 1: VERIFIED PRODUCT INTEGRATION & CATALOGUE TEST SUITE")
        print("================================================================================")
        
        self.test_catalogue_json_structure()
        self.test_approved_products_count_and_identities()
        self.test_zero_v1_assets()
        self.test_zero_quarantined_products()
        self.test_physical_assets_exist()
        self.test_price_integrity()
        self.test_reusable_components_exist()
        self.test_js_data_sync()
        
        print("================================================================================")
        print(f"RESULTS: {self.passed} Passed, {self.failed} Failed")
        print("================================================================================")
        
        if self.failed > 0:
            print("\nErrors encountered:")
            for e in self.errors:
                print(e)
            sys.exit(1)
        else:
            print("\nALL VERIFICATION AND QUALITY CHECKS PASSED SUCCESSFULLY (STAGE 1 COMPLETE).")
            sys.exit(0)

    def test_catalogue_json_structure(self):
        print("\n--> Test Suite 1: Catalogue JSON Structure & Metadata")
        self.assert_true(os.path.exists(JSON_PATH), "data/products.json exists physically")
        
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.assert_true(data.get("title") == "JewelleryCatalogue", "Schema title is JewelleryCatalogue")
        self.assert_true("products" in data and isinstance(data["products"], list), "Catalogue contains 'products' array")
        self.products = data.get("products", [])

    def test_approved_products_count_and_identities(self):
        print("\n--> Test Suite 2: Approved Product Identities & Integrity")
        self.assert_true(len(self.products) == 5, "Strictly 5 approved products in catalogue", f"Found {len(self.products)}")
        
        approved_ids = {"PROD-001", "PROD-003", "PROD-004", "PROD-007A", "PROD-007B"}
        found_ids = {p.get("id") for p in self.products}
        self.assert_true(approved_ids == found_ids, "Exactly approved product IDs present", f"Found: {found_ids}")
        
        for p in self.products:
            pid = p.get("id")
            self.assert_true(bool(p.get("name")), f"{pid} has non-empty name")
            self.assert_true(bool(p.get("category")), f"{pid} has category ({p.get('category')})")
            self.assert_true(bool(p.get("shortDescription")), f"{pid} has shortDescription")
            self.assert_true(bool(p.get("fullDescription")), f"{pid} has fullDescription")
            self.assert_true(p.get("auditStatus") == "VERIFIED_PASS", f"{pid} has auditStatus VERIFIED_PASS")

    def test_zero_v1_assets(self):
        print("\n--> Test Suite 3: Zero V1 Asset Leakage Check (Strict Rule)")
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            raw_json = f.read()
            
        # Match 'processed-jewellery/' NOT followed by '-v2'
        v1_matches = re.findall(r"processed-jewellery/(?!v2)", raw_json)
        self.assert_true(len(v1_matches) == 0, "Zero references to legacy V1 assets ('processed-jewellery/') in catalogue", f"Matches: {v1_matches}")
        
        # Check that all image paths explicitly start with assets/raw-jewellery/extracted/
        for p in self.products:
            pid = p.get("id")
            images = p.get("images", {})
            for role, img_obj in images.items():
                for fmt in ["webp", "jpg", "png"]:
                    if fmt in img_obj and img_obj[fmt]:
                        path_str = img_obj[fmt]
                        self.assert_true(path_str.startswith("assets/raw-jewellery/extracted/"), 
                                         f"{pid} image [{role}].{fmt} is strictly from assets/raw-jewellery/extracted/")

    def test_zero_quarantined_products(self):
        print("\n--> Test Suite 4: Zero Quarantined Products Check (Strict Rule)")
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            raw_json = f.read().lower()
            
        self.assert_true("product-002" not in raw_json and "prod-002" not in raw_json, "Product 002 (Quarantined Tag) is NOT present in catalogue")
        self.assert_true("product-005" not in raw_json and "prov-tray" not in raw_json, "Product 005 (Provisional Tray) is NOT present in catalogue")
        self.assert_true("product-006" not in raw_json and "prov-neck" not in raw_json, "Product 006 (Provisional Split Necklaces) is NOT present in catalogue")

    def test_physical_assets_exist(self):
        print("\n--> Test Suite 5: Physical Asset Existence on Disk")
        for p in self.products:
            pid = p.get("id")
            images = p.get("images", {})
            for role in ["listing", "gallery", "featured", "detail", "master"]:
                self.assert_true(role in images, f"{pid} has '{role}' image configuration")
                img_obj = images.get(role, {})
                for fmt in ["webp", "jpg", "png"]:
                    if fmt in img_obj and img_obj[fmt]:
                        rel_path = img_obj[fmt]
                        abs_path = os.path.join(WORKSPACE, rel_path.replace("/", "\\"))
                        exists = os.path.exists(abs_path)
                        size = os.path.getsize(abs_path) if exists else 0
                        self.assert_true(exists and size > 0, 
                                         f"{pid} [{role}].{fmt} exists on disk ({size:,} bytes)",
                                         f"Path not found: {abs_path}")

    def test_price_integrity(self):
        print("\n--> Test Suite 6: Price & Specification Integrity (Constraint Rule)")
        for p in self.products:
            pid = p.get("id")
            # Must not invent arbitrary prices
            self.assert_true(p.get("price") is None, f"{pid} price field is null (no arbitrary prices invented)")
            self.assert_true(p.get("priceDisplay") == "Price Upon Request", f"{pid} priceDisplay is 'Price Upon Request'")

    def test_reusable_components_exist(self):
        print("\n--> Test Suite 7: Reusable Components & Architecture")
        components = [
            ("js/components/ProductImage.js", "ProductImage component"),
            ("js/components/ProductCard.js", "ProductCard component"),
            ("js/components/ProductGrid.js", "ProductGrid component"),
            ("js/components/ProductModal.js", "ProductModal component"),
            ("js/services/productService.js", "ProductService catalogue service"),
            ("js/app.js", "Main application script"),
            ("css/styles.css", "Design system stylesheet"),
            ("index.html", "Main catalogue presentation page")
        ]
        for rel_path, name in components:
            abs_p = os.path.join(WORKSPACE, rel_path.replace("/", "\\"))
            self.assert_true(os.path.exists(abs_p) and os.path.getsize(abs_p) > 0, f"{name} exists at {rel_path}")

    def test_js_data_sync(self):
        print("\n--> Test Suite 8: ES Module Data Synchronization")
        self.assert_true(os.path.exists(JS_DATA_PATH), "js/data/products.js exists")
        with open(JS_DATA_PATH, "r", encoding="utf-8") as f:
            js_content = f.read()
        for p in self.products:
            pid = p.get("id")
            self.assert_true(pid in js_content, f"Product {pid} is defined in js/data/products.js")

if __name__ == "__main__":
    tester = TestCatalogueIntegration()
    tester.run_all()
