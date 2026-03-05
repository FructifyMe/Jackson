# CHANGELOG — SavATree Satellite Lead Gen Project

> Session-by-session log of what was built, decided, and changed.

---

## Session 1 — March 3, 2026

### Research & Discovery
- Researched satellite imagery feasibility for canopy loss detection
- Evaluated Sentinel-2, Landsat, NAIP, ForSens/Karuna, Purdue uTREE
- Confirmed NDVI change detection as primary method
- Identified Google Earth Engine + MassGIS as free processing/parcel stack

### Deliverables Created
1. **`savitri-canopy-lead-gen-feasibility.html`** — Comprehensive feasibility study covering detection methods, ISA connection, data sources, 6-town feasibility, MVP pipeline, risks
2. **`savitri-lead-qualification-framework.html`** — Lead qualification with tier rankings (S/A/B/C), urgency driver matrix, satellite detection by property type, 4-factor scoring model, sample pitch language
3. **`savitri-isa-digital-assessment.html`** — Interactive digital ISA Basic Tree Risk Assessment form with:
   - NDVI satellite pre-fill fields with auto-calculation
   - All 4 tree zones (Crown, Branches, Trunk, Roots/Soil)
   - 3 failure assessment sections with Matrix 1 → Matrix 2 auto-calculation
   - Overall risk rating auto-calculation
   - Field Mapping Guide tab (34% satellite-detectable)
   - Risk Matrices reference tab
   - **Lead Score tab** (added later in session) with:
     - 4-factor weighted scoring engine
     - Auto-pull from NDVI and risk data
     - Property classification and value inputs
     - Urgency driver chips
     - Outreach recommendation with pitch language
     - Contract value estimates
     - Copy-to-clipboard lead summary export

### Key Decisions
- **Strategy pivot:** From residential → HOA/Commercial/Condo priority (Mike's direction)
- **ISA form:** Build interactive digital version rather than just a reference
- **Lead scoring:** Integrated directly into the ISA assessment form as a 4th tab

### Corrections
- Company name corrected from "Savitri" to **SavATree** (savatree.com)
- All files renamed from `savitri-*` to `savatree-*` and branding updated inside

### Project Structure Created
- `PROJECT.md` — Full project plan and overview
- `MEMORY.md` — Compaction recovery context
- `CHANGELOG.md` — This file

### Tools Assessed
- Confirmed existing connections (Apollo, Clay, Gmail, Calendar, Smartsheet, Drive, Excalidraw) cover needs
- No GIS-specific MCP connectors exist — satellite work will be custom Python + GEE

---

## Session 2 — March 3, 2026

### Satellite Analysis Pipeline Built
1. **`gee-ndvi-wakefield-test.js`** — Google Earth Engine JavaScript script for instant browser-based NDVI analysis:
   - Paste into code.earthengine.google.com and click Run
   - Sentinel-2 L2A cloud-masked NDVI composites
   - Summer 2023 vs Summer 2025 (auto-fallback to 2024)
   - 4 map layers: NDVI 2023, NDVI Recent, NDVI Change, Decline Detection
   - Detection classification: healthy (green), moderate decline (orange), severe (red)
   - Console output with pixel counts and statistics
   - GeoTIFF export commands (commented out, ready to uncomment)
   - Also includes 6-town bounding box for later expansion

2. **`ndvi_change_detection.py`** — Full Python pipeline for automated local analysis:
   - Uses Element84 Earth Search STAC API (free, no auth needed)
   - Downloads Sentinel-2 COGs directly (no GEE account required)
   - NDVI calculation, vegetation masking, change detection
   - scipy cluster analysis to find hotspot groups
   - Outputs: 4-panel PNG, JSON results, CSV with lat/lng + Google Maps links
   - Configurable for any bounding box (ready to expand to 6 towns)

3. **`SATELLITE-TEST-GUIDE.md`** — Setup and usage guide:
   - Step-by-step for both GEE and Python approaches
   - NDVI interpretation table
   - Troubleshooting guide
   - Deployment options discussion (GitHub Pages, Vercel, GitHub repo)
   - Instructions for expanding to full 6-town territory

### Key Technical Decisions
- **Dual pipeline approach:** GEE JS for quick visual exploration, Python for automated batch processing
- **STAC API over GEE Python:** The Python script uses STAC (no auth) instead of GEE Python API (requires OAuth). Simpler setup for Mike to run.
- **Test area:** Wakefield, MA — Lake Quannapowitt area chosen for mix of residential + commercial + mature canopy
- **Bounding box:** [-71.095, 42.485, -71.055, 42.510]
- **Thresholds:** Vegetation min NDVI 0.4, moderate decline >10%, severe >20%

### Discovery: VM Network Limitations
- Cowork VM sandbox blocks outbound HTTPS to satellite data APIs (STAC, GEE, Copernicus, Sentinel Hub)
- All satellite analysis scripts must run on Mike's local machine or a cloud server
- This is expected — the production pipeline will run outside the Cowork environment anyway

### Deployment Discussion (Surfaced, Not Yet Actioned)
- Mike wants HTML deliverables viewable outside his home PC
- Options discussed: GitHub Pages (recommended), Vercel, GitHub repo
- To be set up after test confirms the approach works

---

## Session 3 — March 3, 2026 (continued)

### Satellite Test Results — Wakefield Confirmed Working
- Mike ran `ndvi_change_detection.py` locally — **successful**
- Fixed STAC API `sortby` bug (Element84 doesn't support server-side sort by `eo:cloud_cover`)
- Results: 77,391 vegetated pixels, 13,348 flagged (17.2%), 988 hotspot clusters
- Scenes: S2B_19TCH_20230901 vs S2B_19TCH_20250831 (near-zero cloud cover)
- Mean NDVI: 0.6147 → 0.5779 (mean change -0.0421)

### Lead Identification & Enrichment
1. Cross-referenced top 30 severe hotspot clusters with web research to identify 7 property-level targets
2. Enriched contacts via **Clay** (Equity Residential, Crowninshield Management) and **Apollo** (People API)
3. Found **Dennis Fazio** — Wakefield Tree Warden (MA Tree Warden of the Year 2021) for municipal leads
4. Identified **Cynthia Carney / Carney & Company LLC** as Lakeside Office Park management

### Contact Enrichment Results
- **Equity Residential** (The Basin): 5 key contacts found — Steve Dybowski (VP National Facilities), Kevin Cameron (Sr Regional Mgr), Mickey Mathews (Regional Facilities Mgr), Dan Sprague (Maintenance Supervisor, Wilmington — **email confirmed: dsprague@eqr.com**), Michael Quintanilla (Regional Mgr)
- **Crowninshield Management** (Force Multiplier): 6 contacts with confirmed emails — Janet Perez-Frye (VP/Controller, jpfrye@crowninshield.com), Jacqueline Goohs (Regional PM Condos, jgoohs@crowninshield.com), Adrian Litscher (Regional PM, alitscher@crowninshield.com), John Fantasia (Regional PM, jfantasia@crowninshield.com), Kerry Adie (PM, kadie@crowninshield.com), Eleana Farchione (PM, efarchione@crowninshield.com)
- **Lakeside Office Park**: Cynthia Carney, Carney & Company LLC, (978) 314-2556
- **Wakefield DPW**: Dennis Fazio, Tree Warden, (781) 246-6301

### Deliverable Updated
- **`wakefield-lead-targets.html`** — Rebuilt with full enriched contact data:
  - 7 lead cards with collapsible contact sections
  - Clickable email (mailto:) and LinkedIn profile links
  - Pitch language per lead
  - Google Maps links
  - Methodology section with full satellite analysis stats
  - Mobile-responsive, self-contained HTML

### Key Insights
- **Dan Sprague** at Equity Residential is based in **Wilmington, MA** — one of Jackson's 6 target towns. He's the closest geographic match for The Basin property.
- **Crowninshield** is the strongest "force multiplier" — they explicitly service Wakefield on their website and manage 5,000+ units. One relationship could unlock dozens of properties.
- **The Basin** is still under construction (Building 2 due Q2 2026) — landscaping is being established NOW, making this the perfect time for a tree care partnership.
- **Dennis Fazio** won MA Tree Warden of the Year — personalized outreach referencing this is a strong opening.

---

## Session 4 — March 5, 2026

### UI Redesign & Maps Fix (Completed Session 3, finalized Session 4)
- Fixed Google Maps links: changed from raw NDVI coordinates to address-based searches
- Complete UI overhaul: dark theme → clean white cards with SavATree forest green branding
- Added card shadows, gradients, collapsible contact/pitch sections, mobile responsive

### Contact Enrichment Completed
All 7 leads now have actionable contact information:
- **Lakeside Office Park**: Cynthia Carney — office (978) 531-3630, mobile (978) 314-2556, LinkedIn
- **The Basin / EQR**: 5 contacts with predicted emails (FLast@eqr.com pattern, 94% accuracy). Michael Quintanilla email added.
- **Gates of Greenwood**: No public HOA contacts — linked to Crowninshield as potential manager
- **Forest Glade Cemetery**: Dennis Fazio — dfazio@wakefield.ma.us, (781) 246-6301 x3
- **Wakefield Landing**: CPS Management — manager@cpspm.com, (781) 779-7205
- **Crowninshield Management**: 6 contacts with confirmed emails
- **Lakeside & Temple Israel Cemeteries**: Split into two entities — Lakeside managed by DPW (Fazio), Temple Israel managed by Temple Emmanuel (info@wakefieldtemple.org, (781) 245-1886)

### Satellite Intelligence Section Added to Dashboard
- Embedded 4-panel NDVI analysis image (compressed JPEG, base64-encoded) directly into `wakefield-lead-targets.html`
- Added click-to-zoom lightbox with dark overlay (Escape key / click to close)
- Color legend: healthy (green), moderate decline (orange), severe decline (red), water (blue)
- Tech stack chips: ESA Copernicus Sentinel-2 L2A, 10m Resolution, STAC API, NDVI Change Detection, SciPy Connected Components, Python + rasterio
- "SENTINEL-2 NDVI" badge for credibility
- Self-contained HTML at ~2.2MB — no external dependencies, email/share anywhere

### Fructify Plugin Updated
- Added satellite imagery embedding technique to client-deliverables skill
- Added NDVI/GIS data integration patterns to Fructify Frameworks skill
- Documented base64 image embedding + lightbox pattern for self-contained HTML deliverables

### Key Technical Notes
- Image compression: PNG (3.3MB) → JPEG quality 82 (815KB) → base64 (~1.1MB in HTML)
- Lightbox uses pure CSS/JS — no external libraries
- Python Pillow used for compression (already available in Cowork VM)
- Total HTML file: ~2.2MB — still performant for email/browser sharing
