import os
from pathlib import Path

root_dir = Path(".")
ignored = {
    "processed-jewellery",
    "processed-jewellery-v2",
    "processed-jewellery-v2.zip",
    "received_photos.zip",
    "kyk_storefront_production.zip",
    ".git"
}

large_files = []
total_sz = 0
file_count = 0

for p in root_dir.rglob("*"):
    if not p.is_file():
        continue
    parts = p.parts
    if any(ig in parts for ig in ignored) or p.name in ignored:
        continue
    sz = p.stat().st_size
    total_sz += sz
    file_count += 1
    if sz > 25 * 1024 * 1024:
        large_files.append((str(p), sz))

print(f"Total commit files: {file_count}, Total size: {total_sz / (1024*1024):.2f} MB")
print("Files > 25MB:", large_files if large_files else "None!")
