# Complete Jewellery Image Inventory & Diversity Audit
**Maison Aurum — Archive Analysis & Catalogue Expansion Blueprint**  
**Date:** November 23, 2026  
**Status:** COMPLETE AUDIT

---

## 1. Executive Summary & Critical Findings

A forensic audit of the original archive (`received_photos.zip` / `assets/raw-jewellery/extracted`) and the current processed pipeline was conducted to address catalogue size limitations and genuine photographic diversity.

### The Three Critical Discoveries:

1. **The Single-Photo Dilemma in the Current Catalogue:**
   - **`PROD-003` (Royal Ruby Choker):** There is **only 1 original photograph** (`IMG_0062.JPG.jpeg`, 960×1280, 213 KB) in the entire archive. All 5 presentation angles currently in the storefront modal (`1:1 Studio Card`, `4:5 Portrait`, `16:9 Editorial`, `Macro Detail`, and `Master Cut`) are **digital aspect-ratio crops of this single image**.
   - **`PROD-004` (Temple Long Haar):** There is **only 1 original photograph** (`IMG_0143.PNG`, 1078×1441, 397 KB) in the entire archive. All catalogue views are derived from this single image.
   - **`PROD-007A` (Choker A):** 5 source files exist (`IMG_0034`..`0039`), but they represent burst shots of the same flatlay on red velvet from nearly identical top-down angles.
   - **`PROD-007B` (Choker B):** 5 source files exist (`IMG_0040`..`0044`), but they are burst shots from one flatlay angle (with `IMG_0044` severely motion-blurred).
   - **`PROD-001` (Drop Earrings):** 4 source files exist, but only **2 distinct views** exist: full hanging pair (`IMG_0428`/`0429`/`0431`) and isolated stud tops held on fingers (`IMG_0423`).

2. **The "Missing" Catalogue: 16+ Unintegrated Masterpieces Lie Dormant:**
   - The archive is **not** limited to 5 pieces. It contains photographs of at least **22 distinct physical jewellery creations**:
     - **3 Long Haars on presentation cards** (`IMG_0344`, `IMG_0345`, `IMG_0350`) — each with independent merchant weights (18.140g, 12.210g, 15.720g).
     - **5 Distinct Chokers on presentation cards** (`IMG_0351`, `IMG_0352`, `IMG_0353`, `IMG_0354`, `IMG_0355`) — each an independent design (10.160g, 16.240g, 9.250g, 10.070g, 11.410g).
     - **1 Grand Peacock Temple Haar** (`IMG_0588.HEIC`, 4284×5712, 4.86 MB) — an extraordinary, pristine 4-tier cascading haar with ruby/emerald peacock medallions, previously misclassified in `08_Dark_or_Unclear_Review`.
     - **1 Temple Lakshmi Pendant** (`IMG_0828.HEIC`, 3024×4032, 1.77 MB) — an ornate solid gold Lakshmi pendant with ruby and emerald cabochons.
     - **1 Additional Gold Choker** (`IMG_0235.HEIC`, 2268×4032, 1.4 MB) — curved gold filigree choker with center red cabochon.
     - **12 Distinct Earring Pairs in Tray** (`IMG_0299.HEIC` / `IMG_0300`..`0303`).
     - **1 Chandelier Earring Set** (`PROD-002`, `IMG_0437`..`0442`) — currently occluded by inventory tags.

3. **Non-Jewellery / Out-of-Scope Archive Artifacts:**
   - `IMG_0329.HEIC`: 2-gram 999 fine gold bullion coin.
   - `IMG_0444.HEIC`: Exterior/interior storefront photo of the physical jewellery merchant shop in Gadag.
   - `IMG_0839.JPG.jpeg`: Sterling silver dual pooja cup (kumkum/haldi container).
   - `IMG_0231.HEIC`: Cubic zirconia silver fashion tennis necklace set.
   - `IMG_0360.HEIC`: 14 loose repoussé gold taweez/pendant charms scattered on fabric.

---

## 2. Complete Original Image Inventory

The original archive `received_photos.zip` contains **45 total files**:
- **2 documentation files:** `README.txt` and `README.html`
- **43 original photographs:** 12 JPEG (`.JPG.jpeg`), 1 PNG (`.PNG`, internal JPEG encoding), and 30 HEIF (`.HEIC`). Total uncompressed raw image data: **79.39 MB**.

| # | Original Folder | Filename | Format | Raw Resolution | Display Resolution | Size | Blur Var (Sharpness) | Subject / Visual Description |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | `01_Earrings_Set_1_0423` | `IMG_0423.JPG.jpeg` | JPEG | 3840 × 2160 | 2160 × 3840 | 1,841 KB | 106.1 | Stud tops only held in hand against yellow retail card (incomplete) |
| 2 | `01_Earrings_Set_1_0423` | `IMG_0428.JPG.jpeg` | JPEG | 3840 × 2160 | 2160 × 3840 | 1,777 KB | 90.6 | **Primary Hero:** Full hanging jhumka pair on red velvet |
| 3 | `01_Earrings_Set_1_0423` | `IMG_0429.JPG.jpeg` | JPEG | 3840 × 2160 | 2160 × 3840 | 1,750 KB | 85.1 | Full hanging jhumka pair (burst shot, slight focus shift) |
| 4 | `01_Earrings_Set_1_0423` | `IMG_0431.JPG.jpeg` | JPEG | 3840 × 2160 | 2160 × 3840 | 1,855 KB | 107.8 | Full hanging jhumka pair (burst shot, slightly wider framing) |
| 5 | `02_Earrings_Set_2_0437` | `IMG_0437.JPG.jpeg` | JPEG | 3840 × 2160 | 2160 × 3840 | 1,861 KB | 75.6 | Chandelier earrings on velvet; white barcode tag occluding ear hook |
| 6 | `02_Earrings_Set_2_0437` | `IMG_0438.JPG.jpeg` | JPEG | 3840 × 2160 | 2160 × 3840 | 2,217 KB | 141.0 | Chandelier earrings on velvet; tag looped through wire |
| 7 | `02_Earrings_Set_2_0437` | `IMG_0439.JPG.jpeg` | JPEG | 3840 × 2160 | 2160 × 3840 | 1,870 KB | 114.3 | Chandelier earrings on velvet; burst shot with tag |
| 8 | `02_Earrings_Set_2_0437` | `IMG_0440.JPG.jpeg` | JPEG | 3840 × 2160 | 2160 × 3840 | 1,952 KB | 134.7 | Chandelier earrings on velvet; burst shot with tag |
| 9 | `02_Earrings_Set_2_0437` | `IMG_0441.JPG.jpeg` | JPEG | 3840 × 2160 | 2160 × 3840 | 1,934 KB | 131.4 | Chandelier earrings on velvet; burst shot with tag |
| 10 | `02_Earrings_Set_2_0437` | `IMG_0442.JPG.jpeg` | JPEG | 3840 × 2160 | 2160 × 3840 | 1,930 KB | 131.4 | Chandelier earrings on velvet; burst shot with tag |
| 11 | `03_Necklace_IMG_0062` | `IMG_0062.JPG.jpeg` | JPEG | 960 × 1280 | 960 × 1280 | 213 KB | 1,149.4 | **Singleton:** Royal Ruby Choker on red velvet; only source photo |
| 12 | `04_Long_Necklace_IMG_0143` | `IMG_0143.PNG` | JPEG | 1078 × 1441 | 1078 × 1441 | 398 KB | 923.5 | **Singleton:** Temple Long Haar with pink medallions; only source photo |
| 13 | `05_Ornate_Jewellery_Closeups_0300` | `IMG_0300.HEIC` | HEIF | 2236 × 3731 | 2236 × 3731 | 1,784 KB | 541.0 | Macro closeup of earring compartment 1 in merchant tray |
| 14 | `05_Ornate_Jewellery_Closeups_0300` | `IMG_0301.HEIC` | HEIF | 2239 × 4031 | 2239 × 4031 | 1,704 KB | 267.2 | Macro closeup of earring compartment 2 in merchant tray |
| 15 | `05_Ornate_Jewellery_Closeups_0300` | `IMG_0302.HEIC` | HEIF | 2777 × 3703 | 2777 × 3703 | 1,963 KB | 401.2 | Macro closeup of earring compartment 3 in merchant tray |
| 16 | `05_Ornate_Jewellery_Closeups_0300` | `IMG_0303.HEIC` | HEIF | 2599 × 3465 | 2599 × 3465 | 1,832 KB | 419.9 | Macro closeup of earring compartment 4 in merchant tray |
| 17 | `06_Chain_or_Jewellery_on_Grey_0344` | `IMG_0344.HEIC` | HEIF | 4284 × 5712 | 4284 × 5712 | 3,208 KB | 91.2 | Long Haar #1 on white display card (round filigree pendant, tag 18.140g) |
| 18 | `06_Chain_or_Jewellery_on_Grey_0344` | `IMG_0345.HEIC` | HEIF | 4284 × 5712 | 4284 × 5712 | 3,103 KB | 112.5 | Long Haar #2 on white display card (shield pendant with rubies, tag 12.210g) |
| 19 | `06_Chain_or_Jewellery_on_Grey_0344` | `IMG_0350.HEIC` | HEIF | 4284 × 5712 | 4284 × 5712 | 3,616 KB | 157.7 | Long Haar #3 on white display card (crescent tassel medallion, tag 15.720g) |
| 20 | `07_Fabric_Background_Reference` | `IMG_0034.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 1,707 KB | 114.2 | Choker A (Two-Tone): front flatlay on red velvet (wide crop) |
| 21 | `07_Fabric_Background_Reference` | `IMG_0035.HEIC` | HEIF | 2565 × 3847 | 2565 × 3847 | 1,611 KB | 128.9 | Choker A (Two-Tone): front flatlay on red velvet (tighter crop) |
| 22 | `07_Fabric_Background_Reference` | `IMG_0037.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 2,017 KB | 182.6 | **Primary Hero (Choker A):** Centered front flatlay, sharpest focus |
| 23 | `07_Fabric_Background_Reference` | `IMG_0038.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 2,097 KB | 206.6 | Choker A (Two-Tone): burst shot of IMG_0037 |
| 24 | `07_Fabric_Background_Reference` | `IMG_0039.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 1,644 KB | 100.7 | Choker A (Two-Tone): burst shot with slight shadow shift |
| 25 | `07_Fabric_Background_Reference` | `IMG_0040.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 2,155 KB | 238.0 | Choker B (Ruby Heart): front flatlay on red velvet |
| 26 | `07_Fabric_Background_Reference` | `IMG_0041.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 2,143 KB | 240.0 | **Primary Hero (Choker B):** Centered front flatlay, sharpest focus |
| 27 | `07_Fabric_Background_Reference` | `IMG_0042.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 1,969 KB | 177.5 | Choker B (Ruby Heart): burst shot |
| 28 | `07_Fabric_Background_Reference` | `IMG_0043.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 1,838 KB | 137.8 | Choker B (Ruby Heart): burst shot |
| 29 | `07_Fabric_Background_Reference` | `IMG_0044.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 1,171 KB | 23.0 | Choker B (Ruby Heart): **REJECTED** (severe hand motion blur) |
| 30 | `07_Fabric_Background_Reference` | `IMG_0235.HEIC` | HEIF | 2268 × 4032 | 2268 × 4032 | 1,408 KB | 423.1 | **Recoverable Masterpiece:** Gold choker with filigree fringe & ruby cabochon |
| 31 | `07_Fabric_Background_Reference` | `IMG_0351.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 1,370 KB | 231.8 | Gold Choker #1 on white card (pointed drop motif, tag 10.160g) |
| 32 | `07_Fabric_Background_Reference` | `IMG_0352.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 1,310 KB | 255.5 | Gold Choker #2 on white card (heart repoussé motif, tag 16.240g) |
| 33 | `07_Fabric_Background_Reference` | `IMG_0353.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 1,231 KB | 208.6 | Gold Choker #3 on white card (sunburst medallion, tag 9.250g) |
| 34 | `07_Fabric_Background_Reference` | `IMG_0354.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 1,305 KB | 225.7 | Gold Choker #4 on white card (scalloped arch motif, tag 10.070g) |
| 35 | `07_Fabric_Background_Reference` | `IMG_0355.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 1,519 KB | 203.5 | Gold Choker #5 on white card (flared fan medallion, tag 11.410g) |
| 36 | `07_Fabric_Background_Reference` | `IMG_0360.HEIC` | HEIF | 3023 × 2641 | 3023 × 2641 | 2,087 KB | 506.6 | 14 loose repoussé gold pendant charms / taweez on red fabric |
| 37 | `08_Dark_or_Unclear_Review` | `IMG_0231.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 2,180 KB | 118.1 | Cubic Zirconia silver fashion tennis necklace & earrings set |
| 38 | `08_Dark_or_Unclear_Review` | `IMG_0299.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 2,366 KB | 425.5 | **Merchant Tray:** 4×3 grid containing 12 distinct pairs of gold earrings |
| 39 | `08_Dark_or_Unclear_Review` | `IMG_0329.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 732 KB | 201.9 | 2-gram 999 Fine Gold bullion coin held on hand |
| 40 | `08_Dark_or_Unclear_Review` | `IMG_0444.HEIC` | HEIF | 5712 × 4284 | 5712 × 4284 | 2,427 KB | 95.1 | Physical jewellery shop exterior/interior in Gadag |
| 41 | `08_Dark_or_Unclear_Review` | `IMG_0588.HEIC` | HEIF | 4284 × 5712 | 4284 × 5712 | 4,866 KB | 199.7 | **Recoverable Masterpiece:** 4-tier Grand Peacock Temple Haar in velvet box |
| 42 | `08_Dark_or_Unclear_Review` | `IMG_0828.HEIC` | HEIF | 3024 × 4032 | 3024 × 4032 | 1,773 KB | 1,045.9 | **Recoverable Masterpiece:** Temple Lakshmi Ruby & Emerald Pendant |
| 43 | `09_Fastening_or_Extra_View` | `IMG_0839.JPG.jpeg` | JPEG | 3840 × 2160 | 2160 × 3840 | 1,562 KB | 54.6 | Sterling silver pooja double cup (kumkum/haldi article, not jewellery) |

---

## 3. Current Catalogue Image Diversity Audit

Below is the required forensic audit of the five currently approved storefront products:

| Product | Original Photographs in Archive | Genuine Distinct Views | Processed Derivatives Generated | Missing Views (Required for Luxury Standard) | Diversity Verdict |
|:---|:---:|:---:|:---:|:---|:---:|
| **`PROD-001`**<br>Traditional 22K Gold Drop Earrings | **4**<br>(`IMG_0423`, `IMG_0428`, `IMG_0429`, `IMG_0431`) | **2**<br>1. Complete hanging pair on velvet (`IMG_0428`)<br>2. Stud tops resting on fingers (`IMG_0423`) | **5**<br>`listing` (1:1), `gallery` (4:5), `featured` (16:9), `detail` (1:1 crop), `master` (PNG) | Rear hook view, ear-post clasp view, on-model/scale shot, true optical macro of bell dome filigree | **MODERATE**<br>Has 2 genuine views, but lacks side, rear, and scale shots. |
| **`PROD-003`**<br>Royal Gold Ruby Choker with Pearls | **1**<br>(`IMG_0062.JPG.jpeg`) | **1**<br>Single front-flatlay view only | **5**<br>`listing` (1:1), `gallery` (4:5), `featured` (16:9), `detail` (1:1 crop), `master` (PNG) | Alternate 3/4 angle, rear view, adjustable zardosi dori fastening view, optical macro of ruby bezel mounts, on-mannequin wearing shot | **CRITICALLY LOW**<br>Only 1 physical photo exists. All 5 catalogue views are aspect ratio crops. |
| **`PROD-004`**<br>Temple Long Gold Haar with Medallions | **1**<br>(`IMG_0143.PNG`) | **1**<br>Single vertical flatlay view only | **5**<br>`listing` (1:1), `gallery` (4:5), `featured` (16:9), `detail` (1:1 crop), `master` (PNG) | Draped neckline view, side profile of cascading swags, shoulder medallion rear view, clasp/thread fastening, wearing scale shot | **CRITICALLY LOW**<br>Only 1 physical photo exists. All 5 catalogue views are aspect ratio crops. |
| **`PROD-007A`**<br>Floral Two-Tone Gold & Rhodium Choker | **5**<br>(`IMG_0034`, `IMG_0035`, `IMG_0037`, `IMG_0038`, `IMG_0039`) | **1**<br>Single top-down flatlay on velvet (others are near-identical burst shots) | **5**<br>`listing` (1:1), `gallery` (4:5), `featured` (16:9), `detail` (1:1 crop), `master` (PNG) | 3/4 angle showing curved collar depth, side view of dangling filigree tassels, rear hinge/hook view, on-model collarbone scale shot | **LOW**<br>Multiple source files exist, but represent a single photographic angle. |
| **`PROD-007B`**<br>Royal Ruby Teardrop Medallion Choker | **5**<br>(`IMG_0040`, `IMG_0041`, `IMG_0042`, `IMG_0043`, `IMG_0044`) | **1**<br>Single top-down flatlay on velvet (others are burst shots; `IMG_0044` is blurry) | **5**<br>`listing` (1:1), `gallery` (4:5), `featured` (16:9), `detail` (1:1 crop), `master` (PNG) | 3/4 dimensional collar view, optical macro of center ruby heart, rear fastening/back-plate view, on-model scale shot | **LOW**<br>Multiple source files exist, but represent a single photographic angle. |

---

## 4. Quarantined & Unclassified Image Review

Our audit revealed that several quarantined or unclassified assets represent **genuine, high-value gold jewellery** that can be safely recovered without generative reconstruction:

### A. The Three "Hidden" Masterpieces in `08_Dark_or_Unclear_Review` & `07_Fabric`
1. **`IMG_0588.HEIC` (Grand Peacock Temple Long Haar):**
   - **Quality:** 4284 × 5712, 4.86 MB, extremely sharp (BlurVar: 199.7).
   - **Visuals:** A magnificent 4-tier graduated gold bead haar with elaborate peacock shoulder medallions set with genuine rubies and emeralds, resting inside a velvet-lined box.
   - **Recovery Verdict:** **HIGH PRIORITY RECOVERY**. This was falsely relegated to the dark/unclear folder. It is fully intact, beautifully exposed, and can be isolated cleanly with zero ambiguity.
2. **`IMG_0828.HEIC` (Temple Lakshmi Pendant):**
   - **Quality:** 3024 × 4032, 1.77 MB, ultra-high sharpness (BlurVar: 1,045.9).
   - **Visuals:** Intricate solid gold Goddess Lakshmi repoussé temple pendant crowned by a teardrop ruby, twin emerald cabochons, and 6 hanging ruby bead drops on red velvet.
   - **Recovery Verdict:** **HIGH PRIORITY RECOVERY**. Pristine, centered, clean background. Ideal for a standalone "Temple Pendants" category.
3. **`IMG_0235.HEIC` (Curved Gold Filigree Choker):**
   - **Quality:** 2268 × 4032, 1.4 MB, sharp (BlurVar: 423.1).
   - **Visuals:** Solid gold choker with central ruby cabochon, filigree swag, and hanging tassels on red velvet.
   - **Recovery Verdict:** **HIGH PRIORITY RECOVERY**. A third distinct choker that was buried in `07_Fabric_Background_Reference`.

### B. `PROD-006` (Card-Mounted Necklaces & Haars — 8 Distinct Pieces)
- **Sources:** `IMG_0344`, `IMG_0345`, `IMG_0350` (3 Haars) and `IMG_0351`..`0355` (5 Chokers).
- **Analysis:** Each necklace is pinned to a white presentation card. While the card is a fixture (not jewellery), the jewellery itself is **100% visible and unoccluded**.
- **Recovery Verdict:** **VIABLE VIA PRECISE MASKING**. Because the white packaging card has a clean geometric contrast against the red velvet and the gold jewellery, the card can be segmented out, or the pieces can be presented with an honest editorial treatment (e.g. "Presentation Card Archive"). This immediately expands the catalogue by **8 genuine designs**.

### C. `PROD-005` (Merchant Earring Tray — 12 Distinct Pairs)
- **Sources:** `IMG_0299.HEIC` (Full 4×3 tray) + `IMG_0300`..`0303` (4 Macro closeups).
- **Analysis:** Contains 12 distinct pairs of traditional Indian gold jhumkas and studs.
- **Recovery Verdict:** **VIABLE FOR SELECT PIECES**. The 4 compartments captured in high-resolution macro shots (`IMG_0300` through `IMG_0303`) can be individually isolated and onboarded as distinct earring products. The remaining 8 compartments from `IMG_0299` have lower per-item pixel density and would require reshooting for luxury standard.

### D. `PROD-002` (Chandelier Earrings with Tag — 6 Photos)
- **Sources:** `IMG_0437` through `IMG_0442`.
- **Analysis:** High-quality, sharp photographs, but the white merchant barcode tag loops directly through the ear wire.
- **Recovery Verdict:** **REMAINS QUARANTINED**. Automated removal would require hallucinating the missing wire. Requires a physical studio reshoot without the retail tag or precision manual pen-tool reconstruction.

### E. Non-Jewellery / Out-of-Scope Items
- `IMG_0329` (Gold Coin), `IMG_0444` (Shopfront), `IMG_0839` (Silver Cup), `IMG_0231` (CZ Set), `IMG_0360` (Loose Charms): **REJECT FOR JEWELLERY CATALOGUE**. Can be preserved for brand editorial or supporting story, but not as wearable fine jewellery SKUs.

---

## 5. Luxury Jewellery Storefront: Ideal Photography Standards

To compete with premier luxury houses (e.g., Cartier, Boucheron, Sabyasachi Jewellery, Tanishq Zoya), each product requires a standard multi-asset portfolio:

### Standard 7-Asset Luxury Portfolio per SKU:
1. **Primary Product Hero (1:1 / 4:5):** Clean, unoccluded front shot on warm ivory/alabaster canvas with soft directional contact shadow.
2. **Full Front Symmetry View:** Complete piece showing full proportions, drape, and chain length.
3. **Alternate 3/4 Dimensional Angle:** Demonstrates depth, curved collar volume, dome relief, and structural thickness.
4. **Fastening & Rear Craftsmanship View:** Back-plate inspection, hallmark stamp, gold hinge, screw-back post, or silk zari dori cord.
5. **Optical Macro Detail (1:1):** High-magnification capture of gemstone bezels, granulation, enamel champlevé, or pearl stringing.
6. **Scale & On-Model Wearing View:** Worn on model collarbone, neck, or ear to convey real-world scale and drop length.
7. **Editorial Flatlay / Atmospheric:** Styled composition evoking heritage and provenance.

### Current Portfolio vs. Luxury Requirement:
```
Current Assets:         [Primary Hero] (Extracted) -> [Aspect Ratio Crops (1:1, 4:5, 16:9)]
Luxury Requirement:     [Hero] + [Front] + [3/4 Angle] + [Rear/Clasp] + [True Macro] + [Model/Scale] + [Editorial]
Deficiency:             Archive consists almost exclusively of single-angle flatlays on red velvet.
```

---

## 6. Recommended Catalogue Expansion Strategy

### Phase 1: Rapid Catalogue Expansion (Immediate — from Existing Archive)
Without inventing missing angles or using generative AI, we can expand the catalogue from **5 pieces to 16 authenticated pieces** by recovering clean, uncompromised pieces already in the archive:

1. **Add `PROD-008`: Grand Peacock Temple Haar** (`IMG_0588.HEIC` — pristine 4.86 MB asset).
2. **Add `PROD-009`: Temple Lakshmi Ruby & Emerald Pendant** (`IMG_0828.HEIC` — sharp 1,045 BlurVar asset).
3. **Add `PROD-010`: Royal Gold Filigree Choker C** (`IMG_0235.HEIC`).
4. **Add `PROD-011` through `PROD-013`: 3 Long Gold Haars** (Recovered from `IMG_0344`, `IMG_0345`, `IMG_0350` via card segmentation).
5. **Add `PROD-014` through `PROD-018`: 5 Heritage Gold Chokers** (Recovered from `IMG_0351`..`0355` via card segmentation).
6. **Add `PROD-019` through `PROD-022`: 4 Macro-Audited Earring Pairs** (Recovered from `IMG_0300`..`0303`).

### Phase 2: Professional Studio Reshoot Protocol (To Solve Photographic Diversity)
To achieve true luxury depth for each product, commission a standardized studio photography session:
- **Equipment:** 100mm f/2.8 Macro lens, diffused softboxes, polarized lighting to eliminate harsh metallic glare.
- **Shot List per Product:** 
  1. Front on bust form
  2. 45° profile view
  3. Reverse clasp/hallmark inspection
  4. 2× Optical macro of key motif
  5. On-model wearing reference
- **Handling:** Remove all merchant barcode tags and plastic wrap prior to shooting.
