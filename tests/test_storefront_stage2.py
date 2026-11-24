#!/usr/bin/env python3
"""
Stage 2 Luxury Storefront Validation Test Suite
Validates the complete storefront architecture, navigation, hero, spotlight,
collections, philosophy, craftsmanship, search, and viewing drawer.
"""

import os
import sys
import re

WORKSPACE = r"d:\Jewellery"
INDEX_PATH = os.path.join(WORKSPACE, "index.html")
CSS_PATH = os.path.join(WORKSPACE, "css", "styles.css")
APP_JS_PATH = os.path.join(WORKSPACE, "js", "app.js")

class TestStorefrontStage2:
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
        print("STAGE 2: LUXURY STOREFRONT EXPERIENCE VALIDATION SUITE")
        print("================================================================================")

        self.test_html_structure_and_sections()
        self.test_navigation_and_modals()
        self.test_zero_v1_and_quarantined()
        self.test_image_paths_exist()
        self.test_css_luxury_design_tokens()
        self.test_js_component_integration()

        print("================================================================================")
        print(f"STAGE 2 RESULTS: {self.passed} Passed, {self.failed} Failed")
        print("================================================================================")

        if self.failed > 0:
            print("\nErrors encountered:")
            for e in self.errors:
                print(e)
            sys.exit(1)
        else:
            print("\nALL STAGE 2 STOREFRONT CHECKS PASSED SUCCESSFULLY.")
            sys.exit(0)

    def test_html_structure_and_sections(self):
        print("\n--> Test Suite 1: Homepage Structural Sections in index.html")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        sections = [
            ("site-header", "Navigation Header"),
            ("top-announcement-bar", "Top Announcement Ticker"),
            ("hero-storefront", "Hero Storefront Section"),
            ("section-spotlight", "Curated Highlights Spotlight"),
            ("section-collections", "Collection Discovery Section"),
            ("section-philosophy", "Brand Philosophy Section"),
            ("section-craftsmanship", "Atelier Craftsmanship Section"),
            ("section-vault", "Catalogue Vault Grid Mount Section"),
            ("section-salon-banner", "Salon Appointment CTA Banner"),
            ("site-footer", "Multi-Column Footer")
        ]
        for class_name, desc in sections:
            self.assert_true(class_name in html, f"Section '{desc}' (class: {class_name}) present in index.html")

    def test_navigation_and_modals(self):
        print("\n--> Test Suite 2: Navigation & Interaction Entry Points")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        elements = [
            ('data-action="open-search"', "Search modal trigger"),
            ('data-action="open-viewing-drawer"', "Private viewing drawer trigger"),
            ('id="btn-mobile-menu"', "Mobile hamburger toggle"),
            ('id="mobile-nav-drawer"', "Mobile slide-out drawer"),
            ('id="viewing-badge-count"', "Viewing list counter badge"),
            ('data-collection-filter="Earrings"', "Earrings collection filter trigger"),
            ('data-collection-filter="Necklaces & Chokers"', "Necklaces/Chokers filter trigger"),
            ('id="catalogue-app"', "Catalogue grid mount point")
        ]
        for selector, desc in elements:
            self.assert_true(selector in html, f"{desc} ({selector}) present")

    def test_zero_v1_and_quarantined(self):
        print("\n--> Test Suite 3: Strict Safety Rules (Zero V1 / Zero Quarantined)")
        files_to_check = [INDEX_PATH, CSS_PATH, APP_JS_PATH,
                          os.path.join(WORKSPACE, "js", "components", "ViewingDrawer.js"),
                          os.path.join(WORKSPACE, "js", "components", "SearchModal.js"),
                          os.path.join(WORKSPACE, "js", "components", "ProductModal.js")]

        for path in files_to_check:
            fname = os.path.basename(path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            v1_leak = re.findall(r"processed-jewellery/(?!v2)", content)
            self.assert_true(len(v1_leak) == 0, f"Zero V1 references in {fname}", f"Found: {v1_leak}")

            for q in ["prod-002", "product-002", "prod-005", "product-005", "prod-006", "product-006"]:
                self.assert_true(q not in content.lower(), f"Zero quarantined {q} in {fname}")

    def test_image_paths_exist(self):
        print("\n--> Test Suite 4: Static Image Assets in index.html")
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        # Find all src / srcset referencing raw original assets
        img_refs = re.findall(r'(?:src|srcset)="([^"]+)"', html)
        raw_refs = [r for r in img_refs if "assets/raw-jewellery/extracted" in r]
        self.assert_true(len(raw_refs) > 0, f"Found {len(raw_refs)} raw original image references in index.html")

        for ref in raw_refs:
            abs_p = os.path.join(WORKSPACE, ref.replace("/", "\\"))
            exists = os.path.exists(abs_p)
            size = os.path.getsize(abs_p) if exists else 0
            self.assert_true(exists and size > 0, f"Referenced image exists: {ref} ({size:,} bytes)")

    def test_css_luxury_design_tokens(self):
        print("\n--> Test Suite 5: CSS Luxury Design System Tokens")
        with open(CSS_PATH, "r", encoding="utf-8") as f:
            css = f.read()

        tokens = [
            ("--bg-primary: #F9F7F2", "Warm ivory background (#F9F7F2)"),
            ("--gold-primary: #997D3D", "Antique gold primary accent (#997D3D)"),
            ("Cormorant Garamond", "Cormorant Garamond luxury serif typography"),
            ("Inter", "Inter clean sans typography"),
            (".hero-storefront", "Hero storefront styling"),
            (".viewing-drawer", "Viewing drawer styling"),
            (".search-dialog", "Search dialog styling"),
            (".modal-dialog", "Modal dialog styling"),
            ("@media (max-width: 768px)", "Mobile responsive media queries")
        ]
        for token, desc in tokens:
            self.assert_true(token in css, f"CSS token '{desc}' present")

    def test_js_component_integration(self):
        print("\n--> Test Suite 6: Component Modularity & Service Decoupling")
        modules = [
            ("ViewingDrawer.js", "ViewingDrawer component"),
            ("SearchModal.js", "SearchModal component"),
            ("ProductModal.js", "ProductModal component"),
            ("ProductGrid.js", "ProductGrid component"),
            ("ProductCard.js", "ProductCard component"),
            ("ProductImage.js", "ProductImage component"),
            ("productService.js", "ProductService business logic")
        ]
        for fname, desc in modules:
            p = os.path.join(WORKSPACE, "js", "components" if "Modal" in fname or "Card" in fname or "Grid" in fname or "Image" in fname or "Drawer" in fname else "services", fname)
            self.assert_true(os.path.exists(p) and os.path.getsize(p) > 0, f"{desc} module exists")

if __name__ == "__main__":
    tester = TestStorefrontStage2()
    tester.run_all()
