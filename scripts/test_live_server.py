import urllib.request

endpoints = [
    'http://localhost:8088/',
    'http://localhost:8088/index.html',
    'http://localhost:8088/css/styles.css',
    'http://localhost:8088/js/app.js',
    'http://localhost:8088/js/components/ArchivalGallery.js',
    'http://localhost:8088/js/data/galleryPhotos.js',
    'http://localhost:8088/data/gallery_photos.json',
    'http://localhost:8088/reports/gallery_selection_contact_sheet.html',
    'http://localhost:8088/assets/raw-jewellery/extracted/08_Dark_or_Unclear_Review/IMG_0588.jpg',
    'http://localhost:8088/assets/raw-jewellery/extracted/08_Dark_or_Unclear_Review/IMG_0828.jpg',
    'http://localhost:8088/assets/raw-jewellery/extracted/06_Chain_or_Jewellery_on_Grey_0344/IMG_0344.jpg',
    'http://localhost:8088/assets/raw-jewellery/extracted/05_Ornate_Jewellery_Closeups_0300/IMG_0300.jpg',
    'http://localhost:8088/assets/raw-jewellery/extracted/01_Earrings_Set_1_0423/IMG_0431.JPG.jpeg'
]

print("Testing live HTTP server endpoints at http://localhost:8088/:")
for url in endpoints:
    with urllib.request.urlopen(url) as req:
        length = req.headers.get("Content-Length", "unknown")
        print(f"  {req.status} OK: {url} ({length} bytes)")
print("ALL LIVE ENDPOINTS RETURNED 200 OK!")
