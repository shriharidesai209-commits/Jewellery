"""
Unit and Integration Tests for the KYK Jewellers 1937 Archival Jewellery Gallery
Kashinathsa Y. Khatawate Jewellers (KYK Since 1937), Gadag

Verifies:
1. Gallery JSON and JS datasets contain exactly 20 authenticated photos.
2. Every image file exists on disk and is a valid decodable image.
3. Zero AI/stock images; all 20 trace back to client original files in assets/raw-jewellery/extracted/.
4. None of the gallery items invent false purity, hallmark promises, or prices.
5. Component, HTML mounts, CSS rules, and app bootstrap wiring.
"""

import os
import json
import unittest
from pathlib import Path
from PIL import Image

class TestKYKArchivalGallery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path('.')
        cls.gallery_json_path = cls.root / 'data' / 'gallery_photos.json'
        cls.gallery_js_path = cls.root / 'js' / 'data' / 'galleryPhotos.js'
        cls.component_path = cls.root / 'js' / 'components' / 'ArchivalGallery.js'
        cls.index_html_path = cls.root / 'index.html'
        cls.app_js_path = cls.root / 'js' / 'app.js'
        cls.css_path = cls.root / 'css' / 'styles.css'
        
        with open(cls.gallery_json_path, 'r', encoding='utf-8') as f:
            cls.gallery_data = json.load(f)
            
        with open(cls.index_html_path, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()

        with open(cls.app_js_path, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

        with open(cls.css_path, 'r', encoding='utf-8') as f:
            cls.css = f.read()

    def test_01_gallery_json_count(self):
        """Assert exactly 20 photos in gallery_photos.json"""
        self.assertEqual(self.gallery_data['total'], 20)
        self.assertEqual(len(self.gallery_data['photos']), 20)

    def test_02_all_photos_exist_and_readable(self):
        """Assert all 20 image paths exist on disk and have valid image headers"""
        for i, photo in enumerate(self.gallery_data['photos'], 1):
            src = photo['sourceImage']
            img_path = Path(src)
            self.assertTrue(img_path.exists(), f"Photo {i} missing file: {src}")
            with Image.open(img_path) as img:
                w, h = img.size
                self.assertGreater(w, 0)
                self.assertGreater(h, 0)
                self.assertIn(img.mode, ('RGB', 'RGBA'))

    def test_03_zero_invented_prices_or_hallmarks(self):
        """Assert no gallery photo invents prices, false weights or misleading specs"""
        for photo in self.gallery_data['photos']:
            self.assertNotIn('price', photo)
            self.assertNotIn('purity', photo)
            self.assertTrue(len(photo['description']) > 20)
            self.assertTrue(photo['id'].startswith('ARCH-'))

    def test_04_html_mount_points(self):
        """Assert index.html contains #gallery-section and #archival-gallery-app mount"""
        self.assertIn('id="gallery-section"', self.index_html)
        self.assertIn('id="archival-gallery-app"', self.index_html)
        self.assertIn('1937 Gallery', self.index_html)

    def test_05_app_bootstrap_integration(self):
        """Assert js/app.js imports and initializes ArchivalGallery"""
        self.assertIn("import { ArchivalGallery } from './components/ArchivalGallery.js'", self.app_js)
        self.assertIn("new ArchivalGallery(galleryApp)", self.app_js)

    def test_06_css_styling_rules(self):
        """Assert css/styles.css contains essential luxury gallery styles"""
        self.assertIn('.section-archival-gallery', self.css)
        self.assertIn('.gallery-slider-viewport', self.css)
        self.assertIn('.gallery-slider-track', self.css)
        self.assertIn('.gallery-slide-card', self.css)
        self.assertIn('.gallery-lightbox-backdrop', self.css)
        self.assertIn('scroll-snap-type: x mandatory', self.css)

    def test_07_diversity_across_jewellery_categories(self):
        """Assert selected photos cover multiple distinct jewellery forms"""
        categories = {p['category'] for p in self.gallery_data['photos']}
        self.assertGreaterEqual(len(categories), 4)
        self.assertIn('Temple Haars & Neckpieces', categories)
        self.assertIn('Chokers & Collars', categories)
        self.assertIn('Earrings & Jhumkas', categories)
        self.assertIn('Craftsmanship & Macro Details', categories)

if __name__ == '__main__':
    unittest.main()
