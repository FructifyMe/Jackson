# MEMORY — SavATree Satellite Lead Gen Project

> **Purpose:** This file preserves critical context across conversation compactions. Claude should read this file at the start of any resumed session to recover full project state.
> **Last Updated:** March 3, 2026 — Session 1

---

## CRITICAL CORRECTIONS

- **Company name is SavATree** (www.savatree.com) — NOT "Savitri". Earlier deliverables used "Savitri" by mistake and need renaming.
- Jackson works at the **Middleton, MA branch** of SavATree
- SavATree is a national company with ISA Certified Arborists, TRAQ-qualified consultants, and ASCA credentials
- Files have been renamed from `savitri-*` to `savatree-*` and branding updated inside all files

## USER PROFILE

- **Mike Fructify** (fructifyme@gmail.com) — Project lead, Jackson's father, technical builder
- **Jackson Fructify** — Arborist & Sales PM at SavATree Middleton branch. The end user of everything we build.
- Mike's communication style: direct, iterative, pivots quickly when he sees a better angle. Prefers "build it and show me" over lengthy planning discussions.
- Budget-conscious: MVP/free first, prove it works, then invest.

## KEY DECISIONS MADE

1. **Target territory:** Melrose, Stoneham, Wilmington, Wakefield, Reading, North Reading (all MA)
2. **Strategy pivot:** Mike redirected from residential-only to prioritizing HOAs, commercial, condos — "bigger and better areas" with maximized urgency drivers (insurance, liability, property value)
3. **Detection method:** NDVI change detection via Sentinel-2 + NAIP confirmation, processed through Google Earth Engine
4. **Scoring model:** 4-factor weighted: Canopy Decline 30%, Property Classification 30%, Liability Exposure 25%, Property Value 15%
5. **ISA form approach:** Interactive digital version that pre-fills satellite-detectable fields (~34% of form fields), with integrated lead scoring tab
6. **Tier system:** S-Tier (HOA 9.5, Commercial 9.0), A-Tier (Municipal 8.0, Multifamily 8.0), B-Tier (High-value residential), C-Tier (Standard residential)

## CURRENT STATE

### Completed
- Feasibility study (detection methods, data sources, risks, MVP plan)
- Lead qualification framework (tier rankings, urgency drivers, pitch language, scoring model)
- Interactive ISA digital assessment form (4 tabs: Assessment, Field Mapping, Risk Matrices, Lead Score)
- Lead Score tab with auto-calculation, outreach recommendations, contract estimates
- ISA matrix logic verified correct against TRAQ standards
- Project structure files (PROJECT.md, MEMORY.md, CHANGELOG.md)

### Wakefield Test — COMPLETE
- Satellite test run successfully by Mike — 988 hotspot clusters, 13,348 flagged pixels
- 7 qualified leads identified with contacts enriched
- Lead dashboard built: `wakefield-lead-targets.html` (~2.2MB, self-contained with embedded satellite image)
- All leads have actionable contact information (emails, phones, LinkedIn)

### Next Up
- **Expand to full 6-town territory** — run NDVI analysis on Melrose, Stoneham, Wilmington, Reading, North Reading
- **Smartsheet pipeline setup** — lead tracking sheet for Jackson
- **Outreach materials** — personalized one-pagers per lead with satellite imagery
- **Deploy HTML files** — GitHub Pages or Vercel (discussed, not yet actioned)
- **Outreach sequences** — draft emails for each lead tier

## FILES IN WORKING FOLDER

```
C:\Users\MikeF\Desktop\Cassidy\Claude CoWork Jackson\
├── PROJECT.md                                    ← Project plan & overview
├── MEMORY.md                                     ← This file (compaction recovery)
├── CHANGELOG.md                                  ← Session log
├── SATELLITE-TEST-GUIDE.md                       ← How to run the satellite test
├── ISA-Basic-Tree-Risk-Form-fillable.pdf         ← Official ISA form (reference)
├── savatree-canopy-lead-gen-feasibility.html      ← Feasibility study
├── savatree-lead-qualification-framework.html     ← Lead qualification framework
├── savatree-isa-digital-assessment.html           ← ISA form + Lead Score (4 tabs)
├── gee-ndvi-wakefield-test.js                    ← GEE script — paste into code.earthengine.google.com
├── ndvi_change_detection.py                      ← Python pipeline — run locally for full analysis
├── wakefield-ndvi-analysis.png                   ← 4-panel NDVI satellite output (from test run)
├── wakefield-ndvi-results.json                   ← 988 clusters, full stats
├── wakefield-decline-hotspots.csv                ← 988 hotspot rows with lat/lng
└── wakefield-lead-targets.html                   ← 🔥 Lead dashboard — 7 leads, contacts, satellite image, lightbox
```

## TECHNICAL CONTEXT

### Satellite Data Key Facts
- Sentinel-2: 10m resolution, free, 5-day revisit, 13 bands including NIR + Red Edge
- NAIP: 0.6m resolution, free, 4-band RGBNIR, ~3-year update cycle
- NDVI scale: -1 to +1. Healthy trees 0.6–0.9. Stressed <0.3. Decline >15% = flagged.
- Mixed pixel problem: 10m resolution mixes trees/house/lawn on small residential lots. Fine for HOA/commercial (larger canopy).
- Google Earth Engine: free JS code editor (code.earthengine.google.com) + Python API
- STAC API (Element84 Earth Search): free, no-auth access to Sentinel-2 COGs on AWS
- Cowork VM blocks outbound satellite API calls — analysis must run on Mike's local machine

### ISA Form Field Mapping
- ~35 total fields on ISA Basic Tree Risk Assessment form
- ~12 fields (34%) can be pre-populated from satellite data
- Most valuable satellite pre-fills: Crown health (NDVI → foliage/density/dieback)
- Risk calculation: Matrix 1 (Likelihood of Failure × Likelihood of Impact) → Matrix 2 (Combined Likelihood × Consequences) → Risk Rating (Low/Moderate/High/Extreme)

### Lead Scoring Tiers
- S-Tier: ≥ 75/100 → Immediate outreach (48 hours)
- A-Tier: ≥ 55/100 → Outreach within 1 week
- B-Tier: ≥ 35/100 → Nurture sequence (2 weeks)
- C-Tier: < 35/100 → Monitor, revisit in 3 months

### Contract Value Estimates
- HOA/Condo: Initial $8K–$25K, Annual $5K–$15K
- Commercial: Initial $5K–$20K, Annual $3K–$12K
- Municipal: Initial $10K–$50K, Annual $5K–$25K
- High-value Residential: Initial $2K–$8K, Annual $1K–$3K

## CONNECTED TOOLS & INTEGRATIONS

| Tool | Status | Use Case |
|------|--------|----------|
| Apollo | Connected | Decision-maker lookup, contact enrichment |
| Clay | Connected | Lead enrichment, company research |
| Gmail | Connected | Outreach emails |
| Google Calendar | Connected | Meeting scheduling |
| Smartsheet | Connected | Pipeline tracking (not yet configured) |
| Google Drive | Connected | Document storage |
| Excalidraw | Connected | Diagrams/visuals |

## CONVERSATION STYLE NOTES

- Mike says "Savitri" but means **SavATree** — already corrected
- Mike thinks in terms of maximizing value: "bigger and better areas", "maximize the reasons why they would need tree work"
- Prefers interactive HTML deliverables over static documents
- Appreciates when I show the work product immediately rather than explaining what I'll do
- Budget: free/MVP first, prove concept, then invest
