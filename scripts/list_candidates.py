import sys, os
sys.path.insert(0, os.path.abspath('.'))
import scripts.generate_contact_sheet as gcs

records = gcs.audit_and_prepare_images()
available = [r for r in records if not r['is_catalogue']]
print(f"Total available candidates: {len(available)}")
for i, a in enumerate(available, 1):
    print(f"{i:2d}. [{a['folder']}] {a['browser_file']} ({a['width']}x{a['height']}) -> {a['full_rel_path']}")
