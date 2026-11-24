"""
Netlify Direct Production Deployer for KYK Jewellers Storefront
Uses the Netlify REST API to deploy the storefront directly without heavy CLI dependencies.
Requires NETLIFY_AUTH_TOKEN in environment or passed as argument.
"""

import os
import sys
import zipfile
import json
import urllib.request
import urllib.error
from pathlib import Path

SITE_NAME = "kyk-jewellers-gadag"
ROOT_DIR = Path(".")
DIST_ZIP = Path("reports/kyk_storefront_production.zip")

EXCLUDE_DIRS = {
    ".git", ".gemini", "tests", "scripts", "reports", 
    "processed-jewellery", "processed-jewellery-v2"
}
EXCLUDE_FILES = {
    "processed-jewellery-v2.zip", "received_photos.zip", ".env", ".env.local"
}

def create_production_bundle():
    """Package only clean live storefront files into a zip archive."""
    print("Packaging production assets for KYK Jewellers...")
    DIST_ZIP.parent.mkdir(parents=True, exist_ok=True)
    
    file_count = 0
    total_uncompressed_bytes = 0
    
    with zipfile.ZipFile(DIST_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(ROOT_DIR):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
            
            for f in files:
                if f in EXCLUDE_FILES or f.endswith((".log", ".tmp")):
                    continue
                if f == "received_photos.zip":
                    continue
                    
                fp = Path(root) / f
                arcname = fp.relative_to(ROOT_DIR).as_posix()
                
                # Exclude the zip itself if in root
                if fp.resolve() == DIST_ZIP.resolve():
                    continue
                    
                zf.write(fp, arcname)
                file_count += 1
                total_uncompressed_bytes += fp.stat().st_size
                
    zip_size_mb = DIST_ZIP.stat().st_size / (1024 * 1024)
    print(f"Production bundle created: {DIST_ZIP}")
    print(f"  Files included: {file_count}")
    print(f"  Uncompressed: {total_uncompressed_bytes / (1024*1024):.2f} MB")
    print(f"  Compressed zip: {zip_size_mb:.2f} MB")
    return DIST_ZIP

def deploy_to_netlify(token, custom_name=None):
    """Deploy the packaged zip bundle to Netlify via REST API."""
    if not token:
        print("ERROR: Netlify Auth Token is missing.")
        return False
        
    site_name = custom_name or SITE_NAME
    bundle_path = create_production_bundle()
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/zip"
    }
    
    # 1. Check if site already exists under user's Netlify account
    list_url = "https://api.netlify.com/api/v1/sites"
    req = urllib.request.Request(list_url, headers={"Authorization": f"Bearer {token}"})
    
    site_id = None
    try:
        with urllib.request.urlopen(req) as resp:
            sites = json.loads(resp.read().decode("utf-8"))
            for s in sites:
                if s.get("name") == site_name:
                    site_id = s.get("id")
                    print(f"Found existing Netlify site '{site_name}' (ID: {site_id})")
                    break
    except urllib.error.HTTPError as e:
        print(f"Failed to query existing Netlify sites: HTTP {e.code} {e.reason}")
        if e.code == 401:
            print("Authentication failed: Your Netlify token is invalid or expired.")
            return False
            
    # 2. If site doesn't exist, create it
    if not site_id:
        print(f"Creating new Netlify site: {site_name}...")
        create_url = "https://api.netlify.com/api/v1/sites"
        create_payload = json.dumps({"name": site_name}).encode("utf-8")
        create_req = urllib.request.Request(
            create_url,
            data=create_payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        try:
            with urllib.request.urlopen(create_req) as resp:
                site_data = json.loads(resp.read().decode("utf-8"))
                site_id = site_data.get("id")
                print(f"Successfully created site '{site_name}' (ID: {site_id})")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            # If name is taken, retry with randomized suffix
            if e.code in (422, 400) and "already been taken" in err_body:
                import random
                rand_suffix = random.randint(100, 999)
                site_name = f"{site_name}-{rand_suffix}"
                print(f"Name taken, retrying with '{site_name}'...")
                create_payload = json.dumps({"name": site_name}).encode("utf-8")
                create_req = urllib.request.Request(
                    create_url,
                    data=create_payload,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                )
                with urllib.request.urlopen(create_req) as resp:
                    site_data = json.loads(resp.read().decode("utf-8"))
                    site_id = site_data.get("id")
                    print(f"Successfully created site '{site_name}' (ID: {site_id})")
            else:
                print(f"Failed to create site: HTTP {e.code} - {err_body}")
                return False

    # 3. Deploy the zip archive to the site
    deploy_url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
    print(f"Uploading production bundle to Netlify site ({site_id})...")
    
    with open(bundle_path, "rb") as zf:
        zip_data = zf.read()
        
    deploy_req = urllib.request.Request(
        deploy_url,
        data=zip_data,
        headers=headers
    )
    
    try:
        with urllib.request.urlopen(deploy_req) as resp:
            deploy_data = json.loads(resp.read().decode("utf-8"))
            live_url = deploy_data.get("ssl_url") or deploy_data.get("url")
            print("=" * 60)
            print(f"NETLIFY DEPLOYMENT SUCCESSFUL!")
            print(f"Live URL: {live_url}")
            print(f"Deploy ID: {deploy_data.get('id')}")
            print(f"State: {deploy_data.get('state')}")
            print("=" * 60)
            return live_url
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        print(f"Netlify deploy upload failed: HTTP {e.code} - {err_body}")
        return False

if __name__ == "__main__":
    token = os.environ.get("NETLIFY_AUTH_TOKEN") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not token:
        # Just create the bundle to test packaging
        create_production_bundle()
    else:
        deploy_to_netlify(token)
