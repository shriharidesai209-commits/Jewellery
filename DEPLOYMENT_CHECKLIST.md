# KYK JEWELLERS — PRODUCTION DEPLOYMENT CHECKLIST & READINESS AUDIT
**Kashinathsa Y. Khatawate Jewellers (KYK Since 1937), Gadag, Karnataka**  
**Version:** 2.0.0 (Stage 2 Production Ready)  
**Status:** FULLY AUDITED & PREPARED (DO NOT DEPLOY WITHOUT EXPLICIT CLIENT APPROVAL)

---

## 1. Executive Summary & Architecture Overview

The storefront for **Kashinathsa Y. Khatawate Jewellers** has been architected as an ultra-high performance, zero-bloat static web application powered by modern vanilla ES6 modules and a decoupled Supabase backend.

| Layer | Technology | Details |
|---|---|---|
| **Frontend Runtime** | Pure Vanilla HTML5 / Modern CSS3 / ES6 Modules | Zero build step required; instant HTTP serving |
| **Asset Pipeline** | 100% Authentic Client Photography | 7 Verified Catalogue Pieces + 20 Archival Gallery Pieces |
| **Design System** | Haute Joaillerie Luxury Styling | Warm Ivory (`#F9F7F2`), Antique Gold (`#997D3D`), Cormorant Garamond serif |
| **Backend & DB** | Supabase Postgres with Row Level Security (RLS) | Table `public.inquiries`, automated audit timestamps |
| **Serverless Logic** | Supabase Edge Function (`submit-inquiry`) | Deno TypeScript runtime, bot honeypot, CORS protection |
| **Email Dispatch** | Resend API Integration | Beautiful HTML email templates for instant merchant alerts |
| **Direct Contact** | Click-to-Call & WhatsApp Escalation | Direct routing to proprietors Venkatesh & Prajwal |

---

## 2. Pre-Flight Asset & Code Integrity Audit

### A. Original Photography Fidelity (Zero AI / Zero Stock)
- [x] **Catalogue Integrity:** All 7 verified pieces (5 Gold: `PROD-001`, `003`, `004`, `007A`, `007B` + 2 Silver: `SILV-001`, `SILV-002`) load directly from client originals.
- [x] **Archival Gallery (20 Photos):** 20 distinct, verified archival photographs loaded via `js/data/galleryPhotos.js` and `data/gallery_photos.json`.
- [x] **Zero Destructive Alterations:** Zero GrabCut segmentation, zero background removal, zero generative AI, zero cropping of subject.
- [x] **Contact Sheet Available:** Complete visual inspection contact sheet generated at `reports/gallery_selection_contact_sheet.html`.
- [x] **Decodability:** All candidate HEIC files converted to 100% full-resolution, lossless JPEGs alongside source files for cross-browser native rendering.

### B. Path Portability
- [x] **Zero Absolute Paths:** Complete scan across all HTML, JS, CSS, JSON, SQL, and TS files confirmed **0 hardcoded absolute paths** (no `d:\`, no `C:\`, no `localhost`).
- [x] **Relative Linking:** All assets referenced with portable relative paths (`assets/...`, `css/...`, `js/...`).

### C. Test Suite Verification
All 4 automated test suites run clean with 100% pass rate:
- `tests/test_archival_gallery.py`: **7/7 PASS**
- `tests/test_branding_and_inquiry.py`: **82/82 PASS**
- `tests/test_catalogue_integration.py`: **44/44 PASS**
- `tests/test_storefront_stage2.py`: **88/88 PASS**
- **Total Passing Assertions:** **221 Passed, 0 Failed, 0 Regressions**

---

## 3. Supabase Backend Deployment Instructions

### Step 1: Database Migration
Execute the migration script located at `supabase/migrations/20261124_create_inquiries_table.sql`:

```bash
# If using Supabase CLI:
supabase db push

# OR copy-paste the contents of:
# supabase/migrations/20261124_create_inquiries_table.sql
# directly into the SQL Editor of your Supabase Project Dashboard.
```

**Verification:**
1. Check that table `public.inquiries` is created.
2. Confirm RLS is enabled: `ALTER TABLE public.inquiries ENABLE ROW LEVEL SECURITY;`.
3. Confirm Policy `"Allow public anonymous inquiry submission"` allows `INSERT` for roles `anon, authenticated`.
4. Confirm `SELECT` and `UPDATE` are restricted to `authenticated` staff only.

### Step 2: Supabase Edge Function Deployment
Deploy the serverless Edge Function located at `supabase/functions/submit-inquiry/index.ts`:

```bash
# Deploy function without requiring JWT verification for public customer inquiries:
supabase functions deploy submit-inquiry --no-verify-jwt
```

### Step 3: Configure Supabase Secrets (Environment Variables)
Set the required secrets in your Supabase project:

```bash
# Set your Resend API Key for customer inquiry notifications:
supabase secrets set RESEND_API_KEY="re_your_api_key_here"

# (Optional) Set the merchant destination notification email:
supabase secrets set STORE_NOTIFICATION_EMAIL="contact@kykjewellers.com"
```

---

## 4. Client Frontend Configuration

Before pushing to production static hosting, update `js/config/supabase.js` with your live Supabase credentials:

```javascript
// File: js/config/supabase.js
export const SUPABASE_CONFIG = {
  // Replace with your actual project URL from Supabase Project Settings -> API
  url: 'https://YOUR_PROJECT_ID.supabase.co',
  
  // Replace with your public Anon Key (safe for browser exposure with RLS enabled)
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
  
  // Enable live Supabase submission in production
  useMockFallback: false,
  
  // Custom Edge Function URL (optional, defaults to `${url}/functions/v1/submit-inquiry`)
  edgeFunctionUrl: null
};
```

---

## 5. Static Hosting Deployment Options

Because the storefront consists of pure static assets with ES6 modules, it can be deployed to any modern static hosting provider in seconds:

### Option A: Cloudflare Pages (Recommended for Global Edge CDN & Speed)
```bash
# Install wrangler CLI if needed:
npm install -g wrangler

# Deploy current directory:
wrangler pages deploy . --project-name=kyk-jewellers
```

### Option B: Vercel
```bash
# Install vercel CLI if needed:
npm install -g vercel

# Deploy to production:
vercel --prod
```

### Option C: Netlify
```bash
# Deploy directory:
netlify deploy --prod --dir=.
```

### Option D: AWS S3 + CloudFront
```bash
# Sync files to S3 bucket:
aws s3 sync . s3://your-kyk-storefront-bucket/ --exclude ".git/*" --exclude "tests/*" --exclude "reports/*"
# Invalidate CloudFront cache:
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

---

## 6. Custom Domain & DNS Settings

| Record Type | Host | Points To / Value | TTL |
|---|---|---|---|
| **A** | `@` (apex) | IP provided by hosting provider (e.g., Cloudflare / Vercel) | Auto |
| **CNAME** | `www` | `your-site.pages.dev` or `cname.vercel-dns.com` | Auto |
| **CAA** | `@` | LetsEncrypt / DigiCert authorization | 3600 |

- Ensure **SSL/TLS encryption** is set to **Full (Strict)**.
- Enable HTTP to HTTPS automatic redirection.
- Set HTTP Security Headers:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: SAMEORIGIN`
  - `Referrer-Policy: strict-origin-when-cross-origin`

---

## 7. Post-Deployment Smoke Test Protocol

Once deployed to a staging or preview URL, verify the following 8 critical touchpoints:

1. **Brand Presentation:** Confirm the official store logo (`assets/branding/IMG_0941.PNG`) renders crisply in header, mobile nav, and footer.
2. **Hero & Collections:** Confirm `PROD-004` displays in the Hero card and all 4 Collection Discovery boxes filter the catalogue properly.
3. **1937 Archival Gallery:**
   - Confirm all 20 archival slides render their authentic client photographs without distortion.
   - Click Previous/Next arrows and test horizontal swipe on mobile.
   - Filter by categories: "Temple Haars", "Chokers", "Earrings", "Macro Details", "Sacred Heirlooms".
   - Click "Inspect Photo" to open the high-res Lightbox modal.
   - Verify Escape key and backdrop click close the Lightbox.
4. **Catalogue Vault (7 Masterpieces):**
   - Confirm 5 Gold pieces and 2 Silver pieces render with zero blank cards.
   - Click "Inspect Details" to view multi-angle viewports in the Product Modal.
5. **Private Viewing Drawer:**
   - Add multiple items to the viewing drawer.
   - Open drawer and confirm badge counter increments.
   - Fill in client appointment form and submit.
6. **Individual Product Inquiry Modal:**
   - Click "+ Inquire" on any card.
   - Confirm product image preview renders correctly.
   - Fill in contact details and submit.
7. **Direct Telephone & WhatsApp Escalation:**
   - Click "Call Venkatesh" (`tel:+919448753791`) on a mobile device.
   - Click "WhatsApp" (`https://wa.me/919448753791`) to verify pre-populated message.
   - Click "Call Prajwal" (`tel:+919148996998`) and test WhatsApp link.
8. **Owner Email Receipt:**
   - Check destination mailbox for Resend notification email with inquiry details.

---

*Prepared by Antigravity Autonomous Storefront Engineer for Kashinathsa Y. Khatawate Jewellers (KYK Since 1937).*
